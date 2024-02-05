import pytest

from chordparser.music.note import Note
from chordparser.utils.notecomparer import NoteComparer


class TestGetSemitoneIntervals:
    def test_correct_intervals(self):
        c = Note("C")
        f = Note("F")
        a = Note("A")
        assert [5, 4] == NoteComparer.get_semitone_intervals([c, f, a])

    def test_invalid_array(self):
        c = Note("C")
        with pytest.raises(IndexError):
            NoteComparer.get_semitone_intervals([c])


class TestGetLetterIntervals:
    def test_correct_intervals(self):
        c = Note("C")
        f = Note("F")
        a = Note("A")
        assert [3, 2] == NoteComparer.get_letter_intervals([c, f, a])

    def test_invalid_array(self):
        c = Note("C")
        with pytest.raises(IndexError):
            NoteComparer.get_letter_intervals([c])


class TestGetSemitoneDisplacements:
    def test_correct_displacements(self):
        c = Note("C")
        b = Note("B")
        assert [-1] == NoteComparer.get_semitone_displacements([c, b])

    def test_invalid_array(self):
        c = Note("C")
        with pytest.raises(IndexError):
            NoteComparer.get_letter_intervals([c])

