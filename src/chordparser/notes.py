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
    _symbol_converter = {
        _flat: _flat, _doubleflat: _doubleflat,
        _sharp: _sharp, _doublesharp: _doublesharp,
        'b': _flat, 'bb': _doubleflat,
        '#': _sharp, '##': _doublesharp,
        None: '',
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
        pattern = '^([a-gA-G])(\u266F|\u266D|\U0001D12B|\U0001D12A|bb|##|b|#){0,1}$'
        rgx = re.match(pattern, value, re.UNICODE)
        if not rgx:
            raise NoteError("Note is invalid")
        letter_ = rgx.group(1).upper()
        symbol_ = Note._symbol_converter.get(rgx.group(2))
        self._value = letter_ + symbol_

    def accidental(self, value: int):
        if not isinstance(value, int) or value not in {-2, -1, 0, 1, 2}:
            raise NoteSymbolError(
                "Only integers between -2 and 2 are accepted"
                )
        else:
            self.value = self.letter() + Note._symbols.get(value)

    def shift(self, value: int):
        if not isinstance(value, int):
            raise NoteSymbolError("Only integers are accepted")
        value += self.symbolvalue()
        if value not in {-2, -1, 0, 1, 2}:
            raise NoteSymbolError(
                "Only symbols up to doublesharps and doubleflats are accepted"
                )
        self.value = self.letter() + Note._symbols.get(value)

    def letter(self) -> str:
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
