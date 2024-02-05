from enum import Enum


class ExtensionQuality(Enum):
    """Enum for the quality of the extension of an extended `Chord`.

    The enum members available are DIMINISHED, HALFDIMINISHED, MINOR,
    DOMINANT and MAJOR.

    """

    DIMINISHED = (-2, "")
    HALFDIMINISHED = (-1, "")
    MINOR = (-1, "")
    DOMINANT = (-1, "")
    MAJOR = (0, "maj")

    def seventh_shift(self):
        """Return the step shift of the seventh.

        Returns
        -------
        int
            The step shift of the seventh.

        Examples
        --------
        >>> ExtensionQuality.DIMINISHED.seventh_shift()
        -2

        """
        return self.value[0]

    def __str__(self):
        return self.value[1]

    def __repr__(self):
        return f"ExtensionQuality.{self.name}"
