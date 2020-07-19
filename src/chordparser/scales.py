from chordparser.notes_editor import NoteEditor
from chordparser.keys import Key


class Scale:
    """
    Scale class that composes of a Key and Notes.

    The Scale class accepts a Key and generates a 2-octave Note tuple in its 'notes' attribute. The Scale can be changed by transposing its key using the 'transpose' method.
    """
    _heptatonic_base = (2, 2, 1, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 1)
    _scales = {
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
    _submodes = {
        None: (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
        "natural": (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
        "melodic": (0, 0, 0, 0, 1, 0, -1, 0, 0, 0, 0, 1, 0, -1),
        "harmonic": (0, 0, 0, 0, 0, 1, -1, 0, 0, 0, 0, 0, 1, -1),
    }
    NE = NoteEditor()

    def __init__(self, key: Key):
        self.key = key
        self.build()

    def build(self):
        """Build the scale from its key."""
        self.scale_intervals = self._get_intervals()
        self.notes = [self.NE.create_note(self.key.root.value)]
        for interval in self.scale_intervals:
            new_note = self.NE.create_note(self.notes[-1].value)
            self.notes.append(new_note.transpose(interval, 1))
        self.notes = tuple(self.notes)
        return self

    def _get_intervals(self):
        """Get intervals based on mode."""
        shift = Scale._scales[self.key.mode]
        mode_intervals = (
            Scale._heptatonic_base[shift:]
            + Scale._heptatonic_base[:shift]
        )
        submode_intervals = Scale._submodes[self.key.submode]
        intervals = [x + y for x, y in zip(mode_intervals, submode_intervals)]
        return tuple(intervals)

    def transpose(self, semitones: int, letter: int):
        """Transpose the key of the scale."""
        self.key.transpose(semitones, letter)
        self.build()
        return self

    def transpose_simple(self, semitones: int, use_flats=False):
        """Transpose the key of the scale by specifying the change in semitone intervals. Use use_flats=True to transpose using flat accidentals."""
        self.key.transpose_simple(semitones, use_flats)
        self.build()
        return self

    def __repr__(self):
        return f'{self.key} scale'

    def __eq__(self, other):
        # Allow comparison between Keys by checking their basic attributes
        if not isinstance(other, Scale):
            return NotImplemented
        return self.key == other.key and self.notes == other.notes
