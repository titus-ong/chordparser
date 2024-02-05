from chordparser.music.chordcomponents.basequality import BaseQuality
from chordparser.music.chordtypes.suspended import (SusNotationParser,
                                                    sus_enum_dict)
from chordparser.music.notationparser import NotationParserTemplate
from chordparser.utils.regex_patterns import (dim_triad_pattern,
                                              aug_triad_pattern,
                                              minor_pattern, major_pattern)


triad_enum_dict = {
    "major": BaseQuality.MAJOR,
    "minor": BaseQuality.MINOR,
    "diminished": BaseQuality.DIMINISHED,
    "augmented": BaseQuality.AUGMENTED,
    **sus_enum_dict,
}


class TriadNotationParser(NotationParserTemplate):
    """Parse triads."""

    _SNP = SusNotationParser()

    _pattern = (
        f"({major_pattern})|({minor_pattern})|"
        f"({dim_triad_pattern})|({aug_triad_pattern})|"
        f"({_SNP.pattern})"
    )

    def _split_into_groups(self, regex):
        triad_dict = {
            0: "major",
            1: "minor",
            2: "diminished",
            3: "augmented",
            4: not regex.group(5) or self._SNP.parse_notation(regex.group(5)),
        }
        index = next(
            idx for (idx, triad) in enumerate(regex.groups())
            if triad is not None
        )
        return triad_dict[index]
