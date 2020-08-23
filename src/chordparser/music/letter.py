from collections import UserString

from chordparser.utils.note_lists import (natural_notes,
                                          natural_semitone_intervals)



class Letter(UserString):
    """A class representing the letter part of a `Note`."""

    def as_int(self):
        """Return the `Letter`'s semitone value (basis: C = 0).

        The integer value is based on the number of semitones above C.

        Returns
        -------
        int
            The integer `Letter` value.

        Examples
        --------
        >>> d = Letter("D")
        >>> d.as_int()
        2

        """
        position = natural_notes.index(self.data)
        total_semitones = sum(natural_semitone_intervals[:position])
        return total_semitones

    def shift_by(self, shift):
        """Shift the `Letter` along the natural note scale.

        Parameters
        ----------
        shift : int
            The number of letters to shift by.

        Examples
        --------
        >>> letter = Letter("D")
        >>> letter.shift_by(3)
        >>> letter
        G

        """
        old_position = natural_notes.index(self.data)
        new_position = (old_position + shift) % 7
        self.data = natural_notes[new_position]
