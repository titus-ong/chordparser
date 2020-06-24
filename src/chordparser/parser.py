from chordparser.notes_editor import NoteEditor
from chordparser.keys_editor import KeyEditor
from chordparser.scales_editor import ScaleEditor
from chordparser.chords_editor import ChordEditor
from chordparser.chords_analyser import ChordAnalyser
import os.path


class Parser:
    """
    Parser class that acts as a central collection for easy access to the Editors and Analysers.

    The Parser can use the methods under all the various Editors and Analysers. This makes it more convenient to initialise the various musical classes and interact with them.
    """
    _path = os.path.join(os.path.dirname(__file__), 'sample_sheet.cho')
    sample = open(_path, 'r')

    def __init__(self):
        self.NE = NoteEditor()
        self.KE = KeyEditor()
        self.SE = ScaleEditor()
        self.CE = ChordEditor()
        self.CA = ChordAnalyser()

    def __getattr__(self, attribute):
        # So Editor/Analyser methods can be used on Parser
        if attribute in NoteEditor.__dict__:
            return getattr(self.NE, attribute)
        if attribute in KeyEditor.__dict__:
            return getattr(self.KE, attribute)
        if attribute in ScaleEditor.__dict__:
            return getattr(self.SE, attribute)
        if attribute in ChordEditor.__dict__:
            return getattr(self.CE, attribute)
        if attribute in ChordAnalyser.__dict__:
            return getattr(self.CA, attribute)
        raise AttributeError(f"'Parser' object has no attribute '{attribute}'")
