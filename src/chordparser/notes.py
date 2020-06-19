from typing import Union
import re


class Note:
    """
    Note class that composes of a note value.

    Arguments:
    value -- the Note value (str)

    The Note class consists of notation a-g or A-G, with optional unicode accidental symbols \u266d, \u266f, \U0001D12B, or \U0001D12A.

    Notes can have accidentals set using the 'accidental' method, and can be shifted by semitones using the 'shift' method. Notes also have 'letter', 'symbol', and 'symbolvalue' methods to get their respective values. Notes can be transposed using the 'transpose' method (flats can be toggled using the 'use_flats' kwarg).
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
    _note_values = {
        ('C' + _doubleflat): 10,
        ('C' + _flat): 11,
        'C': 0,
        ('C' + _sharp): 1,
        ('C' + _doublesharp): 2,
        ('D' + _doubleflat): 0,
        ('D' + _flat): 1,
        'D': 2,
        ('D' + _sharp): 3,
        ('D' + _doublesharp): 4,
        ('E' + _doubleflat): 2,
        ('E' + _flat): 3,
        'E': 4,
        ('E' + _sharp): 5,
        ('E' + _doublesharp): 6,
        ('F' + _doubleflat): 3,
        ('F' + _flat): 4,
        'F': 5,
        ('F' + _sharp): 6,
        ('F' + _doublesharp): 7,
        ('G' + _doubleflat): 5,
        ('G' + _flat): 6,
        'G': 7,
        ('G' + _sharp): 8,
        ('G' + _doublesharp): 9,
        ('A' + _doubleflat): 7,
        ('A' + _flat): 8,
        'A': 9,
        ('A' + _sharp): 10,
        ('A' + _doublesharp): 11,
        ('B' + _doubleflat): 9,
        ('B' + _flat): 10,
        'B': 11,
        ('B' + _sharp): 0,
        ('B' + _doublesharp): 1,
        }
    _sharp_scale = (
        'C', 'C\u266f', 'D', 'D\u266f', 'E', 'F', 'F\u266f',
        'G', 'G\u266f', 'A', 'A\u266f', 'B'
        )
    _flat_scale = (
        'C', 'D\u266d', 'D', 'E\u266d', 'E', 'F',
        'G\u266d', 'G', 'A\u266d', 'A', 'B\u266d', 'B'
        )

    def __init__(self, value):
        self.value = value

    def accidental(self, value: int):
        """Change a note's accidental by specifying a value from -2(doubleflat) to 2(doublesharp)."""
        if not isinstance(value, int):
            raise TypeError("Only integers are accepted")
        if value not in {-2, -1, 0, 1, 2}:
            raise ValueError(
                "Only integers between -2 and 2 are accepted"
                )
        self.value = self.letter() + Note._symbols.get(value)
        return self

    def shift(self, value: int):
        """Shift a note's accidental by specifying a value."""
        if not isinstance(value, int):
            raise TypeError("Only integers are accepted")
        value += self.symbolvalue()
        if value not in {-2, -1, 0, 1, 2}:
            raise ValueError(
                "Only symbols up to doublesharps and doubleflats are accepted"
                )
        self.value = self.letter() + Note._symbols.get(value)
        return self

    def num_value(self) -> int:
        """Return numerical value."""
        return Note._note_values[self.value]

    def letter(self) -> str:
        """Return note letter."""
        return self.value[0]

    def symbol(self) -> str:
        """Return note symbol."""
        if len(self.value) > 1:
            return self.value[1]
        return None

    def symbolvalue(self) -> int:
        """Return note symbol as a integer value."""
        if len(self.value) > 1:
            symbol = self.value[1]
        else:
            symbol = None
        return Note._symbols.get(symbol)

    def transpose(self, value=0, use_flats: bool = False):
        """Transpose a note by specifying a value. Use flats if use_flats=True."""
        if not isinstance(value, int):
            raise TypeError("Only integers are accepted")
        number = Note._note_values.get(self.value)
        number += value
        if use_flats:
            dic = Note._flat_scale
        else:
            dic = Note._sharp_scale
        self.value = dic[number % 12]
        return self

    def __repr__(self):
        return self.value

    def __eq__(self, other):
        # Allow comparison between note values
        if isinstance(other, Note):
            return self.value == other.value
        elif isinstance(other, str):
            return self.value == other
        else:
            return NotImplemented


class Key:
    """
    Key class that composes of a note as the root, and its mode and submode.

    Arguments:
    value -- the note of the Key (str)

    Keyword arguments:
    mode -- the mode of the Key (default 'major') (str)
    submode -- the submode (default None) (str)

    The Key class composes of a Note class with the additional attributes 'mode' and 'submode' (e.g. types of minor keys). Keys have the same methods as Notes, with an additional 'transpose' and 'use_flats'/'use_sharps' methods for transposing.

    The Key class only accepts the western heptatonic modes and submodes for now.
    """
    _modes = (
        'major', 'minor', 'ionian', 'dorian', 'phrygian',
        'lydian', 'mixolydian', 'aeolian', 'locrian'
        )
    _submodes = {'minor': ('harmonic', 'melodic', 'natural')}

    def __init__(
            self, value, mode: str = 'major',
            submode: Union[str, None] = None):
        self.root = value
        self.mode = mode
        self.submode = submode

    @property
    def root(self):
        """Root getter."""
        return self._root

    @root.setter
    def root(self, value):
        """Root setter - check if root is a valid Note."""
        if not isinstance(value, Note):
            try:
                self._root = Note(value)
            except TypeError:
                raise TypeError("Only Notes and strings are accepted")
        else:
            self._root = value

    @property
    def mode(self):
        """Mode getter"""
        return self._mode

    @mode.setter
    def mode(self, value):
        """Mode setter - check if mode is valid."""
        if not isinstance(value, str):
            raise TypeError("Only strings are accepted")
        if value.lower() not in Key._modes:
            raise KeyError("Mode could not be found")
        self._mode = value.lower()

    @property
    def submode(self):
        """Submode getter."""
        return self._submode

    @submode.setter
    def submode(self, value):
        """Submode setter - check if submode is valid with reference to mode."""
        if value is None:
            self._submode = value
            return
        if not isinstance(value, str):
            raise TypeError("Only strings are accepted")
        submode_tuple = Key._submodes.get(self.mode)
        if submode_tuple is None:
            raise KeyError("Mode does not have any submodes")
        if value.lower() not in submode_tuple:
            raise KeyError("Submode could not be found")
        self._submode = value.lower()

    def __getattr__(self, attribute):
        # So Note methods can be used on Key
        if attribute in Note.__dict__:
            return getattr(self.root, attribute)

    def __repr__(self):
        if not self.submode:
            return f'{self.root} {self.mode}'
        return f'{self.root} {self.submode} {self.mode}'

    def __eq__(self, other):
        # Allow comparison between Keys by checking their basic attributes
        if not isinstance(other, Key):
            return NotImplemented
        return (
                self.root == other.root
                and self.mode == other.mode
                and self.submode == other.submode
                )
