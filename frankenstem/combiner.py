import librosa
import numpy as np
import random 

def combine_segments(segments_a, segments_b, sr=22050):
    """
    Combine segments from two lists of audio segments into a single list.
    Each segment is randomly chosen from either list, for  total audio length of 20 seconds.

    Returns a list of combined audio segments.
    """

    sources = {
        'a': segments_a,
        'b': segments_b
    }
    combined_segments = []
    total_length = 0
    max_length = 20 * sr  # 20 seconds at 22050 Hz (length in samples)

    while total_length < max_length:
        source = random.choice(list(sources.keys()))
        segment = random.choice(sources[source])
        remaining = max_length - total_length

        segment = segment if len(segment) <= remaining else segment[:remaining]
        combined_segments.append(segment)
        total_length += len(segment)
    
    return combined_segments
    
    