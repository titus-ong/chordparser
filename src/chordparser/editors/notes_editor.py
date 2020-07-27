import re

from chordparser.music.notes import Note


class NoteEditor:
    """A `Note` editor that can create `Notes` and manipulate them.

    The `NoteEditor` can create a `Note` from its notation and change it by specifying a different notation. It can also get semitone and letter intervals between `Notes`.

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

    def create_note(self, notation):
        """Create a `Note` from its notation.

        Accepts a-g or A-G and optional accidental symbols (b, bb, #, ##, or their respective unicode characters \u266d, \u266f, \U0001D12B, or \U0001D12A).

        Parameters
        ----------
        notation : str
            The notation of the `Note`.

        Returns
        -------
        Note
            A `Note` object with value equal to its notation.

        Raises
        ------
        SyntaxError
            If the notation does not follow accepted notation.

        Examples
        --------
        >>> NE = NoteEditor()
        >>> NE.create_note("C")
        C note
        >>> NE.create_note("D#")
        D\u266f note

        """
        letter, symbol = self._parse_note(notation)
        return Note(letter, symbol)

    def _parse_note(self, notation):
        """Parse the note string."""
        rgx = re.match(NoteEditor._pattern, notation, re.UNICODE)
        if not rgx:
            raise SyntaxError(f"'{notation}' could not be parsed")
        letter = rgx.group(1).upper()
        symbol = NoteEditor._symbol_converter.get(rgx.group(2))
        return letter, symbol

    def get_tone_letter(self, *notes):
        """Get the semitone and letter intervals between `Notes`.

        Multiple `Notes` as arguments are accepted. The intervals for each `Note` are relative to the previous `Note`.

        Parameters
        ----------
        *notes : Note
            Any number of `Notes`.

        Returns
        -------
        tuple of (int, int)
            The nested tuple of semitone and letter intervals between all adjacent `Notes`. The inner tuple is the semitone and letter intervals between two adjacent `Notes`.

        Examples
        --------
        >>> NE = NoteEditor()
        >>> c = NE.create_note("C")
        >>> f = NE.create_note("F")
        >>> a = NE.create_note("A")
        >>> NE.get_tone_letter(c, f, a)
        ((5, 3), (4, 2))

        """
        semitones = self.get_intervals(*notes)
        letters = self.get_letter_intervals(*notes)
        return tuple(zip(semitones, letters))

    def get_letter_intervals(self, *notes):
        """Get the letter intervals between `Notes`.

        Multiple `Notes` as arguments are accepted. The interval for each `Note` is relative to the previous `Note`.

        Parameters
        ----------
        *notes : Note
            Any number of `Notes`.

        Returns
        -------
        tuple of int
            The tuple of letter intervals between all adjacent `Notes`.

        Examples
        --------
        >>> NE = NoteEditor()
        >>> c = NE.create_note("C")
        >>> f = NE.create_note("F")
        >>> a = NE.create_note("A")
        >>> NE.get_letter_intervals(c, f, a)
        (3, 2)

        """
        old_note = NoteEditor._notes_tuple.index(notes[0].letter)
        note_diff = []
        for each in notes:
            new_note = NoteEditor._notes_tuple.index(each.letter)
            note_diff.append((new_note - old_note) % 7)
            old_note = new_note
        note_diff.pop(0)
        return tuple(note_diff)

    def get_intervals(self, *notes):
        """Get the semitone intervals between `Notes`.

        Multiple `Notes` as arguments are accepted. The interval for each `Note` is relative to the previous `Note`.

        Parameters
        ----------
        *notes : Note
            Any number of `Notes`.

        Returns
        -------
        tuple of int
            The tuple of semitone intervals between all adjacent `Notes`.

        Examples
        --------
        >>> NE = NoteEditor()
        >>> c = NE.create_note("C")
        >>> f = NE.create_note("F")
        >>> a = NE.create_note("A")
        >>> NE.get_intervals(c, f, a)
        (5, 4)

        """
        old_val = notes[0].num_value()
        intervals = []
        for each in notes:
            new_val = each.num_value()
            intervals.append((new_val - old_val) % 12)
            old_val = new_val
        intervals.pop(0)
        return tuple(intervals)

    def get_min_intervals(self, *notes):
        """Get the shortest semitone distance between `Notes`.

        Multiple `Notes` as arguments are accepted. The distance for each `Note` is relative to the previous `Note`.

        Parameters
        ----------
        *notes : Note
            Any number of `Notes`.

        Returns
        -------
        tuple of int
            The tuple of the shortest semitone distances between all adjacent `Notes`.

        Examples
        --------
        >>> NE = NoteEditor()
        >>> c = NE.create_note("C")
        >>> b = NE.create_note("B")
        >>> NE.get_intervals(c, b)
        (11,)
        >>> NE.get_min_intervals(c, b)
        (-1,)

        """
        intervals = self.get_intervals(*notes)
        min_int = []
        for each in intervals:
            if each > (12 - each):
                shift = each - 12
            else:
                shift = each
            min_int.append(shift)
        return tuple(min_int)

    def change_note(self, note, notation, inplace=True):
        """Change a `Note`'s notation.

        Accepts a-g or A-G and optional accidental symbols (b, bb, #, ##, or their respective unicode characters \u266d, \u266f, \U0001D12B, or \U0001D12A).

        Parameters
        ----------
        note : Note
            The `Note` which value you want to change.
        notation : str
            The new notation for the `Note`.
        inplace : boolean, optional
            Selector to change the notation of current `Note` or to return a new `Note`. Default True when optional.

        Returns
        -------
        Note
            The `Note` with the new notation.

        Examples
        --------
        >>> NE = NoteEditor()
        >>> a = NE.create_note("A")
        >>> NE.change_note(a, "Bb")
        B\u266d note
        >>> NE.change_note(a, "C#", inplace=False)
        C\u266f note
        >>> a
        B\u266d note

        """
        if not inplace:
            note = self.create_note("C")
        note.letter, note.symbol = self._parse_note(notation)
        return note
