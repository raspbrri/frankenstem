from enum import Enum

class StemType(Enum):
    VOCALS = "Vocals"
    DRUMS = "Drums"
    BASS = "Bass"
    OTHER = "Other"

class Stem:
    def __init__(self, song_name: str, stem_type: StemType, filepath: str):
        self.song_name = song_name
        self.stem_type = stem_type
        self.filepath = filepath
        self._audio = None
        self._sr = None

    def load_audio(self): #prevents loading audio multiple times
        if self._audio is None:
            self._audio, self._sr = load_audio(self.filepath)
        return self._audio, self._sr

class Song:
    def __init__(self, name: str):
        self.name = name
        self.stems = {}  # Dict[StemType, Stem]

    def add_stem(self, stem: Stem):
        if stem.stem_type in self.stems:
            raise ValueError(f"Duplicate stem type '{stem.stem_type}' in song '{self.name}'")
        self.stems[stem.stem_type] = stem

    def get_stem(self, stem_type: StemType):
        return self.stems.get(stem_type)

    @property
    def available_stem_types(self):
        return list(self.stems.keys())

    def has_stems(self, required_types: list[StemType]):
        return all(t in self.stems for t in required_types)