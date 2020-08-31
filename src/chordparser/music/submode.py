from enum import Enum


class Submode(Enum):
    """Enum for the various minor submodes.

    The enum members available are NATURAL, HARMONIC, MELODIC and NONE.
    NONE applies to all non-minor modes. Their values are a tuple of a
    boolean and a tuple. The boolean corresponds to whether the
    submode is minor, while the tuple is the changes in their step
    pattern relative to their mode.

    """

    # The boolean helps to distinguish NATURAL from NONE
    NATURAL = (
        True, (
            0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0,
        ),
    )
    HARMONIC = (
        True, (
            0, 0, 0, 0, 0, 1, -1,
            0, 0, 0, 0, 0, 1, -1,
        ),
    )
    MELODIC = (
        True, (
            0, 0, 0, 0, 1, 0, -1,
            0, 0, 0, 0, 1, 0, -1,
        ),
    )
    NONE = (
        False, (
            0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0,
        ),
    )

    @property
    def step_pattern(self):
        return self.value[1]

    def __str__(self):
        if self is Submode.NONE:
            return ""
        return f"{self.name.lower()}"

    def __repr__(self):
        return f"Submode.{self.name}"
