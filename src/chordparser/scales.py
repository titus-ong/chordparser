"""
Basis of chords. Only diatonic scales are included.
"""
from general import Error


class ModeError(Error):
    pass


class Scale:
    _heptatonic_base = (2, 2, 1, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 1)
    _SCALES = {
        "ionian": 0,
        "dorian": 1,
        "phrygian": 2,
        "lydian": 3,
        "mixolydian": 4,
        "aeolian": 5,
        "locrian": 6,
        }

    def __init__(mode="ionian"):
        self.mode = mode
        self.intervals = _get_scale_intervals()

    def _get_scale_intervals(self):
        try:
            shift = _SCALES[self.mode.lower()]
        except KeyError:
            raise ModeError("Mode cannot be found")
        scale_intervals = _heptatonic_base[shift:] + _heptatonic_base[:shift]
        return scale_intervals
