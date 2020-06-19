from chordparser import notes_editor
import pytest


NE = notes_editor.NoteEditor()


@pytest.mark.parametrize(
    "note, expected", [
        ('C', 'C'), ('D\u266F', 'D\u266F'), ('G\u266D', 'G\u266D'),
        ('A\U0001D12B', 'A\U0001D12B'), ('B\U0001D12A', 'B\U0001D12A'),
        ('F#', 'F\u266F'), ('Eb', 'E\u266d'),
        ('Gbb', 'G\U0001D12B'), ('C##', 'C\U0001D12A'),
        ])
def test_note_creation_positive(note, expected):
    new_note = NE.create_note(note)
    assert new_note.value == expected


@pytest.mark.parametrize(
    "note", [True, 1, len, [], ()])
def test_note_creation_typeerror(note):
    with pytest.raises(TypeError):
        new_note = NE.create_note(note)


@pytest.mark.parametrize(
    "note", ['CA', 'D\u266F\u266F', '\u266DG', '\U0001D12A', 'F###'])
def test_note_creation_valueerror(note):
    with pytest.raises(ValueError):
        new_note = NE.create_note(note)


@pytest.mark.parametrize(
    "note1, note2, interval", [
        ('C', 'D#', 3),
        ('B', 'E', 5),
        ]
    )
def test_intervals(note1, note2, interval):
    n1 = NE.create_note(note1)
    n2 = NE.create_note(note2)
    assert interval == NE.get_interval(n1, n2)



