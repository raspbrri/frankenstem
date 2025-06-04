from frankenstem.audio_io import load_audio
from frankenstem.splicer import slice_into_random_beats
from frankenstem.combiner import combine_segments
from frankenstem.removing_silence import remove_silence
from frankenstem.filename_parser import load_songs_from_folder
from frankenstem.classes import StemType, Song
import soundfile as sf
from datetime import datetime
from collections import defaultdict
import numpy as np


timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
#OUTPUT_PATH = f"output/frankenstem_vocals_{timestamp}.wav"
OUTPUT_PATH = "output"

# BPM assumed same for all songs - ADD CODE LATER TO ASK USER FOR BPM
BPM = 132

#load audio files from the input folder and collect stem types
songs = load_songs_from_folder("input")

#dynamically detect stem types from the loaded audio files
present_stem_types = set()
for song in songs:
    present_stem_types.update(song.stems.keys())

print(f"Detected stem types: {[t.name for t in present_stem_types]}")

# organise and slice segments
segments_by_stemtype = defaultdict(list)

# groups present stem objects by their stem type - IMPOORTANT grouping for later combination modes
for stem_type in present_stem_types:
    matching_stems = []
    for song in songs:
        stem = song.get_stem(stem_type)
        if stem:
            matching_stems.append(stem)

    if len(matching_stems) < 2:
        print(f"Not enough stems of type {stem_type.name} found. Skipping this stem type.")
        continue

    for stem in matching_stems:
        audio, sr = stem.load_audio()
        segments = slice_into_random_beats(audio, sr, BPM)
        print(f"[DEBUG] {stem.filepath} → {len(segments)} segments")
        segments_by_stemtype[stem_type].append(segments)

# combine segments from different stem types.. (array of arrays

for stem_type, segment_lists in segments_by_stemtype.items():
    #for now limited to 2 segment arrays
    if not segment_lists[0] or not segment_lists[1]:
        print(f"[SKIP] Not enough segments to combine for {stem_type.name}")
        continue
    combined_segments = combine_segments(segment_lists[0], segment_lists[1], sr=sr)
    # frankenstem = concatentate segments from ^
    frankenstem_audio = np.concatenate(combined_segments)

    # write output to file (prefix 'Frankenstem', suffix timestamp + wav)

    output_file = f"{OUTPUT_PATH}/frankenstem_{stem_type.name.lower()}_{timestamp}.wav"
    sf.write(output_file, frankenstem_audio, sr)
    print(f"Saved frankenstem of type {stem_type.name} to {output_file}")

