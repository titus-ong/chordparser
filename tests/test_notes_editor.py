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
    "note", ['CA', 'D\u266F\u266F', '\u266DG', '\U0001D12A', 'F###'])
def test_note_creation_valueerror(note):
    with pytest.raises(ValueError):
        new_note = NE.create_note(note)


@pytest.mark.parametrize(
    "notes, interval", [
        (('C', 'D#'), (3,)),
        (('B', 'E', 'F#'), (5, 2)),
    ]
)
def test_intervals(notes, interval):
    note_list = []
    for each in notes:
        note_list.append(NE.create_note(each))
    assert interval == NE.get_intervals(*note_list)


@pytest.mark.parametrize(
    "notes, interval", [
        (('C', 'B'), (-1,)),
        (('B', 'E', 'D'), (5, -2)),
    ]
)
def test_min_intervals(notes, interval):
    note_list = []
    for each in notes:
        note_list.append(NE.create_note(each))
    assert interval == NE.get_min_intervals(*note_list)


@pytest.mark.parametrize(
    "notes, difference", [
        (('C', 'B'), ((11, 6),)),
        (('B', 'E', 'D'), ((5, 4), (10, 7))),
    ]
)
def test_tone_letter(notes, difference):
    note_list = []
    for each in notes:
        note_list.append(NE.create_note(each))
    assert difference == NE.get_tone_letter(*note_list)


def test_change_note():
    note = NE.create_note("C")
    NE.change_note(note, "d")
    assert "D" == note


def test_change_note_not_inplace():
    note = NE.create_note("C")
    new = NE.change_note(note, "C", inplace=False)
    assert new is not note
