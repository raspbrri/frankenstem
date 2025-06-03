import re
from frankenstem.classes import Stem, StemType, Song

def parse_filename(filename):
    # Expecting format: "Song_Name (StemType).wav"
    match = re.match(r"^(.*) \(([^)]+)\)\.wav$", filename, re.IGNORECASE)
    if not match:
        raise ValueError("Filename does not match expected format 'Song Name (StemType).wav'")

    song_name = match.group(1).strip()
    raw_stem_type = match.group(2).strip().lower()

    # Map the raw stem type string to the enum
    stem_map = {
        "Vocals": StemType.VOCALS,
        "Drums": StemType.DRUMS,
        "Bass": StemType.BASS,
        "Other": StemType.OTHER
    }

    if raw_stem_type not in stem_map:
        raise ValueError(f"Unrecognized stem type '{raw_stem_type}'")

    return song_name, stem_map[raw_stem_type]


def load_songs_from_folder(input_path):
    input_path = Path(input_path)
    songs_by_name = {}

    for filepath in input_path.glob("*.wav"):
        try:
            song_name, stem_type = parse_filename(filepath.name)
            stem = Stem(song_name, stem_type, str(filepath))
            song = songs_by_name.setdefault(song_name, Song(song_name))
            song.add_stem(stem)
        except ValueError as e:
            print(f"Skipping '{filepath.name}': {e}")
            continue

    # make sure that there are at least two distinct songs with stems
    songs = list(songs_by_name.values()) 
    if len(songs) < 2:
        raise ValueError("At least two distinct songs with stems are required.")

    return songs





