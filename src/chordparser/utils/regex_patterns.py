from chordparser.utils.unicode_chars import (flat, doubleflat,
                                             sharp, doublesharp)
from chordparser.music.notecomponents.letter import Letter
from chordparser.music.keycomponents.mode import Mode
from chordparser.music.notecomponents.symbol import Symbol
from chordparser.music.keycomponents.submode import Submode


# General note
note_pattern = "[A-Ga-g]"
flat_pattern = f"b|{flat}"
doubleflat_pattern = f"bb|{doubleflat}"
sharp_pattern = f"#|{sharp}"
doublesharp_pattern = f"##|{doublesharp}"
symbol_pattern = (
    f"{doubleflat_pattern}|{flat_pattern}|"
    f"{doublesharp_pattern}|{sharp_pattern}"
)
degree_pattern = "[1-7]"

# Mode
submode_pattern = "natural|harmonic|melodic"
mode_pattern = (
    "major|minor|ionian|dorian|phrygian|"
    "lydian|mixolydian|aeolian|locrian"
)
short_minor_pattern = "m"
short_major_pattern = ""

# General quality
major_pattern = "Maj|Ma|M|maj|\u0394"
minor_pattern = "min|m|-"
dim_pattern = "dim|o|\u00B0"
aug_pattern = r"aug|\+"
halfdim_pattern = "\u00f8|\u00d8"
sus2_pattern = "sus2"
sus4_pattern = "sus4|sus"
lowered_5_pattern = f"(?:{dim_pattern})5|(?:{flat_pattern})5"
raised_5_pattern = f"(?:{aug_pattern})5|(?:{sharp_pattern})5"

# Quality
power_pattern = "5"
dim_triad_pattern = f"{dim_pattern}|(?:{minor_pattern})(?:{lowered_5_pattern})"
aug_triad_pattern = f"{aug_pattern}|(?:{major_pattern})(?:{raised_5_pattern})"

# Convert matched regex to enum
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
