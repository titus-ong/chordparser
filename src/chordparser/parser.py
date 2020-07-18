from chordparser.notes_editor import NoteEditor
from chordparser.keys_editor import KeyEditor
from chordparser.scales_editor import ScaleEditor
from chordparser.chords_editor import ChordEditor
from chordparser.chords_analyser import ChordAnalyser
from chordparser.chord_roman_converter import ChordRomanConverter
import os.path


class Parser(KeyEditor, NoteEditor, ScaleEditor, ChordEditor, ChordAnalyser, ChordRomanConverter):
    """
    Parser class that acts as a central collection for easy access to the Editors and Analysers.

    The Parser can use the methods under all the various Editors and Analysers. This makes it more convenient to initialise the various musical classes and interact with them.
    """
    _path = os.path.join(os.path.dirname(__file__), 'sample_sheet.cho')
    sample = open(_path, 'r')
