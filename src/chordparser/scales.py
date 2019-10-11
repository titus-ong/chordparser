"""
Accept key and mode, and return scale with notes.
"""
from .general import Error, TransposeError
from .notes import Note, Key
from typing import Union
import re


class ModeError(Error):
    pass


class Scale:
    _heptatonic_base = (2, 2, 1, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 1)
    _SCALES = {
        "major": 0,
        "ionian": 0,
        "dorian": 1,
        "phrygian": 2,
        "lydian": 3,
        "mixolydian": 4,
        "aeolian": 5,
        "minor": 5,
        "locrian": 6,
        }
    _SCALE_DEGREE = {
        0: "ionian",
        1: "dorian",
        2: "phrygian",
        3: "lydian",
        4: "mixolydian",
        5: "aeolian",
        6: "locrian",
    }
    _notes = ('C', 'D', 'E', 'F', 'G', 'A', 'B',
              'C', 'D', 'E', 'F', 'G', 'A', 'B')

    def __init__(self, key: Union[str, Note], mode: str = "major"):
        self.key = key
        self.mode = mode
        self.intervals = self._get_scale_intervals()
        self.notes = None

    @property
    def key(self):
        return self._key

    @key.setter
    def key(self, value):
        if isinstance(value, Note):
            self._key = Key(value.value)
        else:
            self._key = Key(value)

    @property
    def mode(self):
        return self._mode

    @mode.setter
    def mode(self, value):
        if not isinstance(value, str):
            raise ModeError("Only strings are accepted")
        elif value.lower() not in Scale._SCALES:
            raise ModeError("Mode could not be found")
        else:
            self._mode = value.lower()

    def _get_scale_intervals(self, custom_mode=None):
        mode = custom_mode or self.mode
        shift = Scale._SCALES[mode.lower()]
        scale_intervals = (
            Scale._heptatonic_base[shift:]
            + Scale._heptatonic_base[:shift]
            )
        return scale_intervals

    @property
    def notes(self):
        return self._notes

    @notes.setter
    def notes(self, _):
        self.idx = Scale._notes.index(self.key.letter())
        self._note_order = self._get_note_order()
        self._notes = self._add_note_symbols()

    def _get_note_order(self):
        note_order = Scale._notes[self.idx:] + Scale._notes[:self.idx]
        return note_order

    def _add_note_symbols(self):
        base_intervals = self._get_scale_intervals(
                Scale._SCALE_DEGREE[self.idx]
                )
        symbol_increment = self.key.symbolvalue()
        note_list = []
        for num, note in enumerate(self._note_order):
            new_note = Note(note)
            total_increment = (
                symbol_increment
                + sum(self.intervals[:num])
                - sum(base_intervals[:num])
                )
            new_note.shift(total_increment)
            note_list.append(new_note)
        return tuple(note_list)

    def transpose(self, value: int = 0, flats=False):
        if not isinstance(value, int):
            raise TransposeError("Only integers are accepted")
        if flats:
            self.key.use_flats()
        self.key.transpose(value)
        self.notes = None  # refresh notes
        return self

    def __repr__(self):
        return f'{self.key} {self.mode} scale'
