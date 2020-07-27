import os.path

from chordparser.analysers.chords_analyser import ChordAnalyser
from chordparser.editors.chord_roman_converter import ChordRomanConverter
from chordparser.editors.chords_editor import ChordEditor
from chordparser.editors.keys_editor import KeyEditor
from chordparser.editors.notes_editor import NoteEditor
from chordparser.editors.scales_editor import ScaleEditor


class Parser(KeyEditor, NoteEditor, ScaleEditor, ChordEditor, ChordAnalyser, ChordRomanConverter):
    """A class that acts as a central collection for `Editors` and `Analysers`.

    The `Parser` inherits all the various `Editors` and `Analysers`. As such, all the examples using the `Editors` and `Analysers` can also use the `Parser` to create and interact with musical objects. This makes it more convenient to initialise the various musical classes without having to initialise many different `Editors` for each class beforehand.

    Examples
    --------
    >>> cp = Parser()
    >>> cp.create_note("D#")
    D\u266f note
    >>> c_chord = cp.create_chord("Cmaj7/G")
    >>> c_chord
    Cmaj7/G chord
    >>> c_scale = cp.create_scale("C", "major")
    >>> cp.analyse_diatonic(c_chord, c_scale)
    [(IM43 roman chord, 'major', None)]

    """
    _path = os.path.join(os.path.dirname(__file__), 'sample_sheet.cho')

    def __init__(self):
        try:
            with open(Parser._path, 'r') as f:
                self.sample = f.read()
        except IOError:
            self.sample = ""
