from chordparser.music.notationparser import NotationParser
from chordparser.music.note import NoteNotationParser
from chordparser.utils.regex_patterns import (submode_pattern,
                                              mode_pattern,
                                              short_minor_pattern,
                                              short_major_pattern)


class ModeError(Exception):
    """Exception where a `Key`'s `mode` is invalid."""
    pass


class ModeNotationParser(NotationParser):
    """Parse mode notation into mode and submode."""
    _pattern = (
        fr"(\s?({submode_pattern})?\s?({mode_pattern}))|"
        f"({short_minor_pattern})|"
        f"({short_major_pattern})"
    )

    def _split_into_groups(self, regex):
        """Split into mode and submode."""
        mode = self._get_mode(
            regex.group(3), regex.group(4), regex.group(5)
        )
        submode = self._get_submode(
            regex.group(2), self._is_minor(mode)
        )
        return mode, submode

    def _get_mode(self, long_mode, short_minor, short_major):
        if short_major is not None:
            return "major"
        if short_minor:
            return "minor"
        return long_mode.lower()

    def _is_minor(self, mode):
        return mode in ("minor", "aeolian")

    def _get_submode(self, submode, is_minor):
        if submode and not is_minor:
            raise ModeError("Only minor can have a submode")
        if not is_minor:
            return ""
        if is_minor and not submode:
            return "natural"
        return submode.lower()


class KeyNotationParser:
    """Parse key notation into tonic and mode groups."""
    _NNP = NoteNotationParser()
    _MNP = ModeNotationParser()
    _pattern = (
        f"({_NNP.get_regex_pattern})"
        f"({_MNP.get_regex_pattern})"
    )


class Key:
    def __init__(self, notation):
        pass
