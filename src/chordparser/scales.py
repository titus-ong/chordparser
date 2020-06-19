from .notes import Note
from .keys import Key
from typing import Union
import re


class Scale:
    """
    Scale class that composes of a Key and Notes.

    Arguments:
    key -- the key of the Scale (Key)

    The Scale class accepts a Key and generates a 2-octave Note tuple in its 'notes' attribute.

    The Scale can be changed by setting its 'key' attribute, or by transposing it using the 'transpose' method.
    """
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
    _submodes = {
        None: (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
        "natural": (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
        "melodic": (0, 0, 0, 0, 1, 0, -1, 0, 0, 0, 0, 1, 0, -1),
        "harmonic": (0, 0, 0, 0, 0, 1, -1, 0, 0, 0, 0, 0, 1, -1),
    }
    _notes_tuple = (
        'C', 'D', 'E', 'F', 'G', 'A', 'B',
        'C', 'D', 'E', 'F', 'G', 'A', 'B')

    def __init__(self, key: Key):
        self.key = key

    @property
    def key(self):
        """Key getter."""
        return self._key

    @key.setter
    def key(self, value):
        """Key setter - check if key is valid and re-create the scale."""
        if not isinstance(value, Key):
            try:
                self._key = Key(value)
            except TypeError:
                raise TypeError("Only Keys, Notes and strings are accepted")
        else:
            self._key = value
        self._refresh()

    def _refresh(self):
        """Re-create the scale."""
        self.notes = self._get_notes()

    def _get_notes(self):
        """Get notes in the scale."""
        self.scale_intervals = self._get_scale_intervals()
        note_no_symbol = Note(self.key.letter())
        self._idx = Scale._notes_tuple.index(note_no_symbol)
        self._note_order = self._get_note_order()
        notes = self._shift_notes()
        return notes

    def _get_scale_intervals(self):
        """Get note-by-note intervals in the scale."""
        intervals = self._get_intervals(self.key.mode)
        # Account for submode
        submode_intervals = Scale._submodes.get(self.key.submode)
        scale_intervals = []
        for scale, subm in zip(intervals, submode_intervals):
            scale_intervals.append(scale + subm)
        return tuple(scale_intervals)

    def _get_intervals(self, mode):
        """Get intervals based on mode."""
        shift = Scale._SCALES[mode]
        intervals = (
            Scale._heptatonic_base[shift:]
            + Scale._heptatonic_base[:shift]
            )
        return intervals

    def _get_note_order(self):
        """Re-arrange note order based on key."""
        note_order = (
            Scale._notes_tuple[self._idx:]
            + Scale._notes_tuple[:self._idx]
            )
        return note_order

    def _shift_notes(self):
        """Shift notes with reference to original mode intervals."""
        base_intervals = self._get_intervals(
                Scale._SCALE_DEGREE[self._idx]
                )
        symbol_increment = self.key.symbolvalue()
        note_list = []
        for num, note in enumerate(self._note_order):
            new_note = Note(note)
            total_increment = (
                symbol_increment
                + sum(self.scale_intervals[:num])
                - sum(base_intervals[:num])
                )
            new_note.shift(total_increment)
            note_list.append(new_note)
        return tuple(note_list)

    def transpose(self, value: int = 0, use_flats: bool = False):
        """Transpose key of the scale."""
        if not isinstance(value, int):
            raise TypeError("Only integers are accepted")
        self.key.transpose(value, use_flats=use_flats)
        return self

    def __repr__(self):
        return f'{self.key} scale'
