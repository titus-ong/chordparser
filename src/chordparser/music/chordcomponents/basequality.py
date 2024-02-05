from enum import Enum

from chordparser.music.scaledegree import ScaleDegree


class BaseQuality(Enum):
    """Enum for the base quality of a `Chord`.

    The enum members available are MAJOR, MINOR, AUGMENTED, DIMINISHED,
    SUS2, SUS4, DOMINANT, HALFDIMINISHED and POWER.

    """

    MAJOR = (
        str.upper,
        True,
        ("1", "3", "5"),
        "",
    )
    MINOR = (
        str.lower,
        True,
        ("1", "b3", "5"),
        "m",
    )
    AUGMENTED = (
        str.upper,
        False,
        ("1", "3", "#5"),
        "aug",
    )
    DIMINISHED = (
        str.lower,
        False,
        ("1", "b3", "b5"),
        "dim",
    )
    SUS2 = (
        str.upper,
        False,
        ("1", "2", "5"),
        "sus2",
    )
    SUS4 = (
        str.upper,
        False,
        ("1", "4", "5"),
        "sus4",
    )
    DOMINANT = (
        str.upper,
        True,
        ("1", "3", "5"),
        "",
    )
    HALFDIMINISHED = (
        str.lower,
        False,
        ("1", "b3", "b5"),
        "\u00f8",
    )
    POWER = (
        str.upper,
        False,
        ("1", "5"),
        "5",
    )

    def roman_letter_case_converter(self, roman):
        """Convert the Roman numeral letter case based on quality."""
        return self.value[0](roman)

    def is_derived_from_scale(self):
        """Return if the quality is derived from a scale mode."""
        return self.value[1]

    @property
    def scale_degrees(self):
        return tuple(ScaleDegree(notation) for notation in self.value[2])

    def __str__(self):
        return self.value[3]

    def __repr__(self):
        return f"BaseQuality.{self.name}"
