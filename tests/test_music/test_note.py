import pytest

from chordparser.utils.unicode_chars import (sharp, doublesharp,
                                             flat, doubleflat)
from chordparser.music.note import NoteNotationParser, Note


class TestNNPParseNotation:
    @pytest.fixture
    def parser(self):
        return NoteNotationParser()

    @pytest.mark.parametrize(
        "notation, expected_letter, expected_symbol", [
            ("C", "C", ""),
            ("d", "D", ""),
            ("C#", "C", "\u266F"),
            ("Db", "D", "\u266D"),
        ]
    )
    def test_correct_notation(
            self, parser, notation, expected_letter, expected_symbol,
    ):
        letter, symbol = parser.parse_notation(notation)
        assert expected_letter == letter
        assert expected_symbol == symbol

    @pytest.mark.parametrize(
        "notation", [
            "Ca", "C###", "Cbbb", "H",
        ]
    )
    def test_syntax_error(self, parser, notation):
        with pytest.raises(SyntaxError):
            parser.parse_notation(notation)


class TestNNPGetRegexGroupsCount:
    def test_correct_number_of_groups(self):
        parser = NoteNotationParser()
        parser._pattern = "(a)(b)"
        assert 2 == parser.get_regex_groups_count()


class TestNote:
    def test_init(self):
        note = Note("C#")
        assert "C" == note.letter
        assert sharp == note.symbol


class TestNoteAsInt:
    @pytest.mark.parametrize(
        "note, value", [
            ("C#", 1),
            ("Bbb", 9),
            ("B##", 1),
        ]
    )
    def test_correct_int(self, note, value):
        n = Note(note)
        assert value == n.as_int()


class TestNoteTranspose:
    @pytest.mark.parametrize(
        "semitones, letters, old, new", [
            (1, 0, "C", f"C{sharp}"),
            (-2, -1, "C", f"B{flat}"),
            (-5, -4, "C", f"F{doublesharp}"),
            (-3, -2, "D", "B"),
        ]
    )
    def test_correct_transpose(self, semitones, letters, old, new):
        n = Note(old)
        n.transpose(semitones, letters)
        assert new == str(n)


class TestNoteTransposeSimple:
    @pytest.mark.parametrize(
        "note, num, new_note", [
            ("C", 2, "D"),
            ("C", -13, "B"),
            ("C", 3, f"D{sharp}")
        ]
    )
    def test_correct_transpose_simple(self, note, num, new_note):
        n = Note(note)
        n.transpose_simple(num)
        assert new_note == str(n)


    def test_correct_transpose_simple_flats(self):
        n = Note("C")
        n.transpose_simple(3, use_flats=True)
        assert f"E{flat}" == str(n)


class TestNoteEquality:
    def test_equality(self):
        c = Note("C")
        c2 = Note("C")
        c_str = "C"
        assert c == c2
        assert c == c_str

    @pytest.mark.parametrize(
        "other", [Note("D"), "D", len]
    )
    def test_inequality(self, other):
        c = Note("C")
        assert other != c
