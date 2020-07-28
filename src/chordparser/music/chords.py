from chordparser.editors.notes_editor import NoteEditor
from chordparser.editors.scales_editor import ScaleEditor
from chordparser.music.keys import Key
from chordparser.music.notes import Note
from chordparser.music.quality import Quality


class Chord:
    """A musical class representing a chord.

    The `Chord` is composed of a `root` `Note`, `quality`, optional `add` `Notes` and an optional `bass` `Note`. It automatically builds its `notes` from these components. When printed, a standardised short notation meant for chord sheets is displayed.

    Parameters
    ----------
    root : Note
        The root note.
    quality : Quality
        The `Chord` quality.
    add : list of (str, int), Optional
        List of added notes. The `str` is the accidental and the `int` is the scale degree of each added note.
    bass : Note, Optional
        Bass note.
    string : str, Optional
        The `Chord` notation string input.

    Attributes
    ----------
    root : Note
        The root note.
    quality : Quality
        The `Chord` quality.
    add : list of (str, int), Optional
        List of added notes.
    bass : Note, Optional
        Bass note.
    string : str, Optional
        The `Chord` notation string input.
    base_intervals : tuple of int
        The intervals of the `Chord` solely based on its `quality`.
    base_degrees : tuple of int
        The scale degrees of the `Chord` solely based on its `quality`.
    base_symbols : tuple of str
        The accidentals of the `Chord` solely based on its `quality`.
    intervals : tuple of int
        The intervals of the `Chord`.
    degrees : tuple of int
        The scale degrees of the `Chord`.
    symbols : tuple of str
        The accidentals of the `Chord`.
    notes : tuple of Note
        The tuple of `Notes` in the `Chord`.

    """

    _SE = ScaleEditor()
    _NE = NoteEditor()

    def __init__(self, root, quality, add=None, bass=None, string=None):
        self.root = root
        self.quality = quality
        self.add = add
        self.bass = bass
        self.string = string
        self.build()

    def build(self):
        """Build the `Chord` from its attributes.

        This method does not need to be used if `Chord` adjustments are done through the proper channels (i.e. `ChordEditor` or using other `Chord` methods), since those would build the `Chord` automatically.

        """
        self._build_base_chord()
        self._build_full_chord()
        self._build_notation()

    def _build_base_chord(self):
        """Build the chord without any added or bass notes."""
        self._base_scale = self._SE.create_scale(self.root.value)
        self.base_intervals = self.quality.intervals
        self.base_degrees = self.quality.degrees
        self.base_symbols = self.quality.symbols
        # get a copy of the root
        root = self._NE.create_note(self.root.value)
        notes = [root]
        idx = len(self.base_intervals)
        for i in range(idx):
            new = self._NE.create_note(notes[-1].value)
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
        self.intervals = self._NE.get_intervals(*self.notes)

    def _build_add(self):
        """Add notes for chords with added notes."""
        if not self.add:
            return
        symbols = {
            '\u266d': -1, '\U0001D12B': -2,
            '\u266f': +1, '\U0001D12A': +2,
            '': 0,
            }
        for each in self.add:
            sym = each[0]
            tone = each[1]
            shift = symbols[sym]
            pos = max(
                self.degrees.index(i)
                for i in self.degrees
                if i < tone
                ) + 1
            self.symbols.insert(pos, sym)
            self.degrees.insert(pos, tone)
            # copy the note
            new_note = self._NE.create_note(self._base_scale.notes[tone-1].value)
            new_note.shift_s(shift)
            self.notes.insert(pos, new_note)

    def _build_bass_note(self):
        """Build the bass note."""
        self.inversion = None
        if not self.bass:
            return
        if self.bass in self.notes:
            idx = self.notes.index(self.bass)
            self.notes.insert(0, self.notes.pop(idx))
            self.symbols.insert(0, self.symbols.pop(idx))
            self.degrees.insert(0, self.degrees.pop(idx))
            self.inversion = self.degrees[0]
            return
        self.notes.insert(0, self.bass)
        degree = min(
            self._base_scale.notes.index(x)
            for x in self._base_scale.notes
            if x.letter == self.bass.letter
            ) + 1
        self.degrees.insert(0, degree)
        (shift,) = self._NE.get_min_intervals(
            self._base_scale.notes[degree-1],
            self.bass
        )
        symbols = {
            -1: '\u266d', -2: '\U0001D12B',
            +1: '\u266f', +2: '\U0001D12A',
            0: '',
            }
        sym = symbols[shift]
        self.symbols.insert(0, sym)

    def _build_notation(self):
        """Build a standardised chord notation."""
        add = ""
        if self.add:
            for each in self.add:
                if not add and not str(self.quality):
                    string = 'add'  # when quality is blank
                elif not each[0]:
                    string = 'add'  # when there's no accidental
                else:
                    string = ''
                add += string + each[0] + str(each[1])
        if self.bass:
            bass = '/'+str(self.bass)
        else:
            bass = ''
        self._notation = str(self.root) + str(self.quality) + add + bass
        if not self.string:
            self.string = self._notation

    def transpose(self, semitones, letter):
        """Transpose a `Chord` according to semitone and letter intervals.

        Parameters
        ----------
        semitones
            The difference in semitones to the new transposed `root` of the `Chord`.
        letters
            The difference in scale degrees to the new transposed `root` of the `Chord`.

        Examples
        --------
        >>> CE = ChordEditor()
        >>> c = CE.create_chord("Csus")
        >>> c.transpose(6, 3)
        F\u266fsus chord
        >>> c.transpose(0, 1)
        G\u266dsus chord

        """
        self.root.transpose(semitones, letter)
        if self.bass:
            self.bass.transpose(semitones, letter)
        self.build()
        return self

    def transpose_simple(self, semitones, use_flats=False):
        """Transpose a `Chord` according to semitone intervals.

        Parameters
        ----------
        semitones : int
            The difference in semitones to the new transposed `root` of the `Chord`.
        use_flats : boolean, Optional
            Selector to use flats or sharps for black keys. Default False when optional.

        Examples
        --------
        >>> CE = ChordEditor()
        >>> c = CE.create_chord("Cm")
        >>> c.transpose_simple(6)
        F\u266fm chord
        >>> c.transpose(2, use_flats=True)
        A\u266dm chord

        """
        prev = self._NE.create_note(self.root.value)
        self.root.transpose_simple(semitones, use_flats)
        if self.bass:
            # bass has to be transposed exact!
            (diff,) = self._NE.get_tone_letter(prev, self.root)
            self.bass.transpose(*diff)
        self.build()
        return self

    def __repr__(self):
        return f'{self._notation} chord'

    def __str__(self):
        return self._notation

    def __eq__(self, other):
        """Compare between other `Chords`.

        Checks if the other `Chord` has the same attributes. Since the attributes and not the notation is being compared, `Chords` with different notation but same structure are equal (see ``Examples``).

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
        >>> CE = ChordEditor()
        >>> d = CE.create_chord("Dsus")
        >>> d2 = CE.create_chord("Dsus4")
        >>> d == d2
        True
        >>> d3 = CE.create_chord("Dsus2")
        >>> d == d3
        False

        Another example of the same `Chord` with different notation:

        >>> CE = ChordEditor()
        >>> e = CE.create_chord("Eaug7")
        >>> e2 = CE.create_chord("E7#5")
        >>> e == e2
        True

        """
        if not isinstance(other, Chord):
            return NotImplemented
        return (
            self.root == other.root
            and self.quality == other.quality
            and self.add == other.add
            and self.bass == other.bass
            )
