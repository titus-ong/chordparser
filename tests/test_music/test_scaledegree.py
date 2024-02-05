import pytest

from chordparser.music.scaledegree import (ScaleDegree,
                                           ScaleDegreeNotationParser)
from chordparser.music.notecomponents.symbol import Symbol


class TestSDNPParseNotation:
    @pytest.fixture
    def parser(self):
        return ScaleDegreeNotationParser()

    def test_correct_groups(self, parser):
        degree, symbol = parser.parse_notation("5")
        assert "5" == degree
        assert None == symbol

    def test_correct_groups_2(self, parser):
        degree, symbol = parser.parse_notation("b4")
        assert "4" == degree
        assert "b" == symbol

    def test_wrong_notation(self, parser):
        with pytest.raises(SyntaxError):
            parser.parse_notation("0")


class TestScaleDegree:
    def test_creation(self):
        sd = ScaleDegree("b5")
        assert Symbol.FLAT == sd.symbol
        assert 5 == sd.degree


class TestScaleDegreeFromComps:
    def test_creation(self):
        sd = ScaleDegree.from_components(5, "b")
        sd2 = ScaleDegree.from_components(5, Symbol.FLAT)
        assert sd == sd2


class TestScaleDegreeEquality:
    def test_equality_sd(self):
        sd = ScaleDegree("b5")
        sd2 = ScaleDegree("b5")
        assert sd2 == sd

    def test_equality_str(self):
        sd = ScaleDegree("b5")
        assert "\u266d5" == sd

    def test_inequality(self):
        sd = ScaleDegree("b5")
        sd2 = ScaleDegree("b4")
        assert sd2 != sd

    def test_inequality_2(self):
        sd = ScaleDegree("b5")
        assert len != sd
