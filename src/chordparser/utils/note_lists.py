from chordparser.utils.unicode_chars import sharp, flat


natural_notes = (
    "C", "D", "E", "F", "G", "A", "B",
    "C", "D", "E", "F", "G", "A", "B",
)
mode_order = {
    "major": 0,
    "ionian": 0,
    "dorian": 1,
    "phrygian": 2,
    "lydian": 3,
    "mixolydian": 4,
    "aeolian": 5,
    "minor": 5,
    "locrian": 6,
}
natural_semitone_intervals = (
    2, 2, 1, 2, 2, 2, 1,
    2, 2, 1, 2, 2, 2, 1,
)
harmonic_intervals = (
    0, 0, 0, 0, 0, 1, -1,
    0, 0, 0, 0, 0, 1, -1,
)
melodic_intervals = (
    0, 0, 0, 0, 1, 0, -1,
    0, 0, 0, 0, 1, 0, -1,
)
sharp_scale = (
    "C", f"C{sharp}", "D", f"D{sharp}", "E", "F", f"F{sharp}", "G",
    f"G{sharp}", "A", f"A{sharp}", "B",
    "C", f"C{sharp}", "D", f"D{sharp}", "E", "F", f"F{sharp}", "G",
    f"G{sharp}", "A", f"A{sharp}", "B",
    )
flat_scale = (
    "C", f"D{flat}", "D", f"E{flat}", "E", "F", f"G{flat}", "G",
    f"A{flat}", "A", f"B{flat}", "B",
    "C", f"D{flat}", "D", f"E{flat}", "E", "F", f"G{flat}", "G",
    f"A{flat}", "A", f"B{flat}", "B",
    )
