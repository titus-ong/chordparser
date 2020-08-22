import re

from chordparser.utils.regex_patterns import (note_pattern,
                                              sharp_pattern,
                                              flat_pattern)
from chordparser.utils.converters import symbol_to_unicode


class NoteNotationParser:
    """Parse note notation into letter and symbol groups."""
    _pattern = (
        f"^({note_pattern})({flat_pattern}|{sharp_pattern}){{0,1}}$"
    )

    def parse_notation(self, notation):
        """Parse the note string."""
        regex = self._to_regex_object(notation)
        if self._invalid_notation(regex):
            raise SyntaxError("invalid syntax")
        letter, symbol = self._split_capital_letter_and_symbol(regex)
        return letter, symbol

    def _to_regex_object(self, notation):
        regex = re.match(
            NoteNotationParser._pattern,
            notation,
            re.UNICODE
        )
        return regex

    def _invalid_notation(self, regex):
        return not regex

    def _split_capital_letter_and_symbol(self, regex):
        uppercase_letter = regex.group(1).upper()
        symbol = symbol_to_unicode[regex.group(2)]
        return uppercase_letter, symbol

    def get_regex_pattern(self):
        return self._pattern

    def get_regex_groups_count(self):
        regex = self._to_regex_object("C")
        return len(regex.groups())
