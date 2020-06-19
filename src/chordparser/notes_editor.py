from .notes import Note
from typing import Union
import re


class NoteEditor:
    """
    NoteEditor class that can create a Note and get intervals between Notes.

    The NoteEditor class can create a Note using the 'create_note' method by accepting a string with notation a-g or A-G and optional accidental symbols. The symbols that can be used are b (flat), bb (doubleflat), # (sharp), ## (doublesharp) and their respective unicode characters.

    The NoteEditor can also find the intervals between two Notes using the 'get_interval' method. The method measures the interval of the second Note from the first Note and is expressed in semitones.
    """
    _flat = '\u266d'
    _sharp = '\u266f'
    _doubleflat = '\U0001D12B'
    _doublesharp = '\U0001D12A'
    _symbol_converter = {
        _flat: _flat, _doubleflat: _doubleflat,
        _sharp: _sharp, _doublesharp: _doublesharp,
        'b': _flat, 'bb': _doubleflat,
        '#': _sharp, '##': _doublesharp,
        None: '',
    }

    def create_note(self, value):
        """Create a Note from a string."""
        if not isinstance(value, str):
            raise TypeError("Only strings are accepted")
        pattern = (
            '^([a-gA-G])(\u266F|\u266D|\U0001D12B|\U0001D12A'
            '|bb|##|b|#){0,1}$'
            )
        rgx = re.match(pattern, value, re.UNICODE)
        if not rgx:
            raise ValueError("Note is invalid")
        letter = rgx.group(1).upper()
        symbol = NoteEditor._symbol_converter.get(rgx.group(2))
        notation = letter + symbol
        return Note(notation)

    def get_interval(self, note_1, note_2):
        """Get interval of second Note from first Note in semitones."""
        val_1 = note_1.num_value()
        val_2 = note_2.num_value()
        return (val_2 - val_1) % 12


