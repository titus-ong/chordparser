from chordparser.utils.unicode_chars import (flat, doubleflat,
                                             sharp, doublesharp)
from chordparser.music.letter import Letter
from chordparser.music.symbol import Symbol


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

letter_converter = {
    "C": Letter.C,
    "D": Letter.D,
    "E": Letter.E,
    "F": Letter.F,
    "G": Letter.G,
    "A": Letter.A,
    "B": Letter.B,
}
symbol_converter = {
    "b": Symbol.FLAT,
    flat: Symbol.FLAT,
    "bb": Symbol.DOUBLEFLAT,
    doubleflat: Symbol.DOUBLEFLAT,
    "#": Symbol.SHARP,
    sharp: Symbol.SHARP,
    "##": Symbol.DOUBLESHARP,
    doublesharp: Symbol.DOUBLESHARP,
    None: Symbol.NATURAL,
}
