import librosa
import numpy as np
import random

def remove_silence(audio, sr, bpm, silence_thresh_db=-40):
    """
    Remove silence from the audio signal using beat-aligned chunking.

    Parameters:
    - audio: np.ndarray, mono or stereo audio
    - sr: sample rate
    - bpm: tempo for beat tracking
    - silence_thresh_db: threshold in dB below which to consider silence

    Returns:
    - np.ndarray of audio with silence removed, preserves stereo if input is stereo
    """

    # Create mono mix for beat tracking
    if audio.ndim == 2:
        analysis_audio = np.mean(audio, axis=0)
    else:
        analysis_audio = audio

    tempo, beat_frames = librosa.beat.beat_track(y=analysis_audio, sr=sr, bpm=bpm, units='frames')
    beat_boundaries = librosa.frames_to_samples(beat_frames)

    clean_audio = []
    subwindow_size = int(sr * 0.1)  # 100 ms subwindows

    i = 0
    while i < len(beat_boundaries) - 1:
        start = beat_boundaries[i]
        end = beat_boundaries[i + 1]

        # Slice original audio preserving stereo
        if audio.ndim == 2:
            segment = audio[:, start:end]
            subwindows = [segment[:, j:j + subwindow_size] for j in range(0, segment.shape[1], subwindow_size)]
            peak_amplitudes = [np.max(np.abs(subwindow)) for subwindow in subwindows if subwindow.shape[1] > 0]
        else:
            segment = audio[start:end]
            subwindows = [segment[j:j + subwindow_size] for j in range(0, len(segment), subwindow_size)]
            peak_amplitudes = [np.max(np.abs(subwindow)) for subwindow in subwindows if len(subwindow) > 0]

        # Compute peak dB safely
        if peak_amplitudes:
            peak_db = 20 * np.log10(np.max(peak_amplitudes) + 1e-6)  # avoid log(0)
        else:
            peak_db = -np.inf

        if peak_db > silence_thresh_db:
            clean_audio.append(segment)

        i += 1

    if clean_audio:
        # Concatenate along time axis
        if audio.ndim == 2:
            return np.concatenate(clean_audio, axis=1)
        else:
            return np.concatenate(clean_audio)
    else:
        print("[WARNING] Silence removal returned empty output.")
        return np.zeros((audio.shape[0], 0)) if audio.ndim == 2 else np.array([])

   

