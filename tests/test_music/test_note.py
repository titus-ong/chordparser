import pytest

from chordparser.note import NoteNotationParser


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
