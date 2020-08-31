import pytest

from chordparser.music.letter import Letter
from chordparser.music.symbol import Symbol
from chordparser.music.note import NoteNotationParser, Note
from chordparser.utils.unicode_chars import (sharp, doublesharp,
                                             flat, doubleflat)


class TestNNPParseNotation:
    @pytest.fixture
    def parser(self):
        return NoteNotationParser()

    @pytest.mark.parametrize(
        "notation, expected_letter, expected_symbol", [
            ("C", "C", None),
            ("d", "D", None),
            ("C#", "C", "#"),
            ("Db", "D", "b"),
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


class TestNote:
    def test_init(self):
        note = Note("C#")
        assert Letter.C == note.letter
        assert Symbol.SHARP == note.symbol


class TestNoteAsSteps:
    @pytest.mark.parametrize(
        "note, value", [
            ("C#", 1),
            ("Bbb", 9),
            ("B##", 1),
        ]
    )
    def test_correct_int(self, note, value):
        n = Note(note)
        assert value == n.as_steps()


class TestNoteShiftLetter:
    @pytest.mark.parametrize(
        "shift, letter", [
            (2, Letter.E),
            (-1, Letter.B),
            (15, Letter.D),
        ]
    )
    def test_correct_shift(self, shift, letter):
        this = Note("C")
        this._shift_letter(shift)
        assert letter == this.letter


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
