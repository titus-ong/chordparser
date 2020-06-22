from chordparser.notes_editor import NoteEditor
from chordparser.keys_editor import KeyEditor
from chordparser.scales_editor import ScaleEditor
from chordparser.chords_editor import ChordEditor
from chordparser.chords_analyser import ChordAnalyser


class Parser:
    sample = 'sample_sheet.cho'

    def __init__(self):
        self.NE = NoteEditor()
        self.KE = KeyEditor()
        self.SE = ScaleEditor()
        self.CE = ChordEditor()
        self.CA = ChordAnalyser()

    def __getattr__(self, attribute):
        # So Note methods can be used on Key
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
