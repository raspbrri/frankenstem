import librosa
import numpy as np
from frankenstem.removing_silence import remove_silence
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

def slice_by_transients(audio, sr, bpm, delta=0.005, min_length_seconds=2.0, hop_length=512, backtrack=True):
    """
    Splits audio at transient (onset) points using librosa's onset detection.

    Parameters:
    - audio: np.ndarray, audio signal
    - sr: int, sample rate
    - delta: float, sensitivity for onset detection (lower = more sensitive)
    - min_length_seconds: float, minimum length of a fragment in seconds
    - hop_length: int, hop length for analysis
    - backtrack: bool, adjust onsets backward to local minima for cleaner cuts

    Returns:
    - segments: List of np.ndarray audio fragments
    """

    # Detect onsets
    onset_frames = librosa.onset.onset_detect(y=audio, sr=sr, hop_length=hop_length, backtrack=backtrack, delta=delta)
    onset_samples = librosa.frames_to_samples(onset_frames, hop_length=hop_length)

    # Ensure the last sample is included
    onset_samples = np.append(onset_samples, len(audio))

    min_length_samples = int(min_length_seconds * sr)
    segments = []

    audio = remove_silence(audio, sr, bpm)

    for start, end in zip(onset_samples[:-1], onset_samples[1:]):
        if (end - start) >= min_length_samples:
            segment = audio[start:end]
            segments.append(segment)

    return segments




