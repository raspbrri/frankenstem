import librosa
import numpy as np
from frankenstem.removing_silence import remove_silence
import random

def slice_into_random_beats(audio, sr, bpm, min_beats=8, max_beats=10):
    """
    Splice an audio signal into random beat-length segments using beat tracking.
    Works with mono or stereo, returns stereo if input is stereo. 
    """

    # Remove silence BEFORE analysis for stability
    audio = remove_silence(audio, sr, bpm)

    # If stereo, create mono mix for beat analysis
    if audio.ndim == 2:
        analysis_audio = np.mean(audio, axis=0)
    else:
        analysis_audio = audio

    tempo, beat_frames = librosa.beat.beat_track(y=analysis_audio, sr=sr, bpm=bpm, units='frames')
    beat_boundaries = librosa.frames_to_samples(beat_frames)

    segments = []
    i = 0

    while i < len(beat_boundaries) - min_beats:
        n_beats = random.randint(min_beats, max_beats)
        start = beat_boundaries[i]
        end = beat_boundaries[min(i + n_beats, len(beat_boundaries) - 1)]

        if audio.ndim == 2:
            segment = audio[:, start:end]  # preserve stereo
        else:
            segment = audio[start:end]

        segments.append(segment)
        i += n_beats

    return segments


def slice_by_transients(audio, sr, bpm, delta=0.05, min_length_seconds=0.5, hop_length=512, backtrack=True):
    """
    Splits audio at transient (onset) points using librosa's onset detection.
    Works with mono or stereo, returns stereo if input is stereo.
    """

    # Remove silence
    audio = remove_silence(audio, sr, bpm)

    # If stereo, create mono mix for onset detection
    if audio.ndim == 2:
        analysis_audio = np.mean(audio, axis=0)
    else:
        analysis_audio = audio

    onset_frames = librosa.onset.onset_detect(
        y=analysis_audio,
        sr=sr,
        hop_length=hop_length,
        backtrack=backtrack,
        delta=delta
    )
    onset_samples = librosa.frames_to_samples(onset_frames, hop_length=hop_length)
    onset_samples = np.append(onset_samples, len(analysis_audio))

    min_length_samples = int(min_length_seconds * sr)
    segments = []

    for start, end in zip(onset_samples[:-1], onset_samples[1:]):
        if (end - start) >= min_length_samples:
            if audio.ndim == 2:
                segment = audio[:, start:end]  # preserve stereo
            else:
                segment = audio[start:end]
            segments.append(segment)

    return segments





