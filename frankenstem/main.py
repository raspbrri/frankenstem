from frankenstem.audio_io import load_audio
from frankenstem.splicer import slice_into_random_beats, slice_by_transients
from frankenstem.combiner import combine_segments
from frankenstem.removing_silence import remove_silence
from frankenstem.filename_parser import load_wavs_from_folder
from frankenstem.classes import StemType, Song
from frankenstem.config import FrankenstemConfig

import soundfile as sf
from datetime import datetime
import numpy as np
import random
import os
import time

INPUT_PATH = "input"
OUTPUT_PATH = "output"

def generate_frankenstem(config: FrankenstemConfig):
    start_time = time.time()##DEBUG
    TARGET_DURATION_SECONDS = config.target_duration
    BPM = config.bpm
    selected_stem_types = config.selected_stem_types
    selected_slicing_function = config.selected_slicing_function

    if not os.path.exists(INPUT_PATH):
        raise FileNotFoundError(f"Input path '{INPUT_PATH}' does not exist.")
    if not os.path.exists(OUTPUT_PATH):
        os.makedirs(OUTPUT_PATH)

    stem_wavs = load_wavs_from_folder(INPUT_PATH)

    print(f"[DEBUG] Number of Songs loaded: {len(stem_wavs)}")


    slice_params = {
        slice_into_random_beats: {"bpm": BPM},
        slice_by_transients: {"bpm": BPM, "delta": 0.5, "min_length_seconds": 0.5}
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

    print(f"[DEBUG] Selected segments count: {len(selected_segments)}")
    for i, seg in enumerate(selected_segments):
        print(f"[DEBUG] Segment {i} shape: {seg.shape}, dtype: {seg.dtype}, min: {seg.min() if seg.size else 'empty'}, max: {seg.max() if seg.size else 'empty'}")


    frankenstem_audio = np.concatenate(selected_segments, axis=1 if selected_segments[0].ndim == 2 else 0)
    print(f"[PROFILE] Concatenation took: {time.time() - concat_time:.2f}s") ###DEBUG
    print(f"[PROFILE] Total Frankenstem generation time: {time.time() - start_time:.2f}s") ##DEBUG
    timestamp = datetime.now().strftime("%m%d_%H%M")
    stem_names = "_".join(stem_type.name.capitalize() for stem_type in selected_stem_types)
    slice_type_name = (
        "Transient" if selected_slicing_function == slice_by_transients else
        "Beat" if selected_slicing_function == slice_into_random_beats else
        "UnknownSliceType"
    )
    duration_str = f"{int(TARGET_DURATION_SECONDS)}s"

    output_file = (
        f"{OUTPUT_PATH}/{stem_names}_{slice_type_name}_{duration_str}_{timestamp}.wav"
    )


    # Transpose to correct shape for stereo output
    frankenstem_audio = frankenstem_audio.T  # (N, 2)

    print(f"[INFO] Frankenstem length: {len(frankenstem_audio)/sr:.3f}s "
        f"(target: {TARGET_DURATION_SECONDS}s, segments used: {len(selected_segments)})")

    sf.write(output_file, frankenstem_audio, sr)
    print(f"Saved Frankenstem to {output_file}")


if __name__ == "__main__":
    config = FrankenstemConfig(
        target_duration=30,  # seconds
        bpm=160,
        selected_stem_types=[StemType.DRUMS, StemType.BASS],
        selected_slicing_function=slice_by_transients
    )
    generate_frankenstem(config)
