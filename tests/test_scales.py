import chordparser.scales as scales
import pytest


@pytest.mark.parametrize(
    "mode, intervals", [
         ("ionian", (2, 2, 1, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 1)),
         ("MAJOR", (2, 2, 1, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 1)),
         ("dorian", (2, 1, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 1, 2)),
         ("PhRyGiAn", (1, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 1, 2, 2)),
         ("lydian", (2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 1, 2, 2, 1)),
         ("mixolydian", (2, 2, 1, 2, 2, 1, 2, 2, 2, 1, 2, 2, 1, 2)),
         ("aeolian", (2, 1, 2, 2, 1, 2, 2, 2, 1, 2, 2, 1, 2, 2)),
         ("minor", (2, 1, 2, 2, 1, 2, 2, 2, 1, 2, 2, 1, 2, 2)),
         ("locrian", (1, 2, 2, 1, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2)),
         ]
    )
def test_scale_modes(mode, intervals):
    scale = scales.Scale('C', mode)
    assert scale.intervals == intervals

@pytest.mark.parametrize(
    "mode", ["ionia", 1, True])
def test_scale_modes_fake(mode):
    with pytest.raises(scales.ModeError):
        scales.Scale('C', mode)


@pytest.mark.parametrize(
    "key, note_order", [
        ('C', ('C', 'D', 'E', 'F', 'G', 'A', 'B',
               'C', 'D', 'E', 'F', 'G', 'A', 'B')),
        ('D', ('D', 'E', 'F', 'G', 'A', 'B', 'C',
               'D', 'E', 'F', 'G', 'A', 'B', 'C')),
        ('E', ('E', 'F', 'G', 'A', 'B', 'C', 'D',
               'E', 'F', 'G', 'A', 'B', 'C', 'D')),
        ('F', ('F', 'G', 'A', 'B', 'C', 'D', 'E',
               'F', 'G', 'A', 'B', 'C', 'D', 'E')),
        ('G', ('G', 'A', 'B', 'C', 'D', 'E', 'F',
               'G', 'A', 'B', 'C', 'D', 'E', 'F')),
        ('A', ('A', 'B', 'C', 'D', 'E', 'F', 'G',
               'A', 'B', 'C', 'D', 'E', 'F', 'G')),
        ('B', ('B', 'C', 'D', 'E', 'F', 'G', 'A',
               'B', 'C', 'D', 'E', 'F', 'G', 'A')),
        ]
    )
def test_scale_note_order(key, note_order):
    scale = scales.Scale(key)
    assert scale._note_order == note_order


@pytest.mark.parametrize(
    "key, mode, notes", [
        ('C', 'major', (
            'C', 'D', 'E', 'F', 'G', 'A', 'B',
            'C', 'D', 'E', 'F', 'G', 'A', 'B')),
        ('C\u266f', 'minor', (
            'C\u266f', 'D\u266f', 'E', 'F\u266f', 'G\u266f', 'A', 'B',
            'C\u266f', 'D\u266f', 'E', 'F\u266f', 'G\u266f', 'A', 'B')),
        ('F', 'mixolydian', (
            'F', 'G', 'A', 'B\u266d', 'C', 'D', 'E\u266d',
            'F', 'G', 'A', 'B\u266d', 'C', 'D', 'E\u266d')),
        ('G\u266d', 'dorian', (
            'G\u266d', 'A\u266d', 'B\U0001D12B',
            'C\u266d', 'D\u266d', 'E\u266d', 'F\u266d',
            'G\u266d', 'A\u266d', 'B\U0001D12B',
            'C\u266d', 'D\u266d', 'E\u266d', 'F\u266d')),
        ])
def test_scale_notes(key, mode, notes):
    scale = scales.Scale(key, mode)
    assert scale.notes == notes
