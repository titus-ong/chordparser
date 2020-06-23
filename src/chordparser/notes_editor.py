from chordparser.notes import Note
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
    _notes_tuple = (
        'C', 'D', 'E', 'F', 'G', 'A', 'B',
        'C', 'D', 'E', 'F', 'G', 'A', 'B')

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

    def get_tone_notes(self, *notes):
        """Return a tuple of (semitone, note) differences between notes."""
        semitones = self.get_intervals(*notes)
        old_note = self._notes_tuple.index(notes[0].letter())
        note_diff = []
        for each in notes:
            new_note = self._notes_tuple.index(each.letter())
            note_diff.append((new_note-old_note) % 8)
            old_note = new_note
        note_diff.pop(0)
        return tuple(zip(semitones, note_diff))

    def get_intervals(self, *notes):
        """Return a tuple of intervals between notes in semitones."""
        old_val = notes[0].num_value()
        intervals = []
        for each in notes:
            new_val = each.num_value()
            intervals.append((new_val-old_val) % 12)
            old_val = new_val
        intervals.pop(0)
        return tuple(intervals)

    def get_min_intervals(self, *notes):
        intervals = self.get_intervals(*notes)
        min_int = []
        for each in intervals:
            if each > (12-each):
                shift = each-12
            else:
                shift = each
            min_int.append(shift)
        return tuple(min_int)
