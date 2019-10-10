"""
Basis of chords. Only diatonic scales are included.
"""
from .general import Error
import re


class ModeError(Error):
    pass


class KeySignatureError(Error):
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
    _flat = '\u266d'
    _sharp = '\u266f'
    _doubleflat = '\U0001D12B'
    _doublesharp = '\U0001D12A'
    _symbols = {
        _flat: -1, _doubleflat: -2,
        _sharp: +1, _doublesharp: +2,
        -1: _flat, -2: _doubleflat,
        +1: _sharp, +2: _doublesharp,
        0: '',
        }

    def __init__(self, key, mode="major"):
        self.key = key  # Implement method to check if key is valid
        # How to know Cmaj7 is major and Cm7 is minor?
        self.mode = mode
        self.intervals = self._get_scale_intervals()
        self.notes = self._get_notes()

    def _get_scale_intervals(self, custom_mode=None):
        mode = custom_mode or self.mode
        try:
            shift = Scale._SCALES[mode.lower()]
        except KeyError:
            raise ModeError("Mode cannot be found")
        scale_intervals = (
            Scale._heptatonic_base[shift:]
            + Scale._heptatonic_base[:shift]
            )
        return scale_intervals

    def _get_notes(self):
        if not re.match(
                        '^[a-gA-G](\u266F|\u266D|\U0001D12B|\U0001D12A){0,1}$',
                        self.key, re.UNICODE):
            raise KeySignatureError("Key signature does not exist")
        self.idx = Scale._notes.index(self.key[0])
        self._note_order = self._get_note_order()
        return self._add_note_symbols()

    def _get_note_order(self):
        note_order = Scale._notes[self.idx:] + Scale._notes[:self.idx]
        return note_order

    def _add_note_symbols(self):
        base_intervals = self._get_scale_intervals(
                Scale._SCALE_DEGREE[self.idx]
                )
        if len(self.key) > 1:
            symbol_increment = Scale._symbols[self.key[1]]
        else:
            symbol_increment = 0
        note_list = []
        for num, note in enumerate(self._note_order):
            total_increment = (
                symbol_increment
                + sum(self.intervals[:num])
                - sum(base_intervals[:num])
                )
            note_list.append(note + Scale._symbols[total_increment])
        return tuple(note_list)
