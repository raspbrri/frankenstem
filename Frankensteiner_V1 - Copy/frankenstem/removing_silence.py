import librosa
import numpy as np
import random 

def remove_silence(audio, sr, bpm, silence_thresh_db=-40):
    """
    Remove silence from the audio signal based on a threshold.
    
    Parameters:
    - audio: numpy array of audio samples
    - sr: sample rate of the audio
    - threshold: amplitude threshold below which audio is considered silence
    
    Returns:
    - numpy array of audio with silence removed
    """

    tempo, beat_frames = librosa.beat.beat_track(y=audio, sr=sr, bpm=bpm, units = 'frames')
    beat_boundaries = librosa.frames_to_samples(beat_frames)

    clean_audio = []
    subwindow_size = int(sr * 0.1)  # 100 ms subwindows
    i = 0

    while i < len(beat_boundaries) - 1:
        start = beat_boundaries[i]
        end = beat_boundaries[i + 1]
        segment = audio[start:end]

        # divide the segment into subwindows and compute peak amplitude for each subwindow
        subwindows = [segment[j:j + subwindow_size] for j in range(0, len(segment), subwindow_size)]
        peak_amplitudes = [np.max(np.abs(subwindow)) for subwindow in subwindows if len(subwindow) > 0]
        peak_db = 20 * np.log10(np.max(peak_amplitudes) + 1e-6) #convert to db and avoid log(0)

        # append to clean_audio if peak amplitude is above the silence threshold
        if peak_db > silence_thresh_db:
            clean_audio.append(segment)
        i += 1

    return np.concatenate(clean_audio) if clean_audio else np.array([])

