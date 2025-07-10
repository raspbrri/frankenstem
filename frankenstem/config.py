from dataclasses import dataclass
from frankenstem.classes import StemType

@dataclass
class FrankenstemConfig:
    target_duration: float
    bpm: float
    selected_stem_types: list[StemType]
    selected_slicing_function: callable
