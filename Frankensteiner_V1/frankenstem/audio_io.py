import librosa

def load_audio(file_path):
    """
    Load an audio file  as a NumPy array using librosa.

    Returns: (audio_array, sample_rate)
    """

    audio, sr = librosa.load(file_path, sr=None, mono=True)
    return audio, sr
