import pytest

from chordparser.music.chordtypes.suspended import SusNotationParser


class TestPCNPParseNotation:
    @pytest.fixture
    def parser(self):
        return SusNotationParser()

    @pytest.mark.parametrize(
        "notation, string",
        [("sus", "sus4"), ("sus2", "sus2"), ("sus4", "sus4")]
    )
    def test_correct_notation(self, parser, notation, string):
        result = parser.parse_notation(notation)
        assert string == result
