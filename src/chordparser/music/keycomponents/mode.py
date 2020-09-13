from enum import Enum


class Mode(Enum):
    """Enum for the various modes, including major and minor.

    The enum members available are MAJOR, MINOR, IONIAN, DORIAN,
    PHRYGIAN, LYDIAN, MIXOLYDIAN, AEOLIAN and LOCRIAN.

    """

    MAJOR = (
        2, 2, 1, 2, 2, 2, 1,
        2, 2, 1, 2, 2, 2, 1,
    )
    IONIAN = (
        2, 2, 1, 2, 2, 2, 1,
        2, 2, 1, 2, 2, 2, 1,
    )
    DORIAN = (
        2, 1, 2, 2, 2, 1, 2,
        2, 1, 2, 2, 2, 1, 2,
    )
    PHRYGIAN = (
        1, 2, 2, 2, 1, 2, 2,
        1, 2, 2, 2, 1, 2, 2,
    )
    LYDIAN = (
        2, 2, 2, 1, 2, 2, 1,
        2, 2, 2, 1, 2, 2, 1,
    )
    MIXOLYDIAN = (
        2, 2, 1, 2, 2, 1, 2,
        2, 2, 1, 2, 2, 1, 2,
    )
    MINOR = (
        2, 1, 2, 2, 1, 2, 2,
        2, 1, 2, 2, 1, 2, 2,
    )
    AEOLIAN = (
        2, 1, 2, 2, 1, 2, 2,
        2, 1, 2, 2, 1, 2, 2,
    )
    LOCRIAN = (
        1, 2, 2, 1, 2, 2, 2,
        1, 2, 2, 1, 2, 2, 2,
    )

    @property
    def step_pattern(self):
        return self.value

    def __str__(self):
        return f"{self.name.lower()}"

    def __repr__(self):
        return f"Mode.{self.name}"
