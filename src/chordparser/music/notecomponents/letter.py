from enum import Enum


class Letter(Enum):
    """Enum for the letter part of a `Note`.

    The enum members available are C, D, E, F, G, A and B. Their values
    correspond to their index in the natural note scale and their
    semitone steps away from C.

    """

    C = (0, 0)
    D = (1, 2)
    E = (2, 4)
    F = (3, 5)
    G = (4, 7)
    A = (5, 9)
    B = (6, 11)

    def index(self):
        """Return the index of the `Letter` in the natural note scale.

        Returns
        -------
        int
            The index of the `Letter`.

        Examples
        --------
        >>> Letter.C.index()
        0
        >>> Letter.D.index()
        1
        >>> Letter.B.index()
        6

        """
        return self.value[0]

    def as_steps(self):
        """Return the number of steps of the `Letter` from C.

        Returns
        -------
        int
            The number of steps of the `Letter` from C.

        Examples
        --------
        >>> Letter.C.as_steps()
        0
        >>> Letter.D.as_steps()
        2
        >>> Letter.B.as_steps()
        11

        """
        return self.value[1]

    def __str__(self):
        return f"{self.name}"

    def __repr__(self):
        return f"Letter.{self.name}"
