import pytest

from chordparser.music.notationparser import NotationParserTemplate
import chordparser.utils.regex_patterns as RegP


class RegexParserTemplate(NotationParserTemplate):
    def __init__(self, pattern):
        self._pattern = pattern
        super().__init__()

    def _split_into_groups(self, regex):
        return regex.group()


class TestLowered5:
    @pytest.fixture
    def parser(self):
        return RegexParserTemplate(RegP.lowered_5_pattern)

    @pytest.mark.parametrize("pattern", ["o5", "b5"])
    def test_correct_match(self, parser, pattern):
        assert pattern == parser.parse_notation(pattern)


class TestRaised5:
    @pytest.fixture
    def parser(self):
        return RegexParserTemplate(RegP.raised_5_pattern)

    @pytest.mark.parametrize("pattern", ["#5", "+5"])
    def test_correct_match(self, parser, pattern):
        assert pattern == parser.parse_notation(pattern)


class TestDimTriad:
    @pytest.fixture
    def parser(self):
        return RegexParserTemplate(RegP.dim_triad_pattern)

    @pytest.mark.parametrize("pattern", ["dim", "mb5", "mo5"])
    def test_correct_match(self, parser, pattern):
        assert pattern == parser.parse_notation(pattern)


class TestAugTriad:
    @pytest.fixture
    def parser(self):
        return RegexParserTemplate(RegP.aug_triad_pattern)

    @pytest.mark.parametrize("pattern", ["aug", "M#5", "M+5"])
    def test_correct_match(self, parser, pattern):
        assert pattern == parser.parse_notation(pattern)
