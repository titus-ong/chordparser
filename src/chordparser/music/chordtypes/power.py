from chordparser.music.chordcomponents.basequality import BaseQuality
from chordparser.music.notationparser import NotationParserTemplate
from chordparser.utils.regex_patterns import power_pattern


power_enum_dict = {
    "power": BaseQuality.POWER,
}


class PowerChordNotationParser(NotationParserTemplate):
    """Parse power chords."""

    _pattern = f"({power_pattern})"

    def _split_into_groups(self, regex):
        return "power"
