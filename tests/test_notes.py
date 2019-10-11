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
    "note", ['CA', 'D\u266F\u266F', '\u266DG', 1, '\U0001D12A', 'Ebbb', 'F###'])
def test_note_creation_negative(note):
    with pytest.raises(notes.NoteError):
        new_note = notes.Note(note)


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
