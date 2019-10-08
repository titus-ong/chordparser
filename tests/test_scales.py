import chordparser as cp
import pytest


@pytest.mark.parametrize(
    "mode, intervals", [
         ("ionian", (2, 2, 1, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 1)),
         ("dorian", (2, 1, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 1, 2)),
         ("phrygian", (1, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 1, 2, 2)),
         ("lydian", (2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 1, 2, 2, 1)),
         ("mixolydian", (2, 2, 1, 2, 2, 1, 2, 2, 2, 1, 2, 2, 1, 2)),
         ("aeolian", (2, 1, 2, 2, 1, 2, 2, 2, 1, 2, 2, 1, 2, 2)),
         ("locrian", (1, 2, 2, 1, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2)),
         ]
    )
def test_scale_modes(mode, intervals):
    scale = cp.scales.Scale(mode)
    assert scale.intervals == intervals, "Scale intervals are incorrect"


def test_scale_modes_fake():
    with pytest.raises(cp.scales.ModeError):
        cp.scales.Scale("ionia")
