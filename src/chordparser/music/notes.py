class Note:
    """A class representing a musical note.

    The `Note` class consists of notation A-G with optional unicode accidental symbols \u266d, \u266f, \U0001D12B, or \U0001D12A. It is created by the `NoteEditor`.

    Parameters
    ----------
    letter : str
        The letter part of the `Note`'s notation. Consists of A-G.
    symbol : str
        The accidental part of the `Note`'s notation. Consists of the unicode characters \u266d, \u266f, \U0001D12B, or \U0001D12A. If there are no accidentals, it is an empty string.

    Attributes
    ----------
    letter : str
        The letter part of the `Note`'s notation.
    symbol : str
        The accidental part of the `Note`'s notation.

    """

    _flat = '\u266d'
    _sharp = '\u266f'
    _doubleflat = '\U0001D12B'
    _doublesharp = '\U0001D12A'
    _symbols = {
        -1: _flat, -2: _doubleflat,
        +1: _sharp, +2: _doublesharp,
        0: '',
    }
    _symbol_signs = {
        _flat: -1, _doubleflat: -2,
        _sharp: 1, _doublesharp: 2,
        '': 0,
    }
    _note_values = {  # Basis: C = 0
        'C': 0,
        'D': 2,
        'E': 4,
        'F': 5,
        'G': 7,
        'A': 9,
        'B': 11,
    }
    _notes_tuple = (
        'C', 'D', 'E', 'F', 'G', 'A', 'B',
        'C', 'D', 'E', 'F', 'G', 'A', 'B',
    )
    _sharp_tuple = (
        ('C', ''), ('C', '\u266f'), ('D', ''), ('D', '\u266f'), ('E', ''),
        ('F', ''), ('F', '\u266f'), ('G', ''), ('G', '\u266f'), ('A', ''),
        ('A', '\u266f'), ('B', ''),
    )
    _flat_tuple = (
        ('C', ''), ('D', '\u266d'), ('D', ''), ('E', '\u266d'), ('E', ''),
        ('F', ''), ('G', '\u266d'), ('G', ''), ('A', '\u266d'), ('A', ''),
        ('B', '\u266d'), ('B', ''),
    )

    def __init__(self, letter, symbol):
        self.letter = letter
        self.symbol = symbol

    @property
    def value(self):
        """str: The full notation of the `Note`."""
        return self.letter + self.symbol

    def num_value(self):
        """Return the `Note`'s numerical value (basis: C = 0).

        The numerical value is based on the number of semitones above C.

        Returns
        -------
        int
            The numerical value.

        Examples
        --------
        >>> NE = NoteEditor()
        >>> d = NE.create_note("D")
        >>> d.num_value()
        2

        """
        num = (self.letter_value() + self.symbol_value()) % 12
        return num

    def letter_value(self):
        """Return the `Note`'s letter as an integer value (basis: C = 0).

        The value is based on the number of scale degrees above C.

        Returns
        -------
        int
            The letter's value.

        Examples
        --------
        >>> NE = NoteEditor()
        >>> d = NE.create_note("D")
        >>> d.letter_value()
        1

        """
        return Note._note_values[self.letter]

    def symbol_value(self):
        """Return the `Note`'s symbol as an integer value (basis: natural = 0).

        The value is based on the number of semitones away from the natural `Note`.

        Returns
        -------
        int
            The symbol's value.

        Examples
        --------
        >>> NE = NoteEditor()
        >>> d_sharp = NE.create_note("D#")
        >>> d_sharp.symbol_value()
        1

        """
        return Note._symbol_signs[self.symbol]

    def accidental(self, value: int):
        """Change a `Note`'s accidental by specifying a `value` from -2 to 2.

        The range of `values` [-2, 2] correspond to the values a symbol can take, from doubleflat (-2) to doublesharp (2).

        Parameters
        ----------
        value : int
            The accidental's integer value.

        Raises
        ------
        ValueError
            If `value` is not in the range of [-2, 2].

        Examples
        --------
        >>> NE = NoteEditor()
        >>> d_sharp = NE.create_note("D#")
        >>> d_sharp.accidental(-1)
        D\u266d note

        """
        if value not in range(-2, 3):
            raise ValueError(
                "Only integers between -2 and 2 are accepted"
            )
        self.symbol = Note._symbols[value]
        return self

    def shift_s(self, value: int):
        """Shift a `Note`'s accidental.

        The `Note`'s `symbol_value()` must be in the range of [-2, 2] after the shift, which corresponds to the values a symbol can take from doubleflat (-2) to doublesharp (2).

        Parameters
        ----------
        value : int
            The value of the shift in accidentals.

        Raises
        ------
        ValueError
            If the `Note`'s `symbol_value()` is not in the range of [-2, 2] after the shift.

        Examples
        --------
        >>> NE = NoteEditor()
        >>> d_sharp = NE.create_note("D#")
        >>> d_sharp.shift_s(-1)
        D note

        """
        value += self.symbol_value()
        if value not in range(-2, 3):
            raise ValueError(
                "Only symbols up to doublesharps and doubleflats are accepted"
            )
        self.symbol = Note._symbols[value]
        return self

    def shift_l(self, value: int):
        """Shift a `Note`'s letter.

        The `value` corresponds to the change in scale degree of the `Note`.

        Parameters
        ----------
        value : int
            The value of the letter shift.

        Examples
        --------
        >>> NE = NoteEditor()
        >>> d_sharp = NE.create_note("D#")
        >>> d_sharp.shift_l(3)
        G\u266f note

        """
        pos = (Note._notes_tuple.index(self.letter) + value) % 7
        new_letter = Note._notes_tuple[pos]
        self.letter = new_letter
        return self

    def transpose(self, semitones: int, letters: int):
        """Transpose a `Note` according to semitone and letter intervals.

        Parameters
        ----------
        semitones
            The difference in semitones to the new transposed `Note`.
        letters
            The difference in scale degrees to the new transposed `Note`.

        Examples
        --------
        >>> NE = NoteEditor()
        >>> c = NE.create_note("C")
        >>> c.transpose(6, 3)
        F\u266f note
        >>> c.transpose(0, 1)
        G\u266d note

        """
        new_val = (self.num_value() + semitones) % 12
        self.shift_l(letters)
        curr_val = self.num_value()
        shift = (new_val - curr_val) % 12
        shift = shift - 12 if shift > 6 else shift  # shift downwards if closer
        self.shift_s(shift)
        return self

    def transpose_simple(self, semitones: int, use_flats=False):
        """Transpose a `Note` according to semitone intervals.

        Parameters
        ----------
        semitones : int
            The difference in semitones to the new transposed `Note`.
        use_flats : boolean, Optional
            Selector to use flats or sharps for black keys. Default False when optional.

        Examples
        --------
        >>> NE = NoteEditor()
        >>> c = NE.create_note("C")
        >>> c.transpose_simple(6)
        F\u266f note
        >>> c.transpose(2, use_flats=True)
        A\u266d note

        """
        if use_flats:
            note_list = Note._flat_tuple
        else:
            note_list = Note._sharp_tuple
        self.letter, self.symbol = note_list[
            (self.num_value() + semitones) % 12
        ]
        return self

    def __repr__(self):
        return self.value + " note"

    def __str__(self):
        return self.value

    def __eq__(self, other):
        """Compare between other `Notes` and strings.

        Checks if the other `Note`'s value or the string is the same as this `Note`.

        Parameters
        ----------
        other
            The object to be compared with.

        Returns
        -------
        boolean
            The outcome of the `value` comparison.

        Examples
        --------
        >>> NE = NoteEditor()
        >>> d = NE.create_note("D")
        >>> d2 = NE.create_note("D")
        >>> d_str = "D"
        >>> d == d2
        True
        >>> d == d_str
        True

        Note that symbols are converted to their unicode characters when a `Note` is created.

        >>> NE = NoteEditor()
        >>> ds = NE.create_note("D#")
        >>> ds_str = "D#"
        >>> ds_str_2 = "D\u266f"
        >>> ds == ds_str
        False
        >>> ds == ds_str_2
        True

        """
        if isinstance(other, Note):
            return self.value == other.value
        elif isinstance(other, str):
            return self.value == other
        else:
            return NotImplemented
