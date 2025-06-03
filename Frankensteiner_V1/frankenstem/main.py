from frankenstem.audio_io import load_audio
from frankenstem.splicer import slice_into_random_beats
from frankenstem.combiner import combine_segments
from frankenstem.removing_silence import remove_silence
from frankenstem.parser.file_parser import load_songs_from_folder
import soundfile as sf
from datetime import datetime
import numpy as np

input_path = "Frankensteiner_V1/input"
songs = load_songs_from_folder(input_path)

timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
OUTPUT_PATH = f"output/frankenstem_vocals_{timestamp}.wav"

# BPM assumed same for all songs - ADD CODE LATER TO ASK USER FOR BPM
BPM = 130

# Load audio - ADD CODE LATER TO AUTOMATICALLY DO ALL OF THESE THINGS FOR EACH SONG
audio_a, sr = load_audio(AUDIO_PATH_A)
audio_b, _  = load_audio(AUDIO_PATH_B)

# Slice each into beat segments (2–4 beat chunks)
segments_a = slice_into_random_beats(audio_a, sr, BPM)
segments_b = slice_into_random_beats(audio_b, sr, BPM)

print(f"{len(segments_a)} segments from Song A")
print(f"{len(segments_b)} segments from Song B")

#combine segments from both songs into a single audio array
combined_segments = combine_segments(segments_a, segments_b, sr=sr)
frankenstem_audio = np.concatenate(combined_segments)

# Save the combined audio to a file
sf.write(OUTPUT_PATH, frankenstem_audio, sr)
print(f"Frankenstem audio saved to {OUTPUT_PATH}")


