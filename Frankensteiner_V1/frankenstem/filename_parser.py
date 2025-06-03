from frankenstem.classes import Stem, StemType, Song


def load_stems_from_folder(input_path):
    input_path = Path(input_path)
    stems_by_name = {}

    for file in input_path.glob("*.wav"):
        try:
            song_name, ste