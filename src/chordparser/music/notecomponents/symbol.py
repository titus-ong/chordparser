from enum import Enum

from chordparser.utils.unicode_chars import (sharp, doublesharp,
                                             flat, doubleflat)


class Symbol(Enum):
    """Enum for the symbol part of a `Note`.

    The enum members available are DOUBLEFLAT, FLAT, NATURAL, SHARP
    and DOUBLESHARP.

    """

    DOUBLEFLAT = (doubleflat, -2)
    FLAT = (flat, -1)
    NATURAL = ("", 0)
    SHARP = (sharp, 1)
    DOUBLESHARP = (doublesharp, 2)

    def as_steps(self):
        """Return the number of steps of the `Symbol` from NATURAL.

        Returns
        -------
        int
            The number of steps from NATURAL.

        Examples
        --------
        >>> Symbol.SHARP.as_steps()
        1
        >>> Symbol.FLAT.as_steps()
        -1

        """
        return self.value[1]

    def __str__(self):
        return f"{self.value[0]}"

    def __repr__(self):
        return f"Symbol.{self.name}"
