from chordparser.utils.unicode_chars import (flat, doubleflat,
                                             sharp, doublesharp)


note_pattern = "[A-G]"
flat_pattern = f"bb|b|{flat}|{doubleflat}"
sharp_pattern = f"##|#|{sharp}|{doublesharp}"
symbol_pattern = f"{flat_pattern}|{sharp_pattern}"
submode_pattern = "natural|harmonic|melodic"
mode_pattern = (
    "major|minor|ionian|dorian|phrygian|"
    "lydian|mixolydian|aeolian|locrian"
)
short_minor_pattern = "m"
short_major_pattern = ""
degree_pattern = "[1-7]"
