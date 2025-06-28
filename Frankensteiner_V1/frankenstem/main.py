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

INPUT_PATH = "input"
OUTPUT_PATH = "output"

def generate_frankenstem(config: FrankenstemConfig):
    TARGET_DURATION_SECONDS = config.target_duration
    BPM = config.bpm
    selected_stem_types = config.selected_stem_types
    selected_slicing_function = config.selected_slicing_function

    if not os.path.exists(INPUT_PATH):
        raise FileNotFoundError(f"Input path '{INPUT_PATH}' does not exist.")
    if not os.path.exists(OUTPUT_PATH):
        os.makedirs(OUTPUT_PATH)

    stem_wavs = load_wavs_from_folder(INPUT_PATH)

    slice_params = {
        slice_into_random_beats: {"bpm": BPM},
        slice_by_transients: {"bpm": BPM, "delta": 0.01, "min_length_seconds": 0.5}
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

    if len(all_segments) == 0:
        raise ValueError("No valid segments found for selected stem types.")

    random.shuffle(all_segments)

    ### NEED TO FIX THIS SECTION TO PROPERLY ESTIMATE SEGMENT COUNT BASED ON BPM AND TARGET DURATION
    beats_per_second = BPM / 60
    seconds_per_segment = 2  # average 2 beats per segment
    estimated_segment_duration = seconds_per_segment / beats_per_second
    num_segments = int(TARGET_DURATION_SECONDS / estimated_segment_duration)

    selected_segments = all_segments[:num_segments]

    frankenstem_audio = np.concatenate(selected_segments)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M")
    stem_names = "_".join(stem_type.name.capitalize() for stem_type in selected_stem_types)
    output_file = f"{OUTPUT_PATH}/FRANKENSTEM_{stem_names}_{timestamp}.wav"

    sf.write(output_file, frankenstem_audio, sr)
    print(f"Saved Frankenstem to {output_file}")

if __name__ == "__main__":
    config = FrankenstemConfig(
        target_duration=20,  # seconds
        bpm=130,
        selected_stem_types=[StemType.VOCALS, StemType.OTHER],
        selected_slicing_function=slice_into_random_beats
    )
    generate_frankenstem(config)
