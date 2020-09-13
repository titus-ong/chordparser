from chordparser.music.notationparser import NotationParserTemplate
from chordparser.utils.regex_patterns import power_pattern


class PowerChordNotationParser(NotationParserTemplate):
    """Parse power chords."""

    _pattern = f"({power_pattern})"

    def _split_into_groups(self, regex):
        return regex.group(1)
