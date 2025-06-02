from audio_io import load_audio
from splicer import splice_into_random_beats

# Paths to two stems of the same type (e.g. vocals)
AUDIO_PATH_A = "input/Song A (Vocals).wav"
AUDIO_PATH_B = "input/Song B (Vocals).wav"

# BPM assumed same for both songs
BPM = 100

# Load audio
audio_a, sr = load_audio(AUDIO_PATH_A)
audio_b, _  = load_audio(AUDIO_PATH_B)

# Slice each into beat segments (2–4 beat chunks)
segments_a = slice_into_random_beats(audio_a, sr, BPM)
segments_b = slice_into_random_beats(audio_b, sr, BPM)

print(f"{len(segments_a)} segments from Song A")
print(f"{len(segments_b)} segments from Song B")
