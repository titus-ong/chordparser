import pytest

from chordparser.music.chordtypes.power import PowerChordNotationParser


class TestPCNPParseNotation:
    @pytest.fixture
    def parser(self):
        return PowerChordNotationParser()

    def test_correct_notation(self, parser):
        result = parser.parse_notation("5")
        assert "power" == result

    def test_reject_wrong_notation(self, parser):
        with pytest.raises(SyntaxError):
            parser.parse_notation("6")
