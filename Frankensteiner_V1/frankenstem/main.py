from frankenstem.audio_io import load_audio
from frankenstem.splicer import slice_into_random_beats
from frankenstem.combiner import combine_segments
import numpy as np
from datetime import datetime
import soundfile as sf

# Paths to two stems of the same type (e.g. vocals)
AUDIO_PATH_A = "input/Song_A (Vocals).wav"
AUDIO_PATH_B = "input/Song_B (Vocals).wav"
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
OUTPUT_PATH = f"output/frankenstem_vocals_{timestamp}.wav"

# BPM assumed same for both songs
BPM = 130

# Load audio
audio_a, sr = load_audio(AUDIO_PATH_A)
audio_b, _  = load_audio(AUDIO_PATH_B)

# remove silence from the audio files


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


