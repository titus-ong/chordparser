import pytest

from chordparser.music.key import (ModeError, ModeNotationParser,
                                   KeyNotationParser, Key)


class TestMNPParseNotation:
    @pytest.fixture
    def parser(self):
        return ModeNotationParser()

    @pytest.mark.parametrize(
        "notation, expected_mode", [
            ("", "major"),
            ("m", "minor"),
            (" major", "major"),
            (" Dorian", "dorian"),
        ]
    )
    def test_correct_mode(self, parser, notation, expected_mode):
        mode, _ = parser.parse_notation(notation)
        assert expected_mode == mode

    @pytest.mark.parametrize(
        "notation, expected_submode", [
            (" minor", "natural"),
            ("harmonic minor", "harmonic"),
            (" major", ""),
        ]
    )
    def test_correct_submode(self, parser, notation, expected_submode):
        _, submode = parser.parse_notation(notation)
        assert expected_submode == submode

    def test_mode_error(self, parser):
        with pytest.raises(ModeError):
            parser.parse_notation("natural major")
