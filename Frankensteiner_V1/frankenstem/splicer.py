import librosa
import numpy as n
from frankenstem.remove_silence_to_beat import remove_silence
import random

def slice_into_random_beats(audio, sr, bpm, min_beats=2, max_beats=4):
    """
    Splice an audio signal into random 2-4 beat segments using beat tracking.
    Returns a list of audio arrays containing the segments
    """

    tempo, beat_frames = librosa.beat.beat_track(y=audio, sr=sr, bpm=bpm, units = 'frames')
    beat_boundaries = librosa.frames_to_samples(beat_frames) #an array of sample indices where beats occur

    segments = []
    i = 0

    # remove silence from the audio signal
    audio = remove_silence(audio, sr, bpm)

    while i < len(beat_boundaries) - min_beats:
        n_beats = random.randint(min_beats, max_beats) # randomly choose number of beats for segment
        start = beat_boundaries[i] # start of the segment in the audio file
        end = beat_boundaries[min(i + n_beats, len(beat_boundaries) - 1)] 
        segment = audio[start:end]
        segments.append(segment) #adds the current segment to the list
        i += n_beats # adds the number of beats to the index to move to the next segment

    return segments




