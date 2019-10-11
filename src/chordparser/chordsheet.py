"""
Store ChordPro file as a chordparser.Sheet.
"""
from .general import Error


class Sheet:
    def __init__(self, contents):
        self.contents_raw = contents
        self.contents = self.process_contents()

    def process_contents(self):
        pass
        # Check file formatting - brackets and all that
        # Divide file up into different parts - lyrics and chords and {}?

    def __repr__(self):
        return 'Chordsheet'
