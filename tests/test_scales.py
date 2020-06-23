from chordparser import scales
from chordparser import keys_editor
from chordparser import scales_editor
import pytest


KE = keys_editor.KeyEditor()
SE = scales_editor.ScaleEditor()


@pytest.mark.parametrize(
    "mode, submode, intervals", [
         ("ionian", None, (2, 2, 1, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 1)),
         ("MAJOR", None, (2, 2, 1, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 1)),
         ("dorian", None, (2, 1, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 1, 2)),
         ("PhRyGiAn", None, (1, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 1, 2, 2)),
         ("lydian", None, (2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 1, 2, 2, 1)),
         ("mixolydian", None, (2, 2, 1, 2, 2, 1, 2, 2, 2, 1, 2, 2, 1, 2)),
         ("aeolian", None, (2, 1, 2, 2, 1, 2, 2, 2, 1, 2, 2, 1, 2, 2)),
         ("minor", None, (2, 1, 2, 2, 1, 2, 2, 2, 1, 2, 2, 1, 2, 2)),
         ("minor", "natural", (2, 1, 2, 2, 1, 2, 2, 2, 1, 2, 2, 1, 2, 2)),
         ("minor", "melodic", (2, 1, 2, 2, 2, 2, 1, 2, 1, 2, 2, 2, 2, 1)),
         ("minor", "harmonic", (2, 1, 2, 2, 1, 3, 1, 2, 1, 2, 2, 1, 3, 1)),
         ("locrian", None, (1, 2, 2, 1, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2)),
         ]
    )
def test_scale_modes(mode, submode, intervals):
    nkey = KE.create_key('D', mode=mode, submode=submode)
    scale = SE.create_scale(nkey)
    assert scale.scale_intervals == intervals


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
    nkey = KE.create_key(key)
    scale = SE.create_scale(nkey)
    assert scale._note_order == note_order


@pytest.mark.parametrize(
    "key, mode, note", [
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
def test_scale_notes(key, mode, note):
    nkey = KE.create_key(key, mode=mode)
    scale = SE.create_scale(nkey)
    assert scale.notes == note


@pytest.mark.parametrize(
    "key, mode, submode, note", [
        ('C', 'minor', 'natural', (
            'C', 'D', 'E\u266d', 'F', 'G', 'A\u266d', 'B\u266d',
            'C', 'D', 'E\u266d', 'F', 'G', 'A\u266d', 'B\u266d',)),
        ('C', 'minor', 'harmonic', (
            'C', 'D', 'E\u266d', 'F', 'G', 'A\u266d', 'B',
            'C', 'D', 'E\u266d', 'F', 'G', 'A\u266d', 'B',)),
        ('C', 'minor', 'melodic', (
            'C', 'D', 'E\u266d', 'F', 'G', 'A', 'B',
            'C', 'D', 'E\u266d', 'F', 'G', 'A', 'B',)),
        ])
def test_scale_submode_notes(key, mode, submode, note):
    nkey = KE.create_key(key, mode=mode, submode=submode)
    scale = SE.create_scale(nkey)
    assert scale.notes == note


def test_scale_transpose_sharps():
    nkey = KE.create_key("D")
    new_scale = SE.create_scale("C")
    new_scale.transpose(2, 1)
    assert new_scale.key == nkey


def test_scale_repr():
    new_scale = SE.create_scale('C', 'minor', 'harmonic')
    assert repr(new_scale) == "C harmonic minor scale"


def test_scale_equality():
    s = SE.create_scale('C', 'dorian')
    assert s == SE.create_scale('C', 'dorian')


def test_scale_not_implemented():
    s = SE.create_scale('C')
    assert s != len
