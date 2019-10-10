import chordparser as cp
import chordparser.scales as scales
import pytest


@pytest.mark.parametrize(
    "mode, intervals", [
         ("ionian", (2, 2, 1, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 1)),
         ("major", (2, 2, 1, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 1)),
         ("dorian", (2, 1, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 1, 2)),
         ("phrygian", (1, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 1, 2, 2)),
         ("lydian", (2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 1, 2, 2, 1)),
         ("mixolydian", (2, 2, 1, 2, 2, 1, 2, 2, 2, 1, 2, 2, 1, 2)),
         ("aeolian", (2, 1, 2, 2, 1, 2, 2, 2, 1, 2, 2, 1, 2, 2)),
         ("minor", (2, 1, 2, 2, 1, 2, 2, 2, 1, 2, 2, 1, 2, 2)),
         ("locrian", (1, 2, 2, 1, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2)),
         ]
    )
def test_scale_modes(mode, intervals):
    scale = scales.Scale('C', mode)
    string = (
        f'Scale intervals for {mode} are incorrect. '
        + f'Expected {intervals} but got {scale.intervals} instead'
        )
    assert scale.intervals == intervals, string


def test_scale_modes_fake():
    with pytest.raises(scales.ModeError):
        scales.Scale('C', "ionia")


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
    string = (
        f'Scale intervals for {key} are incorrect. '
        + f'Expected {note_order} but got {scale._note_order} instead'
        )
    assert scale._note_order == note_order, string


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
            'G\u266d', 'A\u266d', 'B\U0001D12B', 'C\u266d', 'D\u266d', 'E\u266d', 'F\u266d',
            'G\u266d', 'A\u266d', 'B\U0001D12B', 'C\u266d', 'D\u266d', 'E\u266d', 'F\u266d')),
        ])
def test_scale_notes(key, mode, notes):
    scale = scales.Scale(key, mode)
    string = (
        f'Scale intervals for {key} {mode} are incorrect. '
        + f'Expected {notes} but got {scale.notes} instead'
        )
    assert scale.notes == notes, string
