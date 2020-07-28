from chordparser.editors.notes_editor import NoteEditor
from chordparser.music.keys import Key


class Scale:
    """A class representing a musical scale.

    The `Scale` composes of a `Key` on which it is based on, and a tuple of `Notes` as part of its `notes` attribute.

    Parameters
    ----------
    key : Key
        The `Key` which the `Scale` is based on.

    Attributes
    ----------
    key : Key
        The `Key` which the `Scale` is based on.
    notes : tuple
        A two-octave tuple of `Notes` of the `Scale`.
    scale_intervals : tuple
        The semitone intervals between `notes`.

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
    _NE = NoteEditor()

    def __init__(self, key):
        self.key = key
        self.build()

    def build(self):
        """Build the `Scale` from its `Key`.

        This method does not need to be used if `Scale` adjustments are done through the proper channels (i.e. `ScaleEditor` or using other `Scale` methods), since those would build the `Scale` automatically.

        """
        self.scale_intervals = self._get_intervals()
        self.notes = self._get_notes()
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

    def _get_notes(self):
        """Get notes based on intervals."""
        notes = [self._NE.create_note(self.key.root.value)]
        for interval in self.scale_intervals:
            new_note = self._NE.create_note(notes[-1].value)
            notes.append(new_note.transpose(interval, 1))
        return tuple(notes)

    def transpose(self, semitones, letter):
        """Transpose a `Scale` according to semitone and letter intervals.

        Parameters
        ----------
        semitones
            The difference in semitones to the new transposed `root` of the `Scale`'s `Key`.
        letters
            The difference in scale degrees to the new transposed `root` of the `Scale`'s `Key`.

        Examples
        --------
        >>> SE = ScaleEditor()
        >>> c = SE.create_scale("C", "major")
        >>> c.transpose(6, 3)
        F\u266f major scale
        >>> c.transpose(0, 1)
        G\u266d major scale

        """
        self.key.transpose(semitones, letter)
        self.build()
        return self

    def transpose_simple(self, semitones, use_flats=False):
        """Transpose a `Scale` according to semitone intervals.

        Parameters
        ----------
        semitones : int
            The difference in semitones to the new transposed `root` of the `Scale`'s `Key`.
        use_flats : boolean, Optional
            Selector to use flats or sharps for black keys. Default False when optional.

        Examples
        --------
        >>> SE = ScaleEditor()
        >>> c = SE.create_scale("C", "minor")
        >>> c.transpose_simple(6)
        F\u266f natural minor scale
        >>> c.transpose(2, use_flats=True)
        A\u266d natural minor scale

        """
        self.key.transpose_simple(semitones, use_flats)
        self.build()
        return self

    def __repr__(self):
        return f'{self.key} scale'

    def __str__(self):
        return str(self.key)

    def __eq__(self, other):
        """Compare between other `Scales`.

        Checks if the other `Scale` has the same `Key` and `notes`.

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
        >>> SE = ScaleEditor()
        >>> d = SE.create_scale("D", "minor")
        >>> d2 = SE.create_scale("D", "minor")
        >>> d == d2
        True
        >>> d3 = SE.create_scale("D", "minor", "harmonic")
        >>> d == d3
        False

        """
        if not isinstance(other, Scale):
            return NotImplemented
        return self.key == other.key and self.notes == other.notes
