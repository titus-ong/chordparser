import pytest

from chordparser.music.notationparser import NotationParserTemplate


class NotationParser(NotationParserTemplate):
    _pattern = "(a)(b)"

    def _split_into_groups(self, regex):
        return regex.group(1), regex.group(2)


class TestNPParseNotation:
    @pytest.fixture
    def parser(self):
        return NotationParser()

    def test_correct_parsing(self, parser):
        groups = parser.parse_notation("ab")
        assert "a" == groups[0]
        assert "b" == groups[1]

    def test_wrong_notation(self, parser):
        with pytest.raises(SyntaxError):
            parser.parse_notation("aa")

    def test_incomplete_notation(self, parser):
        with pytest.raises(SyntaxError):
            parser.parse_notation("a")


class TestNPGetNumGroups:
    def test_correct_number_of_groups(self):
        parser = NotationParser()
        assert 2 == parser.get_num_groups()
