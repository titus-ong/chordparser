import pytest

from chordparser.utils.unicode_chars import sharp
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
