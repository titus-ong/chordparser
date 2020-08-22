from collections import UserString

from chordparser.utils.converters import (symbol_to_unicode,
                                          symbol_to_int,
                                          int_to_symbol)



class Symbol(UserString):
    """A class representing the symbol part of a `Note`.

    The `Symbol` is automatically converted to its unicode form. Only
    symbols from doubleflats to doublesharps are allowed.

    """
    def __init__(self, data):
        self.data = symbol_to_unicode[data]

    def as_int(self):
        """Return the `Symbol`'s semitone value (basis: natural = 0).

        The integer value is based on the number of semitones above or
        below the natural note.

        Returns
        -------
        int
            The integer `Symbol` value.

        Examples
        --------
        >>> sharp = Symbol("#")
        >>> sharp.as_int()
        1

        """
        return symbol_to_int[self.data]

    def shift_by(self, semitones):
        """Shift the `Symbol` (i.e. raise or lower it).

        Parameters
        ----------
        semitones : int
            The semitones to shift the `Symbol` by.

        Examples
        --------
        >>> sharp = Symbol("#")
        >>> sharp.shift_by(-2)
        >>> sharp
        \u266D

        """
        int_value = self.as_int() + semitones
        if int_value not in int_to_symbol.keys():
            raise ValueError(
                "Symbol integer value is out of range"
            )
        self.data = int_to_symbol[int_value]
