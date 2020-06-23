class Note:
    """
    Note class that composes of a note value.

    The Note class consists of notation a-g or A-G, with optional unicode accidental symbols \u266d, \u266f, \U0001D12B, or \U0001D12A. It is created by the NoteEditor.

    Notes can have accidentals set using the 'accidental' method, and can be shifted by semitones using the 'shift_s' method. The letter of the Note can be shifted using the 'shift_l' method. Notes also have 'letter' and 'symbol' methods to get their respective values. Numerical representation of the Note value can be accessed via the 'num_value' and 'symbolvalue' methods. Notes can be transposed using the 'transpose' method.

    Notes can be compared either with other Notes or with strings.
    """
    _flat = '\u266d'
    _sharp = '\u266f'
    _doubleflat = '\U0001D12B'
    _doublesharp = '\U0001D12A'
    _symbols = {
        _flat: -1, _doubleflat: -2,
        _sharp: +1, _doublesharp: +2,
        -1: _flat, -2: _doubleflat,
        +1: _sharp, +2: _doublesharp,
        0: '', None: 0,
        }
    _note_values = {  # Basis: C = 0
        ('C' + _doubleflat): 10,
        ('C' + _flat): 11,
        'C': 0,
        ('C' + _sharp): 1,
        ('C' + _doublesharp): 2,
        ('D' + _doubleflat): 0,
        ('D' + _flat): 1,
        'D': 2,
        ('D' + _sharp): 3,
        ('D' + _doublesharp): 4,
        ('E' + _doubleflat): 2,
        ('E' + _flat): 3,
        'E': 4,
        ('E' + _sharp): 5,
        ('E' + _doublesharp): 6,
        ('F' + _doubleflat): 3,
        ('F' + _flat): 4,
        'F': 5,
        ('F' + _sharp): 6,
        ('F' + _doublesharp): 7,
        ('G' + _doubleflat): 5,
        ('G' + _flat): 6,
        'G': 7,
        ('G' + _sharp): 8,
        ('G' + _doublesharp): 9,
        ('A' + _doubleflat): 7,
        ('A' + _flat): 8,
        'A': 9,
        ('A' + _sharp): 10,
        ('A' + _doublesharp): 11,
        ('B' + _doubleflat): 9,
        ('B' + _flat): 10,
        'B': 11,
        ('B' + _sharp): 0,
        ('B' + _doublesharp): 1,
        }
    _notes_tuple = (
        'C', 'D', 'E', 'F', 'G', 'A', 'B',
        'C', 'D', 'E', 'F', 'G', 'A', 'B')

    def __init__(self, value):
        self.value = value

    def accidental(self, value: int):
        """Change a note's accidental by specifying a value from -2(doubleflat) to 2(doublesharp)."""
        if not isinstance(value, int):
            raise TypeError("Only integers are accepted")
        if value not in {-2, -1, 0, 1, 2}:
            raise ValueError(
                "Only integers between -2 and 2 are accepted"
                )
        self.value = self.letter() + Note._symbols.get(value)
        return self

    def shift_s(self, value: int):
        """Shift a note's accidental."""
        if not isinstance(value, int):
            raise TypeError("Only integers are accepted")
        value += self.symbolvalue()
        if value not in {-2, -1, 0, 1, 2}:
            raise ValueError(
                "Only symbols up to doublesharps and doubleflats are accepted"
                )
        self.value = self.letter() + Note._symbols.get(value)
        return self

    def shift_l(self, value: int):
        """Shift a note's letter."""
        if not isinstance(value, int):
            raise TypeError("Only integers are accepted")
        pos = self._notes_tuple.index(self.letter()) + value % 7
        new_letter = self._notes_tuple[pos]
        self.value = new_letter + (self.symbol() or '')
        return self

    def num_value(self) -> int:
        """Return numerical value (basis: C = 0)."""
        return Note._note_values[self.value]

    def letter(self) -> str:
        """Return note letter."""
        return self.value[0]

    def symbol(self) -> str:
        """Return note symbol (None if no symbol)."""
        if len(self.value) > 1:
            return self.value[1]
        return None

    def symbolvalue(self) -> int:
        """Return note symbol as a integer value."""
        if len(self.value) > 1:
            symbol = self.value[1]
        else:
            symbol = None
        return Note._symbols.get(symbol)

    def transpose(self, semitones: int, letter: int):
        """Transpose a note by specifying the change in semitone and letter intervals."""
        if not isinstance(semitones, int) or not isinstance(letter, int):
            raise TypeError("Only integers are accepted for value")
        new_val = (self.num_value() + semitones) % 12
        self.shift_l(letter)
        curr_val = self.num_value()
        if (new_val-curr_val) % 12 < 12 - ((new_val-curr_val) % 12):
            shift = abs((new_val-curr_val) % 12)
        else:
            shift = -abs(12 - (new_val-curr_val) % 12)
        self.shift_s(shift)
        return self

    def __repr__(self):
        return self.value

    def __eq__(self, other):
        # Allow comparison between note values and strings
        if isinstance(other, Note):
            return self.value == other.value
        elif isinstance(other, str):
            return self.value == other
        else:
            return NotImplemented
