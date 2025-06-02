import librosa
import numpy as np
import random 

def splice_into_random_beats(audio, sr, bpm, min_beats=2, max_beats=4):
    """
    Splice an audio signal into random 2-4 beat segments using beat tracking.
    Returns a list of audio arrays containing the segments
    """

    tempo, beat_frames = librosa.beat.beat_track(y=audio, sr=sr, bpm=bpm, units = 'frames')
    beat_samples = librosa.frames_to_samples(beat_frames)

    segments = []
    i = 0
    while i < len(beat_samples) - min_beats:
        n_beats = random.randint(min_beats, max_beats) # randomly choose number of beats for segment
        start = beat_samples[i] # start of the segment in the audio file
        end = beat_samples[min(i + n_beats, len(beat_samples) - 1)] 
        segment = audio[start:end]
        segments.append(segment) #adds the current segment to the list
        i += n_beats # adds the number of beats to the index to move to the next segment

    return segments




