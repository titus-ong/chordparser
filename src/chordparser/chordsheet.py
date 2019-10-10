"""
Store ChordPro file as a chordparser.Sheet.
"""
from .general import Error


class Sheet:
    def __init__(self, contents):
        self.contents_raw = contents

    def __repr__(self):
        return 'Chordsheet'
