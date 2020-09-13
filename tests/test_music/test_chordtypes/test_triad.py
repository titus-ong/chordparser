import pytest

from chordparser.music.chordtypes.triad import TriadNotationParser


class TestPCNPParseNotation:
    @pytest.fixture
    def parser(self):
        return TriadNotationParser()

    @pytest.mark.parametrize(
        "notation, string",
        [("M", "major"), ("dim", "diminished"), ("sus4", "sus4")]
    )
    def test_correct_notation(self, parser, notation, string):
        result = parser.parse_notation(notation)
        assert string == result
