from .general import Error, TransposeError
from typing import Union
import re


class NoteError(Error):
    pass


class NoteSymbolError(Error):
    pass


class ModeError(Error):
    pass


class SubmodeError(Error):
    pass


class Note:
    """
    Create a Note.

    Arguments:
    value -- the Note value (str)

    The Note class consists of notation a-g or A-G, with optional accidental symbols. The symbols that can be used are b (flat), bb (doubleflat), # (sharp), ## (doublesharp) and their respective unicode characters.

    Notes can have accidentals set using the 'accidental' method, and can be shifted by semitones using the 'shift' method. Notes also have 'letter', 'symbol', and 'symbolvalue' methods to get their respective values.
    """
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
        pattern = (
            '^([a-gA-G])(\u266F|\u266D|\U0001D12B|\U0001D12A'
            '|bb|##|b|#){0,1}$'
            )
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


class Key:
    """
    Create a Key.

    Arguments:
    value -- the note of the Key (str)

    Keyword arguments:
    mode -- the mode of the Key (default 'major') (str)
    submode -- the submode (default None) (str)

    The Key class composes of a Note class with the additional attributes 'mode' and 'submode' (e.g. types of minor keys). Keys have the same methods as Notes, with an additional 'transpose' and 'use_flats'/'use_sharps' methods for transposing.

    The Key class only accepts the western heptatonic modes and submodes for now.
    """
    _note_values = {
        ('C' + Note._doubleflat): 10,
        ('C' + Note._flat): 11,
        'C': 0,
        ('C' + Note._sharp): 1,
        ('C' + Note._doublesharp): 2,
        ('D' + Note._doubleflat): 0,
        ('D' + Note._flat): 1,
        'D': 2,
        ('D' + Note._sharp): 3,
        ('D' + Note._doublesharp): 4,
        ('E' + Note._doubleflat): 2,
        ('E' + Note._flat): 3,
        'E': 4,
        ('E' + Note._sharp): 5,
        ('E' + Note._doublesharp): 6,
        ('F' + Note._doubleflat): 3,
        ('F' + Note._flat): 4,
        'F': 5,
        ('F' + Note._sharp): 6,
        ('F' + Note._doublesharp): 7,
        ('G' + Note._doubleflat): 5,
        ('G' + Note._flat): 6,
        'G': 7,
        ('G' + Note._sharp): 8,
        ('G' + Note._doublesharp): 9,
        ('A' + Note._doubleflat): 7,
        ('A' + Note._flat): 8,
        'A': 9,
        ('A' + Note._sharp): 10,
        ('A' + Note._doublesharp): 11,
        ('B' + Note._doubleflat): 9,
        ('B' + Note._flat): 10,
        'B': 11,
        ('B' + Note._sharp): 0,
        ('B' + Note._doublesharp): 1,
        }
    _sharp_scale = (
        'C', 'C\u266f', 'D', 'D\u266f', 'E', 'F', 'F\u266f',
        'G', 'G\u266f', 'A', 'A\u266f', 'B'
        )
    _flat_scale = (
        'C', 'D\u266d', 'D', 'E\u266d', 'E', 'F',
        'G\u266d', 'G', 'A\u266d', 'A', 'B\u266d', 'B'
        )
    _modes = (
        'major', 'minor', 'ionian', 'dorian', 'phrygian',
        'lydian', 'mixolydian', 'aeolian', 'locrian'
        )
    _submodes = {'minor': ('harmonic', 'melodic', 'natural')}

    def __init__(
            self, value, mode: str = 'major',
            submode: Union[str, None] = None):
        self.note = Note(value)
        self.mode = mode
        self.submode = submode
        self.flats_on = False

    @property
    def mode(self):
        return self._mode

    @mode.setter
    def mode(self, value):
        if not isinstance(value, str):
            raise ModeError("Only strings are accepted")
        if value.lower() not in Key._modes:
            raise ModeError("Mode could not be found")
        else:
            self._mode = value.lower()

    @property
    def submode(self):
        return self._submode

    @submode.setter
    def submode(self, value):
        if value is None:
            self._submode = value
            return
        elif not isinstance(value, str):
            raise SubmodeError("Only strings are accepted")
        submode_tuple = Key._submodes.get(self.mode)
        if submode_tuple is None:
            raise SubmodeError("Mode does not have any submodes")
        if value.lower() not in submode_tuple:
            raise SubmodeError("Submode could not be found")
        else:
            self._submode = value.lower()

    def transpose(self, value=0):
        if not isinstance(value, int):
            raise TransposeError("Only integers are accepted")
        number = Key._note_values.get(self.note.value)
        number += value
        if self.flats_on:
            dic = Key._flat_scale
        else:
            dic = Key._sharp_scale
        self.note.value = dic[number % 12]

    def use_flats(self):
        self.flats_on = True

    def use_sharps(self):
        self.flats_on = False

    def __getattr__(self, attribute):
        if attribute in Note.__dict__:
            # So Note methods can be used on Key
            return getattr(self.note, attribute)

    def __repr__(self):
        if not self.submode:
            return f'{self.note} {self.mode}'
        else:
            return f'{self.note} {self.submode} {self.mode}'

    def __eq__(self, other):
        if not isinstance(other, Key):
            return NotImplemented
        else:
            return (
                self.note == other.note
                and self.mode == other.mode
                and self.submode == other.submode
                )
