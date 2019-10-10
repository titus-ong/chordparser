import chordparser.notes as notes
import pytest


@pytest.mark.parametrize(
    "note", ['C', 'D\u266F', 'G\u266D', 'A\U0001D12B', 'B\U0001D12A'])
def test_note_creation_positive(note):
    new_note = notes.Note(note)
    assert new_note.value == note


@pytest.mark.parametrize(
    "note", ['CA', 'D\u266F\u266F', '\u266DG', 1, '\U0001D12A'])
def test_note_creation_negative(note):
    with pytest.raises(notes.NoteError):
        new_note = notes.Note(note)


@pytest.mark.parametrize(
    "note", ['C', 'D\u266F', 'G\u266D', 'A\U0001D12B', 'B\U0001D12A'])
def test_note_creation_repr(note):
    new_note = notes.Note(note)
    assert repr(new_note) == note


@pytest.mark.parametrize(
    "accidental", ['CA', 'D\u266F', 300, -10, 2.0])
def test_note_accidental_negative(accidental):
    new_note = notes.Note('C')
    with pytest.raises(notes.NoteSymbolError):
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
    "shift", ['CA', 'D\u266F', 300, -10, 2.0, 3, -3])
def test_note_shift_negative(shift):
    new_note = notes.Note('C')
    with pytest.raises(notes.NoteSymbolError):
        new_note.shift(shift)


@pytest.mark.parametrize(
    "shift, note", [
        (-2, 'C\U0001D12B'), (-1, 'C\u266d'),
        (0, 'C'), (1, 'C\u266f'), (2, 'C\U0001D12A')])
def test_note_shift_positive(shift, note):
    new_note = notes.Note('C')
    new_note.shift(shift)
    assert new_note.value == note


def test_note_equality():
    new_note = notes.Note('C')
    assert new_note == 'C'
