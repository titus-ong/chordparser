from chordparser.notes import Note
from chordparser.keys import Key
from chordparser.quality import Quality
from chordparser.notes_editor import NoteEditor
from chordparser.scales_editor import ScaleEditor
from typing import Union, List, Tuple


class Chord:
    """
    Chord class that is composed of a root note, chord quality, optional added notes and an optional bass note.

    The Chord class accepts the chord components and builds a tuple of notes provided by the 'notes' method.

    The Chord class can be transposed using the 'transpose' method.
    """
    SE = ScaleEditor()
    NE = NoteEditor()

    def __init__(
            self,
            root: Note,
            quality: Quality,
            add: Union[List[Tuple[str, int]], None] = None,
            bass: Union[Note, None] = None,
            string: str = None,
    ):
        self.root = root
        self.quality = quality
        self.add = add
        self.bass = bass
        self.string = string
        self.build()

    def build(self):
        """Build the chord."""
        self._build_base_chord()
        self._build_full_chord()
        self._build_notation()

    def _build_base_chord(self):
        """Build the chord without any added or bass notes."""
        self.base_scale = self.SE.create_scale(self.root.value)
        self.base_intervals = self.quality.intervals
        self.base_degrees = self.quality.degrees
        self.base_symbols = self.quality.symbols
        # get a copy of the root
        root = self.NE.create_note(self.root.value)
        notes = [root]
        idx = len(self.base_intervals)
        for i in range(idx):
            new = self.NE.create_note(notes[-1].value)
            new.transpose(
                self.base_intervals[i],
                self.base_degrees[i+1] - self.base_degrees[i]
                )
            notes.append(new)
        self.base_notes = tuple(notes)

    def _build_full_chord(self):
        self.notes = list(self.base_notes)
        self.degrees = list(self.base_degrees)
        self.symbols = list(self.base_symbols)
        self._build_add()
        self._build_bass_note()
        self.notes = tuple(self.notes)
        self.degrees = tuple(self.degrees)
        self.symbols = tuple(self.symbols)
        self.intervals = self.NE.get_intervals(*self.notes)

    def _build_add(self):
        """Add notes for chords with added notes."""
        symbols = {
            '\u266d': -1, '\U0001D12B': -2,
            '\u266f': +1, '\U0001D12A': +2,
            }
        pos_list = []
        for each in self.add:
            adjustment = 0
            accidental = None
            if each[0] in symbols.keys():
                adjustment = symbols[each[0]]
                accidental = each[0]
                each = each[1:]
            tone = int(each)
            pos = max(self.tones.index(i) for i in self.tones if i[1] < tone)+1
            self.tones.insert(pos, [accidental, tone])
            self.notes.insert(pos, self._scale.notes[tone-1].shift_s(adjustment))
            pos_list.append(pos)
        self.add = [x for _, x in sorted(zip(pos_list, self.add))]
        return

    def _build_bass_note(self):
        """Build the bass note."""
        if self.bass in self.notes:
            idx = self.notes.index(self.bass)
            self.notes.pop(idx)
            self.notes.insert(0, self.bass)
            tone = self.tones.pop(idx)
            self.tones.insert(0, tone)
            return
        self.notes.insert(0, self.bass)
        degree = min(
            self._scale.notes.index(x) for x in self._scale.notes if x.letter() == self.bass.letter()
            )+1
        (interval,) = self.NE.get_min_intervals(self._scale.notes[degree-1], self.bass)
        symbols = {
            -1: '\u266d', -2: '\U0001D12B',
            +1: '\u266f', +2: '\U0001D12A',
            0: None,
            }
        accidental = symbols[interval]
        self.tones.insert(0, [accidental, degree])
        return

    def _build_notation(self):
        """Build a standardised chord notation."""
        add = ''
        if self.add:
            for each in self.add:
                if not each[0] in {'\u266d', '\U0001D12B', '\u266f', '\U0001D12A'}:
                    add += 'add'
                add += each
        if self.bass:
            bass = '/'+str(self.bass)
        else:
            bass = ''
        self.notation = str(self.root)+q_short+sus+add+str(bass)
        if not self.string:
            self.string = self.notation
        return

    def transpose(self, semitones: int, letter: int):
        """Transpose the chord by specifying the semitone and letter intervals."""
        self.root.transpose(semitones, letter)
        if self.bass:
            self.bass.transpose(semitones, letter)
        self.build()
        return self

    # def format(self, options):
    #     """Specify options to format string output."""
    #     pass

    def _xstr(self, value):
        # To print blank for None values
        if value is None:
            return ''
        return value

    def __repr__(self):
        return f'{self.notation} chord'

    def __eq__(self, other):
        # Allow comparison between Keys by checking their basic attributes
        if not isinstance(other, Chord):
            return NotImplemented
        return (
            self.root == other.root
            and self.quality == other.quality
            and self.add == other.add
            and self.bass == other.bass
            )
