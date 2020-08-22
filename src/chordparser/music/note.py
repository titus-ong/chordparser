import re

from chordparser.music.letter import Letter
from chordparser.music.symbol import Symbol
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


class Note:
    _NNP = NoteNotationParser()

    def __init__(self, notation):
        letter, symbol = self._NNP.parse_notation(notation)
        self._letter = Letter(letter)
        self._symbol = Symbol(symbol)

    @property
    def letter(self):
        return self._letter

    @property
    def symbol(self):
        return self._symbol

    def as_int(self):
        """Return the `Note`'s value as an integer (basis: C = 0).

        The integer value is based on the number of semitones above C.

        Returns
        -------
        int
            The integer `Note` value.

        Examples
        --------
        >>> d = Note("D#")
        >>> d.as_int()
        3

        """
        return (self._letter.as_int() + self._symbol.as_int()) % 12
