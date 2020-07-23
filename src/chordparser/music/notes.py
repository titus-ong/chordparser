class Note:
    """
    Note class that composes of a note value.

    The Note class consists of notation a-g or A-G, with optional unicode accidental symbols \u266d, \u266f, \U0001D12B, or \U0001D12A. It is created by the NoteEditor.

    Notes can have accidentals set using the 'accidental' method, and can be shifted by semitones using the 'shift_s' method. The letter of the Note can be shifted using the 'shift_l' method. Notes also have 'letter' and 'symbol' methods to get their respective values. Numerical representation of the Note value can be accessed via the 'num_value', 'letter_value' and 'symbol_value' methods. Notes can be transposed using the 'transpose' or 'transpose_simple' methods.

    Notes can be compared either with other Notes or with strings.
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
        return self.letter + self.symbol

    def num_value(self) -> int:
        """Return numerical value (basis: C = 0)."""
        num = (self.letter_value() + self.symbol_value()) % 12
        return num

    def letter_value(self) -> int:
        """Return note letter as an integer value (Basis: C = 0)."""
        return Note._note_values[self.letter]

    def symbol_value(self) -> int:
        """Return note symbol as an integer value."""
        return Note._symbol_signs[self.symbol]

    def accidental(self, value: int):
        """Change a note's accidental by specifying a value from -2(doubleflat) to 2(doublesharp)."""
        if value not in range(-2, 3):
            raise ValueError(
                "Only integers between -2 and 2 are accepted"
            )
        self.symbol = Note._symbols[value]
        return self

    def shift_s(self, value: int):
        """Shift a note's accidental."""
        value += self.symbol_value()
        if value not in range(-2, 3):
            raise ValueError(
                "Only symbols up to doublesharps and doubleflats are accepted"
            )
        self.symbol = Note._symbols[value]
        return self

    def shift_l(self, value: int):
        """Shift a note's letter."""
        pos = (Note._notes_tuple.index(self.letter) + value) % 7
        new_letter = Note._notes_tuple[pos]
        self.letter = new_letter
        return self

    def transpose(self, semitones: int, letter: int):
        """Transpose a note by specifying the change in semitone and letter intervals."""
        new_val = (self.num_value() + semitones) % 12
        self.shift_l(letter)
        curr_val = self.num_value()
        shift = (new_val - curr_val) % 12
        shift = shift - 12 if shift > 6 else shift  # shift downwards if closer
        self.shift_s(shift)
        return self

    def transpose_simple(self, semitones: int, use_flats=False):
        """Transpose a note by specifying the change in semitone intervals. Use use_flats=True to transpose using flat accidentals."""
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
        # Allow comparison between other Notes and strings
        if isinstance(other, Note):
            return self.value == other.value
        elif isinstance(other, str):
            return self.value == other
        else:
            return NotImplemented
