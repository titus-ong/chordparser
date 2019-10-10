"""
Note class.
"""
from .general import Error
import re


class NoteError(Error):
    pass


class NoteSymbolError(Error):
    pass


class Note:
    _flat = '\u266d'
    _sharp = '\u266f'
    _doubleflat = '\U0001D12B'
    _doublesharp = '\U0001D12A'
    _symbols = {
        _flat: -1, _doubleflat: -2,
        _sharp: +1, _doublesharp: +2,
        -1: _flat, -2: _doubleflat,
        +1: _sharp, +2: _doublesharp,
        0: '', None: 0,
        }

    def __init__(self, value):
        self.value = value

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value: str):
        if not isinstance(value, str):
            raise NoteError("Only strings are accepted")
        if not re.match(
                '^[a-gA-G](\u266F|\u266D|\U0001D12B|\U0001D12A){0,1}$',
                value, re.UNICODE):
            raise NoteError("Note does not exist")
        else:
            self._value = value

    def accidental(self, value: int):
        if not isinstance(value, int) or value not in {-2, -1, 0, 1, 2}:
            raise NoteSymbolError(
                "Only integers between -2 and 2 are accepted"
                )
        else:
            self.value = self.value[0] + Note._symbols.get(value)

    def shift(self, value: int):
        if not isinstance(value, int) or value not in {-2, -1, 0, 1, 2}:
            raise NoteSymbolError(
                "Only integers between -2 and 2 are accepted"
                )
        if len(self.value) > 1:
            value += Note._symbols.get(self.value[1])
        if value not in {-2, -1, 0, 1, 2}:
            raise NoteSymbolError(
                "Only symbols up to doublesharps and doubleflats are accepted"
                )
        self.value = self.value[0] + Note._symbols.get(value)

    def letter(self):
        return self.value[0]

    def symbol(self) -> str:
        if len(self.value) > 1:
            return self.value[1]
        else:
            return None

    def symbolvalue(self) -> int:
        if len(self.value) > 1:
            symbol = self.value[1]
        else:
            symbol = None
        return Note._symbols.get(symbol)

    def __repr__(self):
        return self.value

    def __eq__(self, other):
        if isinstance(other, Note):
            return self.value == other.value
        elif isinstance(other, str):
            return self.value == other
        else:
            return NotImplemented
