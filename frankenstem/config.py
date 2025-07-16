from dataclasses import dataclass
from frankenstem.classes import StemType

@dataclass
class FrankenstemConfig:
    target_duration: float
    bpm: float
    selected_stem_types: list[StemType]
    selected_slicing_function: callable
    min_beats: int = 4
    max_beats: int = 8
    export_fragments_individually: bool = False


    def __post_init__(self):
        if self.min_beats >= self.max_beats:
            raise ValueError("min_beats must be less than max_beats")
