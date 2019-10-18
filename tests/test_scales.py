import chordparser.scales as scales
import chordparser.notes as notes
import pytest


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
    nkey = notes.Key('D', mode=mode, submode=submode)
    scale = scales.Scale(nkey)
    assert scale.scale_intervals == intervals


@pytest.mark.parametrize(
    "key", ["A", "C\u266f", "D\u266d", "B\U0001D12B", "F\U0001D12A"])
def test_scale_keys(key):
    nkey = notes.Key(key)
    new_scale = scales.Scale(nkey)
    assert new_scale.key == notes.Key(key)


@pytest.mark.parametrize(
    "key", [1, True, len])
def test_scale_keys_typeerror(key):
    with pytest.raises(TypeError):
        scales.Scale(key)


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
    nkey = notes.Key(key)
    scale = scales.Scale(nkey)
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
    nkey = notes.Key(key, mode=mode)
    scale = scales.Scale(nkey)
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
    nkey = notes.Key(key, mode=mode, submode=submode)
    scale = scales.Scale(nkey)
    assert scale.notes == note


@pytest.mark.parametrize(
    "value", [
        "H#", 10.0, "Z", len])
def test_scale_transpose_error(value):
    nkey = notes.Key('C')
    new_scale = scales.Scale(nkey)
    with pytest.raises(TypeError):
        new_scale.transpose(value)


@pytest.mark.parametrize(
    "key, value, new_key", [
        ('C', 3, 'D\u266f'),
        ('D', -5, 'A'),
        ('G', 12, 'G')])
def test_scale_transpose_sharps(key, value, new_key):
    nkey = notes.Key(key)
    new_scale = scales.Scale(nkey)
    new_scale.transpose(value)
    assert new_scale.key == notes.Key(new_key)


@pytest.mark.parametrize(
    "key, value, new_key", [
        ('C', 3, 'E\u266d'),
        ('D', -4, 'B\u266d')])
def test_scale_transpose_flats(key, value, new_key):
    nkey = notes.Key(key)
    new_scale = scales.Scale(nkey)
    new_scale.transpose(value, use_flats=True)
    assert new_scale.key == notes.Key(new_key)
