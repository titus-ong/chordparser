import re

from chordparser.music.notes import Note


class NoteEditor:
    """
    NoteEditor class that can create a Note and get intervals between Notes.

    The NoteEditor class can create a Note using the 'create_note' method by accepting a string with notation a-g or A-G and optional accidental symbols. The symbols that can be used are b (flat), bb (doubleflat), # (sharp), ## (doublesharp) and their respective unicode characters.

    The NoteEditor can also find the intervals between Notes using the 'get_intervals', 'get_min_intervals' and 'get_tone_notes' methods. The 'change_note' method allows for changing a note's value.
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
    _pattern = (
        '^([a-gA-G])(\u266F|\u266D|\U0001D12B|\U0001D12A'
        '|bb|##|b|#){0,1}$'
    )

    def create_note(self, value):
        """Create a Note from a string."""
        letter, symbol = self._parse_note(value)
        return Note(letter, symbol)

    def _parse_note(self, value):
        """Parse the note string."""
        rgx = re.match(NoteEditor._pattern, value, re.UNICODE)
        if not rgx:
            raise SyntaxError(f"'{value}' could not be parsed")
        letter = rgx.group(1).upper()
        symbol = NoteEditor._symbol_converter.get(rgx.group(2))
        return letter, symbol

    def get_tone_letter(self, *notes):
        """Return a nested tuple of (semitone interval, letter interval) between notes."""
        semitones = self.get_intervals(*notes)
        letters = self.get_letter_intervals(*notes)
        return tuple(zip(semitones, letters))

    def get_letter_intervals(self, *notes):
        """Return a tuple of letter intervals between notes."""
        old_note = NoteEditor._notes_tuple.index(notes[0].letter)
        note_diff = []
        for each in notes:
            new_note = NoteEditor._notes_tuple.index(each.letter)
            note_diff.append((new_note - old_note) % 7)
            old_note = new_note
        note_diff.pop(0)
        return tuple(note_diff)

    def get_intervals(self, *notes):
        """Return a tuple of semitone intervals between notes."""
        old_val = notes[0].num_value()
        intervals = []
        for each in notes:
            new_val = each.num_value()
            intervals.append((new_val - old_val) % 12)
            old_val = new_val
        intervals.pop(0)
        return tuple(intervals)

    def get_min_intervals(self, *notes):
        """Return a tuple of the shortest semitone distance between notes."""
        intervals = self.get_intervals(*notes)
        min_int = []
        for each in intervals:
            if each > (12 - each):
                shift = each - 12
            else:
                shift = each
            min_int.append(shift)
        return tuple(min_int)

    def change_note(self, note, value, inplace=True):
        """Change a note's value. Use inplace=True to return a new note."""
        if not inplace:
            note = self.create_note("C")
        note.letter, note.symbol = self._parse_note(value)
        return note
