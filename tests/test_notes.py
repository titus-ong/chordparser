from chordparser import notes
from chordparser import notes_editor
import pytest


NE = notes_editor.NoteEditor()


@pytest.mark.parametrize(
    "accidental", ['CA', 'D\u266F', 2.0])
def test_note_accidental_wrong_type(accidental):
    new_note = NE.create_note('C')
    with pytest.raises(TypeError):
        new_note.accidental(accidental)


@pytest.mark.parametrize(
    "accidental", [-3, 3])
def test_note_accidental_wrong_value(accidental):
    new_note = NE.create_note('C')
    with pytest.raises(ValueError):
        new_note.accidental(accidental)


@pytest.mark.parametrize(
    "accidental, note", [
        (-2, 'C\U0001D12B'), (-1, 'C\u266d'),
        (0, 'C'), (1, 'C\u266f'), (2, 'C\U0001D12A')])
def test_note_accidental_positive(accidental, note):
    new_note = NE.create_note('C')
    new_note.accidental(accidental)
    assert new_note.value == note


@pytest.mark.parametrize(
    "shift", ['CA', 'D\u266F', 2.0, len, [], ()])
def test_note_shift_wrong_type(shift):
    new_note = NE.create_note('C')
    with pytest.raises(TypeError):
        new_note.shift_s(shift)


@pytest.mark.parametrize(
    "shift", [300, -10, 3, -3])
def test_note_shift_wrong_value(shift):
    new_note = NE.create_note('C')
    with pytest.raises(ValueError):
        new_note.shift_s(shift)


@pytest.mark.parametrize(
    "shift, note", [
        (-2, 'C\U0001D12B'), (-1, 'C\u266d'),
        (0, 'C'), (1, 'C\u266f'), (2, 'C\U0001D12A')])
def test_note_shift_positive(shift, note):
    new_note = NE.create_note('C')
    new_note.shift_s(shift)
    assert new_note.value == note


@pytest.mark.parametrize(
    "shift", ['CA', 'D\u266F', 2.0, len, [], ()])
def test_note_shift_wrong_type_2(shift):
    new_note = NE.create_note('C')
    with pytest.raises(TypeError):
        new_note.shift_l(shift)


@pytest.mark.parametrize(
    "shift, note", [
        (-2, 'A'), (-1, 'B'),
        (15, 'D'), (-10, 'G')
    ]
)
def test_note_shift_positive_2(shift, note):
    new_note = NE.create_note('C')
    new_note.shift_l(shift)
    assert new_note.value == note


@pytest.mark.parametrize(
    "note, value", [
        ('C', 0), ('D\u266F', 3), ('G\u266D', 6),
        ('A\U0001D12B', 7), ('B\U0001D12A', 1)])
def test_note_num_value(note, value):
    new_note = NE.create_note(note)
    assert new_note.num_value() == value


@pytest.mark.parametrize(
    "note", ['C', 'D\u266F', 'G\u266D', 'A\U0001D12B', 'B\U0001D12A'])
def test_note_letter(note):
    new_note = NE.create_note(note)
    assert new_note.letter() == note[0]


@pytest.mark.parametrize(
    "note", ['C', 'D\u266F', 'G\u266D', 'A\U0001D12B', 'B\U0001D12A'])
def test_note_symbol(note):
    new_note = NE.create_note(note)
    if len(note) > 1:
        symbol = note[1]
    else:
        symbol = None
    assert new_note.symbol() == symbol


@pytest.mark.parametrize(
    "note, value", [
        ('C', 0), ('D\u266F', 1), ('G\u266D', -1),
        ('A\U0001D12B', -2), ('B\U0001D12A', 2)])
def test_note_value(note, value):
    new_note = NE.create_note(note)
    if len(note) > 1:
        symbol = note[1]
    else:
        symbol = note[0]
    assert new_note.symbol_value() == value


@pytest.mark.parametrize(
    "note", ['C', 'D\u266F', 'G\u266D', 'A\U0001D12B', 'B\U0001D12A'])
def test_note_creation_repr(note):
    new_note = NE.create_note(note)
    assert repr(new_note) == note


@pytest.mark.parametrize(
    "note", ['C', notes.Note('C')])
def test_note_equality(note):
    new_note = NE.create_note('C')
    assert new_note == note


@pytest.mark.parametrize(
    "note", ['CA', notes.Note('D'), True, 10, 'B#'])
def test_note_inequality(note):
    new_note = NE.create_note('C')
    assert new_note != note


@pytest.mark.parametrize(
    "note, semitone, letter, new_note", [
        ('C', 2, 1, 'D'), ('G\u266d', -5, -4, 'C\u266f'), ('A\U0001D12A', 1, 2, 'C')])
def test_note_transpose(note, semitone, letter, new_note):
    nnote = NE.create_note(note)
    nnote.transpose(semitone, letter)
    assert nnote == new_note


@pytest.mark.parametrize(
    "value", [
        "H#", 10.0, "Z", len])
def test_root_transpose_error(value):
    nnote = NE.create_note('C')
    with pytest.raises(TypeError):
        nnote.transpose(value, 1)


@pytest.mark.parametrize(
    "value", [
        "H#", 10.0, "Z", len])
def test_root_transpose_error_2(value):
    nnote = NE.create_note('C')
    with pytest.raises(TypeError):
        nnote.transpose(1, value)
