class Note:
    """
    Note class that composes of a note value.

    The Note class consists of notation a-g or A-G, with optional unicode accidental symbols \u266d, \u266f, \U0001D12B, or \U0001D12A. It is created by the NoteEditor.

    Notes can have accidentals set using the 'accidental' method, and can be shifted by semitones using the 'shift_s' method. The letter of the Note can be shifted using the 'shift_l' method. Notes also have 'letter' and 'symbol' methods to get their respective values. Numerical representation of the Note value can be accessed via the 'num_value', 'letter_value' and 'symbol_value' methods. Notes can be transposed using the 'transpose' method.

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
        'C', 'D', 'E', 'F', 'G', 'A', 'B')

    def __init__(self, value):
        self.value = value

    def accidental(self, value: int):
        """Change a note's accidental by specifying a value from -2(doubleflat) to 2(doublesharp)."""
        if value not in range(-2, 3):
            raise ValueError(
                "Only integers between -2 and 2 are accepted"
            )
        self.value = self.letter() + Note._symbols[value]
        return self

    def shift_s(self, value: int):
        """Shift a note's accidental."""
        value += self.symbol_value()
        if value not in range(-2, 3):
            raise ValueError(
                "Only symbols up to doublesharps and doubleflats are accepted"
            )
        self.value = self.letter() + Note._symbols[value]
        return self

    def shift_l(self, value: int):
        """Shift a note's letter."""
        pos = (Note._notes_tuple.index(self.letter()) + value) % 7
        new_letter = Note._notes_tuple[pos]
        self.value = new_letter + (self.symbol() or '')
        return self

    def num_value(self) -> int:
        """Return numerical value (basis: C = 0)."""
        num = (self.letter_value() + self.symbol_value()) % 12
        return num

    def letter(self) -> str:
        """Return note letter."""
        return self.value[0]

    def letter_value(self) -> int:
        """Return note letter as an integer value (Basis: C = 0)."""
        return Note._note_values[self.letter()]

    def symbol(self) -> str:
        """Return note symbol (None if no symbol)."""
        if len(self.value) > 1:
            return self.value[1]
        return None

    def symbol_value(self) -> int:
        """Return note symbol as an integer value."""
        return Note._symbol_signs.get(self.symbol(), 0)

    def transpose(self, semitones: int, letter: int):
        """Transpose a note by specifying the change in semitone and letter intervals."""
        new_val = (self.num_value() + semitones) % 12
        self.shift_l(letter)
        curr_val = self.num_value()
        shift = (new_val - curr_val) % 12
        shift = shift - 12 if shift > 6 else shift  # shift downwards if closer
        self.shift_s(shift)
        return self

    def __repr__(self):
        return self.value

    def __eq__(self, other):
        # Allow comparison between other Notes and strings
        if isinstance(other, Note):
            return self.value == other.value
        elif isinstance(other, str):
            return self.value == other
        else:
            return NotImplemented
