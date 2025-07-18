from frankenstem.audio_io import load_audio
from frankenstem.splicer import slice_into_random_beats, slice_by_transients
from frankenstem.combiner import combine_segments
from frankenstem.removing_silence import remove_silence
from frankenstem.filename_parser import load_wavs_from_folder
from frankenstem.classes import StemType, Song
from frankenstem.config import FrankenstemConfig
from frankenstem.energy_filter import filter_segments_by_energy


import soundfile as sf
from datetime import datetime
import numpy as np
import random
import os
import time

def generate_frankenstem(config: FrankenstemConfig, input_path="input", output_path="output"):
    start_time = time.time()##DEBUG
    TARGET_DURATION_SECONDS = config.target_duration
    BPM = config.bpm
    selected_stem_types = config.selected_stem_types
    selected_slicing_function = config.selected_slicing_function

    if not os.path.exists(input_path):
        raise FileNotFoundError(f"Input path '{input_path}' does not exist.")
    if not os.path.exists(output_path):
        os.makedirs(output_path)

    stem_wavs = load_wavs_from_folder(input_path)

    print(f"[DEBUG] Number of Songs loaded: {len(stem_wavs)}")


    slice_params = {
    slice_into_random_beats: {
        "bpm": BPM,
        "min_beats": config.min_beats,
        "max_beats": config.max_beats
    },
    slice_by_transients: {
        "bpm": BPM,
        "delta": 0.5,
        "min_length_seconds": 0.5
    }
}


    all_segments = []
    sr = None  # will be set after first audio load

    for stem_type in selected_stem_types:
        for wav in stem_wavs:
            stem = wav.get_stem(stem_type)
            if not stem:
                continue

            audio, this_sr = stem.load_audio()

            if sr is None:
                sr = this_sr
            elif this_sr != sr:
                raise ValueError(f"Sample rate mismatch in stem: {stem.filepath}")

            segments = selected_slicing_function(
                audio,
                sr,
                **slice_params[selected_slicing_function]
            )

            all_segments.extend(segments)

    print(f"[PROFILE] Loading & slicing took: {time.time() - start_time:.2f}s") ##DEBUG
    slice_time = time.time() ##DEBUG

    if len(all_segments) == 0:
        raise ValueError("No valid segments found for selected stem types.")

    random.shuffle(all_segments)

    if config.filter_by_energy:
        all_segments = filter_segments_by_energy(
        segments=all_segments,
        target=config.energy_target
    )


    # Select segments up to exact target duration
    selected_segments = []
    cumulative_samples = 0
    target_samples = int(TARGET_DURATION_SECONDS * sr)

    for segment in all_segments:
        segment_length = segment.shape[-1]  # handles mono or stereo consistently
        if cumulative_samples + segment_length > target_samples:
            remaining_samples = target_samples - cumulative_samples
            if remaining_samples > 0:
                if segment.ndim == 2:
                    selected_segments.append(segment[:, :remaining_samples])
                else:
                    selected_segments.append(segment[:remaining_samples])
            break
        selected_segments.append(segment)
        cumulative_samples += segment_length

    print(f"[PROFILE] Segment selection took: {time.time() - slice_time:.2f}s") ##DEBUG
    concat_time = time.time() ##DEBUG

    # exporting fragments individually
    if config.export_fragments_individually:
        fragment_folder = os.path.join(output_path, f"fragments_{datetime.now().strftime('%m%d_%H%M')}")
        os.makedirs(fragment_folder, exist_ok=True)

        for i, seg in enumerate(selected_segments):
            out_path = os.path.join(fragment_folder, f"fragment_{i+1:03d}.wav")
            sf.write(out_path, seg.T if seg.ndim == 2 else seg, sr)

        print(f"[INFO] Saved {len(selected_segments)} fragments to {fragment_folder}")
    else: #exporting as a single concatenated Frankenstem
        frankenstem_audio = np.concatenate(selected_segments, axis=1 if selected_segments[0].ndim == 2 else 0)
        frankenstem_audio = frankenstem_audio.T  # (N, 2)

        # Filename logic
        timestamp = datetime.now().strftime("%m%d_%H%M")
        stem_names = "_".join(stem_type.name.capitalize() for stem_type in selected_stem_types)
        slice_type_name = (
            "Transient" if selected_slicing_function == slice_by_transients else
            "Beat" if selected_slicing_function == slice_into_random_beats else
            "UnknownSliceType"
        )
        duration_str = f"{int(TARGET_DURATION_SECONDS)}s"

        output_file = f"{output_path}/{stem_names}_{slice_type_name}_{duration_str}_{timestamp}.wav"

        sf.write(output_file, frankenstem_audio, sr)
        print(f"Saved Frankenstem to {output_file}")


if __name__ == "__main__":
    config = FrankenstemConfig(
        target_duration=10,  # seconds
        bpm=160,
        selected_stem_types=[StemType.VOCALS, StemType.OTHER],
        selected_slicing_function=slice_into_random_beats, # slice_by_transients, or slice_into_random_beats
        min_beats=2, # make sure this is less than max_beats
        max_beats=4,
        export_fragments_individually=False,
        filter_by_energy=True,
        energy_target="medium" #very_low, low, medium, or high

    )
    generate_frankenstem(config)

