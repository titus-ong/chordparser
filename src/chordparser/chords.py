"""
Parse chord notation and return key and mode.
"""
from .general import Error, TransposeError
from .notes import Note, Key
from typing import Union
import re


class ChordError(Error):
    pass


class Chord:
    def __init__(self, chord_name: Union[Note, str]):
        self.name = chord_name

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        if not (isinstance(value, str) or isinstance(value, Note)):
            raise ChordError("Only strings or Notes are accepted")
        if isinstance(value, Note):
            value = str(value)
        pattern = (
            "([a-gA-G])(\u266F|\u266D|\U0001D12B|\U0001D12A|bb|##|b|#)"
            "{0,1}((Maj|Ma|M|maj)|(min|m|-)){0,1}(.*)"
            )
        rgx = re.match(pattern, value, re.UNICODE)
        if not rgx:
            raise ChordError("Chord could not be recognised")
        self.key = self._parse_key(rgx)
        self.quality = self._parse_quality(rgx)
        self.other = self._parse_other(rgx)
        self.major_minor = self._maj_min_str(rgx)
        self._name = str(self.key) + self.major_minor + self.other

    def _parse_key(self, rgx):
        note = rgx.group(1)
        accidental = rgx.group(2) or ''
        return Key(note + accidental)

    def _parse_quality(self, rgx):
        if not rgx.group(3) and rgx.group(1).isupper():
            # No quality, capital letter key
            return 'major'
        elif not rgx.group(3):
            # lowercase key
            return 'minor'
        elif rgx.group(4):
            return 'major'
        else:
            return 'minor'

    def _parse_other(self, rgx):
        return rgx.group(6)

    def _maj_min_str(self, rgx):
        """Print major if seventh chord."""
        if self.quality == 'minor':
            return 'm'
        if rgx.group(4) and re.match('7', self.other):
            return rgx.group(4)
        else:
            return ''

    def transpose(self, value: int = 0, flats=False):
        if not isinstance(value, int):
            raise TransposeError("Only integers are accepted")
        if flats:
            self.key.use_flats()
        self.key.transpose(value)
        self.name = str(self.key) + self.major_minor + self.other
        return self

    def __repr__(self):
        return f'{self.name} chord'
