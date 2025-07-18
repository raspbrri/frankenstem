import numpy as np
import librosa

def compute_energy(audio):
    """
    Computes RMS energy of a mono or stereo audio segment.
    """
    if audio.ndim == 2:
        audio = np.mean(audio, axis=0)  # convert to mono

    return np.sqrt(np.mean(audio**2))


def filter_segments_by_energy(segments, target='low'):
    """
    Filters segments by RMS energy, using the median as threshold.
    Returns segments that are either 'low' or 'high' energy.
    """
    scores = [compute_energy(seg) for seg in segments]

    mean_score = np.mean(scores)
    std_score = np.std(scores)
    median_score = np.median(scores)
    print(f"[DEBUG] Energy mean: {mean_score:.5f}, median: {median_score:.5f}")
    threshold = None

    # make a map to handle different energy targets

    if target == 'low':
        threshold = mean_score - 2 * std_score
        filtered = [seg for seg, score in zip(segments, scores) if score < threshold]
    elif target == 'very_low':
        threshold = mean_score - 1.5 * std_score
        filtered = [seg for seg, score in zip(segments, scores) if score < threshold]
    elif target == 'medium':
        lower = mean_score - std_score
        upper = mean_score + std_score
        filtered = [seg for seg, score in zip(segments, scores) if lower <= score <= upper]
        print(f"[DEBUG] Energy medium range: {lower:.5f} to {upper:.5f}")
    elif target == 'high':
        threshold = mean_score + std_score
        filtered = [seg for seg, score in zip(segments, scores) if score > threshold]
    else:
        raise ValueError("target must be 'low', 'very_low', 'medium' or 'high'")

    print(f"[INFO] Filtered down to {len(filtered)} of {len(segments)} segments.")
    return filtered
