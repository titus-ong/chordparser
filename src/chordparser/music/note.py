from chordparser.music.letter import Letter
from chordparser.music.notationparser import NotationParserTemplate
from chordparser.music.symbol import Symbol
from chordparser.utils.converters import symbol_to_unicode
from chordparser.utils.note_lists import sharp_scale, flat_scale
from chordparser.utils.regex_patterns import (note_pattern,
                                              symbol_pattern)


class NoteNotationParser(NotationParserTemplate):
    """Parse note notation into letter and symbol groups."""
    _pattern = (
        f"({note_pattern})({symbol_pattern})?"
    )

    def _split_into_groups(self, regex):
        """Split into capitalised letter and symbol."""
        uppercase_letter = regex.group(1).upper()
        symbol = symbol_to_unicode[regex.group(2)]
        return uppercase_letter, symbol


class Note:
    """A class representing a musical note.

    The `Note` class composes of a `Letter` and `Symbol` object,
    representing the letter and symbol part of the `Note` respectively.
    It is created from a string of notation A-G with optional
    accidental symbols b, bb, #, ## or their respective unicode
    characters \u266d, \u266f, \U0001D12B, or \U0001D12A. Upon
    creation, the symbols will be converted to unicode.

    Parameters
    ----------
    notation : str
        The notation of the `Note` to be created.

    Attributes
    ----------
    letter : Letter
        The letter part of the `Note`'s notation.
    symbol : Symbol
        The symbol part of the `Note`'s notation. If there is no
        symbol, this will be a Symbol of an empty string.

    Raises
    ------
    SyntaxError
        If the notation is invalid.

    Examples
    --------
    >>> note = Note("C#")
    >>> note
    C\u266f Note
    >>> str(note)
    "C\u266f"

    """

    _NNP = NoteNotationParser()

    def __init__(self, notation):
        self._set(notation)

    def _set(self, notation):
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

    def transpose(self, semitones, letters):
        """Transpose the `Note` by some semitone and letter intervals.

        Parameters
        ----------
        semitones : int
            The difference in semitones to the transposed `Note`.
        letters : int
            The difference in scale degrees to the transposed `Note`.

        Examples
        --------
        >>> note = Note("C")
        >>> note.transpose(6, 3)
        >>> note
        F\u266f Note
        >>> note.transpose(0, 1)
        >>> note
        G\u266d Note

        """
        original_int = self.as_int()
        self._letter.shift_by(letters)
        positive_int_diff = (self.as_int() - original_int) % 12
        positive_semitones = semitones % 12
        semitone_difference = positive_semitones - positive_int_diff
        self._symbol.shift_by(semitone_difference)

    def transpose_simple(self, semitones, use_flats=False):
        """Transpose the `Note` by some semitone interval.

        Parameters
        ----------
        semitones : int
            The difference in semitones to the transposed `Note`.
        use_flats : boolean, Optional
            Selector to use flats or sharps for black keys. Default
            False when optional.

        Examples
        --------
        >>> note = Note("C")
        >>> note.transpose_simple(6)
        F\u266f Note
        >>> note.transpose_simple(2, use_flats=True)
        A\u266d Note

        """
        if use_flats:
            notes = flat_scale
        else:
            notes = sharp_scale
        note = notes[(self.as_int() + semitones) % 12]
        self._set(note)

    def __repr__(self):
        return f"{self} Note"

    def __str__(self):
        return f"{self._letter}{self._symbol}"

    def __eq__(self, other):
        """Compare with other `Notes` or strings.

        If comparing with a `Note`, checks if the other `Note`'s string notation is the same as this `Note`. If comparing with a
        string, checks if the string is equal to this `Note`'s string
        notation.'

        Parameters
        ----------
        other
            The object to be compared with.

        Returns
        -------
        boolean
            The outcome of the comparison.

        Examples
        --------
        >>> d = Note("D")
        >>> d2 = Note("D")
        >>> d_str = "D"
        >>> d == d2
        True
        >>> d == d_str
        True

        Note that symbols are converted to their unicode characters
        when a `Note` is created.

        >>> ds = Note("D#")
        >>> ds_str = "D#"
        >>> ds_str_2 = "D\u266f"
        >>> ds == ds_str
        False
        >>> ds == ds_str_2
        True

        """
        if isinstance(other, Note):
            return (
                self._letter == other.letter and
                self._symbol == other.symbol
            )
        if isinstance(other, str):
            return str(self) == other
        return NotImplemented
