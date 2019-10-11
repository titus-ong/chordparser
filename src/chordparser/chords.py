"""
Parse chord notation and return key and mode.
"""
from .general import Error
from .notes import Note
import re


class ChordError(Error):
    pass


class Chord:
    def __init__(self, chord_name: str):
        self.name = chord_name

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        if not isinstance(value, str):
            raise ChordError("Only strings are accepted")
        pattern = "([a-gA-G])(bb|##|b|#){0,1}((Maj|Ma|M|maj)|(min|m|-)){0,1}(.*)"
        rgx = re.match(pattern, value)
        if not rgx:
            raise ChordError("Chord could not be recognised")
        note = rgx.group(1)
        accidental = rgx.group(2) or ''
        self.note = Note(note + accidental)
        if not rgx.group(3):  # No quality, check capital letter
            quality = rgx.group(1).isupper()
        elif rgx.group(4):  # Major
            quality = True
        else:
            quality = False
        if quality:
            self.quality = 'major'
        else:
            self.quality = 'minor'
        self.other = rgx.group(6)
        self._name = value


class ChordConverter:
    pass  # Convert chords to scales (keys) for roman numeral analysis


class ChordTransposer:
    pass  # parse chord to get position relative to base interval (if there's sharp/flat), then go to new key and add that position back to the sign
    # e.g. D# in G major --> +1 to D in G major
    # convert to Eb major --> Bb +1 ==> B in Eb major
