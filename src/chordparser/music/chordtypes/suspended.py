from chordparser.music.chordcomponents.basequality import BaseQuality
from chordparser.music.notationparser import NotationParserTemplate
from chordparser.utils.regex_patterns import sus2_pattern, sus4_pattern


sus_enum_dict = {
    "sus2": BaseQuality.SUS2,
    "sus4": BaseQuality.SUS4,
}


class SusNotationParser(NotationParserTemplate):
    """Parse suspended chords."""

    # sus2 must come first since sus4 detects for "sus"
    _pattern = f"({sus2_pattern})|({sus4_pattern})"

    def _split_into_groups(self, regex):
        return "sus2" if regex.group(1) else "sus4"
