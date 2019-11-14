import chordparser.notes as notes
import pytest


@pytest.mark.parametrize(
    "note, expected", [
        ('C', 'C'), ('D\u266F', 'D\u266F'), ('G\u266D', 'G\u266D'),
        ('A\U0001D12B', 'A\U0001D12B'), ('B\U0001D12A', 'B\U0001D12A'),
        ('F#', 'F\u266F'), ('Eb', 'E\u266d'),
        ('Gbb', 'G\U0001D12B'), ('C##', 'C\U0001D12A'),
        ])
def test_note_creation_positive(note, expected):
    new_note = notes.Note(note)
    assert new_note.value == expected


@pytest.mark.parametrize(
    "note", [True, 1, len, [], ()])
def test_note_creation_typeerror(note):
    with pytest.raises(TypeError):
        new_note = notes.Note(note)


@pytest.mark.parametrize(
    "note", ['CA', 'D\u266F\u266F', '\u266DG', '\U0001D12A', 'F###'])
def test_note_creation_valueerror(note):
    with pytest.raises(ValueError):
        new_note = notes.Note(note)


@pytest.mark.parametrize(
    "accidental", ['CA', 'D\u266F', 2.0])
def test_note_accidental_negative(accidental):
    new_note = notes.Note('C')
    with pytest.raises(TypeError):
        new_note.accidental(accidental)


@pytest.mark.parametrize(
    "accidental, note", [
        (-2, 'C\U0001D12B'), (-1, 'C\u266d'),
        (0, 'C'), (1, 'C\u266f'), (2, 'C\U0001D12A')])
def test_note_accidental_positive(accidental, note):
    new_note = notes.Note('C')
    new_note.accidental(accidental)
    assert new_note.value == note


@pytest.mark.parametrize(
    "shift", ['CA', 'D\u266F', 2.0, len, [], ()])
def test_note_shift_negative(shift):
    new_note = notes.Note('C')
    with pytest.raises(TypeError):
        new_note.shift(shift)


@pytest.mark.parametrize(
    "shift", [300, -10, 3, -3])
def test_note_shift_negative(shift):
    new_note = notes.Note('C')
    with pytest.raises(ValueError):
        new_note.shift(shift)


@pytest.mark.parametrize(
    "shift, note", [
        (-2, 'C\U0001D12B'), (-1, 'C\u266d'),
        (0, 'C'), (1, 'C\u266f'), (2, 'C\U0001D12A')])
def test_note_shift_positive(shift, note):
    new_note = notes.Note('C')
    new_note.shift(shift)
    assert new_note.value == note


@pytest.mark.parametrize(
    "note, value", [
        ('C', 0), ('D\u266F', 3), ('G\u266D', 6),
        ('A\U0001D12B', 7), ('B\U0001D12A', 1)])
def test_note_num_value(note, value):
    new_note = notes.Note(note)
    assert new_note.num_value() == value


@pytest.mark.parametrize(
    "note", ['C', 'D\u266F', 'G\u266D', 'A\U0001D12B', 'B\U0001D12A'])
def test_note_letter(note):
    new_note = notes.Note(note)
    assert new_note.letter() == note[0]


@pytest.mark.parametrize(
    "note", ['C', 'D\u266F', 'G\u266D', 'A\U0001D12B', 'B\U0001D12A'])
def test_note_letter(note):
    new_note = notes.Note(note)
    if len(note) > 1:
        symbol = note[1]
    else:
        symbol = note[0]
    assert new_note.symbol() == symbol


@pytest.mark.parametrize(
    "note, value", [
        ('C', 0), ('D\u266F', 1), ('G\u266D', -1),
        ('A\U0001D12B', -2), ('B\U0001D12A', 2)])
def test_note_letter(note, value):
    new_note = notes.Note(note)
    if len(note) > 1:
        symbol = note[1]
    else:
        symbol = note[0]
    assert new_note.symbolvalue() == value


@pytest.mark.parametrize(
    "note", ['C', 'D\u266F', 'G\u266D', 'A\U0001D12B', 'B\U0001D12A'])
def test_note_creation_repr(note):
    new_note = notes.Note(note)
    assert repr(new_note) == note


@pytest.mark.parametrize(
    "note", ['C', notes.Note('C')])
def test_note_equality(note):
    new_note = notes.Note('C')
    assert new_note == note


@pytest.mark.parametrize(
    "note", ['CA', notes.Note('D'), True, 10])
def test_note_inequality(note):
    new_note = notes.Note('C')
    assert new_note != note


@pytest.mark.parametrize(
    "note, value, new_note", [
        ('C', 2, 'D'), ('G\u266d', -5, 'C\u266f'), ('A\U0001D12A', 1, 'C')])
def test_note_transpose_sharps(note, value, new_note):
    nnote = notes.Note(note)
    nnote.transpose(value)
    assert nnote == new_note


@pytest.mark.parametrize(
    "note, value, new_note", [
        ('C', -2, 'B\u266d'), ('F\u266f', -5, 'D\u266d'), ('F', -2, 'E\u266d')])
def test_root_transpose_flat(note, value, new_note):
    nnote = notes.Note(note)
    nnote.transpose(value, use_flats=True)
    assert nnote == new_note


@pytest.mark.parametrize(
    "value", [
        "H#", 10.0, "Z", len])
def test_root_transpose_error(value):
    nnote = notes.Note('C')
    with pytest.raises(TypeError):
        nnote.transpose(value)


@pytest.mark.parametrize(
    "key", [1, True, len, [], ()])
def test_keys_typeerror(key):
    with pytest.raises(TypeError):
        nkey = notes.Key(key)


@pytest.mark.parametrize(
    "key", ["ABC", "G\u266f\u266f", "H"])
def test_keys_valueerror(key):
    with pytest.raises(ValueError):
        nkey = notes.Key(key)


@pytest.mark.parametrize(
    "key, value, new_key", [
        ('C', 2, 'D'), ('G\u266d', -5, 'C\u266f'), ('A\U0001D12A', 1, 'C')])
def test_key_transpose_sharps(key, value, new_key):
    nkey = notes.Key(key)
    nkey.transpose(value)
    assert nkey.root == new_key


@pytest.mark.parametrize(
    "key, value, new_key", [
        ('C', -2, 'B\u266d'), ('F\u266f', -5, 'D\u266d'), ('F', -2, 'E\u266d')])
def test_key_transpose_flat(key, value, new_key):
    nkey = notes.Key(key)
    nkey.transpose(value, use_flats=True)
    assert nkey.root == new_key


@pytest.mark.parametrize(
    "value", [
        "H#", 10.0, "Z", len])
def test_key_transpose_error(value):
    nkey = notes.Key('C')
    with pytest.raises(TypeError):
        nkey.transpose(value)


@pytest.mark.parametrize(
    "mode, submode", [
        ("major", None), ("mInoR", None), ("MINOR", "harmonic"),
        ("minor", "melodic"), ("minor", "natural"), ("ionian", None),
        ("dorian", None), ("phrygian", None), ("lydian", None),
        ("mixolydian", None), ("aeolian", None), ("locrian", None)])
def test_key_mode_submode(mode, submode):
    nkey = notes.Key('C', mode=mode, submode=submode)
    if not submode:
        assert str(nkey) == f'C {mode.lower()}'
    else:
        assert str(nkey) == f'C {submode.lower()} {mode.lower()}'


@pytest.mark.parametrize(
    "mode", [1, True, len])
def test_key_mode_typeerror(mode):
    with pytest.raises(TypeError):
        nkey = notes.Key('C', mode)


@pytest.mark.parametrize(
    "mode", ["ionia", "hello", "1rh9"])
def test_key_mode_error(mode):
    with pytest.raises(KeyError):
        nkey = notes.Key('C', mode)


@pytest.mark.parametrize(
    "mode, submode", [("major", "harmonic"), ("minor", "nothing")])
def test_key_submode_error(mode, submode):
    with pytest.raises(KeyError):
        nkey = notes.Key('C', mode, submode)


@pytest.mark.parametrize(
    "mode, submode", [("major", 1), ("minor", True)])
def test_key_submode_error(mode, submode):
    with pytest.raises(TypeError):
        nkey = notes.Key('C', mode, submode)
