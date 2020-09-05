from chordparser.utils.unicode_chars import (flat, doubleflat,
                                             sharp, doublesharp)
from chordparser.music.notecomponents.letter import Letter
from chordparser.music.keycomponents.mode import Mode
from chordparser.music.notecomponents.symbol import Symbol
from chordparser.music.keycomponents.submode import Submode


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
mode_converter = {
    "major": Mode.MAJOR,
    "ionian": Mode.IONIAN,
    "dorian": Mode.DORIAN,
    "phrygian": Mode.PHRYGIAN,
    "lydian": Mode.LYDIAN,
    "mixolydian": Mode.MIXOLYDIAN,
    "aeolian": Mode.AEOLIAN,
    "minor": Mode.MINOR,
    "locrian": Mode.LOCRIAN,
}
submode_converter = {
    "natural": Submode.NATURAL,
    "harmonic": Submode.HARMONIC,
    "melodic": Submode.MELODIC,
    "none": Submode.NONE,
}
