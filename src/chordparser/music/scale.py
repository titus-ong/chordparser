from chordparser.music.key import Key
from chordparser.music.note import Note
from chordparser.music.scaledegree import ScaleDegree
from chordparser.music.symbol import Symbol
from chordparser.utils.note_lists import natural_semitone_intervals


class Scale:
    """A class representing a musical scale.

    The `Scale` composes of a `Key` on which it is based on, and
    provides access to its notes and scale degrees.

    Parameters
    ----------
    key : Key
        The `Key` which the `Scale` is based on.

    Attributes
    ----------
    key : Key
        The `Key` which the `Scale` is based on.

    Examples
    --------
    >>> scale = Scale(Key("C major"))
    >>> scale
    C major scale

    """

    def __init__(self, key):
        # Type check to avoid surprises when using key methods later
        if not isinstance(key, Key):
            raise TypeError(f"object of type {type(key)} is not a Key")
        self._key = key

    @property
    def key(self):
        return self._key

    def get_notes(self):
        """Return a two octave list of `Notes` in the `Scale`.

        Returns
        -------
        list of `Note`
            Two octaves of the `Notes` in the `Scale`.

        Examples
        --------
        >>> scale = Scale(Key("C major"))
        >>> scale.get_notes()
        [C note, D note, E note, F note, G note, A note, B note,
        C note, D note, E note, F note, G note, A note, B note, C note]

        """
        notes = self._initialise_notes()
        for step in self._key.get_step_pattern():
            self._add_note(notes, step)
        return notes

    def _initialise_notes(self):
        tonic = Note(str(self._key.tonic))  # avoid same reference
        return [tonic]

    def _add_note(self, notes, step):
        prev_note = notes[-1]
        new_note = Note(str(prev_note))  # avoid same reference
        new_note.transpose(step, 1)
        notes.append(new_note)

    def get_scale_degrees(self):
        """Return a two octave list of `ScaleDegrees` in the `Scale`.

        Returns
        -------
        list of `ScaleDegree`
            Two octaves of the `ScaleDegrees` in the `Scale`.

        Examples
        --------
        >>> scale = Scale(Key("C major"))
        >>> scale.get_scale_degrees()
        [1 scale degree, 2 scale degree, \u266d3 scale degree,
        4 scale degree, 5 scale degree, \u266d6 scale degree,
        \u266d7 scale degree, 1 scale degree, 2 scale degree,
        \u266d3 scale degree, 4 scale degree, 5 scale degree,
        \u266d6 scale degree, \u266d7 scale degree, 1 scale degree]

        """
        scale_degrees = self._initialise_scale_degrees()
        for step in self._key.get_step_pattern():
            self._add_scale_degree(scale_degrees, step)
        return scale_degrees

    def _initialise_scale_degrees(self):
        return [ScaleDegree("1")]

    def _add_scale_degree(self, scale_degrees, step):
        prev_degree = scale_degrees[-1]
        new_degree = prev_degree.degree % 7 + 1
        step_difference = self._get_step_diff_from_major(new_degree, step)
        new_symbol = Symbol(str(prev_degree.symbol))  # avoid same reference
        new_symbol.shift_by(step_difference)
        scale_degrees.append(
            ScaleDegree.from_components(new_degree, new_symbol)
        )

    def _get_step_diff_from_major(self, new_degree, step):
        step_reference = natural_semitone_intervals[new_degree-2]
        return step - step_reference

    def transpose(self, semitones, letters):
        """Transpose the `Scale` by some semitone and letter intervals.

        Parameters
        ----------
        semitones : int
            The difference in semitones to the transposed `Scale`.
        letters : int
            The difference in scale degrees to the transposed `Scale`.

        Examples
        --------
        >>> scale = Scale(Key("C major"))
        >>> scale.transpose(6, 3)
        >>> scale
        F\u266f major scale
        >>> scale.transpose(0, 1)
        >>> scale
        G\u266d major scale

        """
        self._key.transpose(semitones, letters)

    def transpose_simple(self, semitones, use_flats=False):
        """Transpose the `Scale` by some semitone interval.

        Parameters
        ----------
        semitones : int
            The difference in semitones to the transposed `Scale`.
        use_flats : boolean, Optional
            Selector to use flats or sharps for black keys. Default
            False when optional.

        Examples
        --------
        >>> scale = Scale(Key("C major"))
        >>> scale.transpose_simple(6)
        F\u266f major scale
        >>> scale.transpose_simple(2, use_flats=True)
        A\u266d major scale

        """
        self._key.transpose_simple(semitones, use_flats)

    def get_note_from_scale_degree(self, scale_degree):
        """Get `Note` of a `Scale` by specifying its `ScaleDegree`.

        Parameters
        ----------
        scale_degree: ScaleDegree
            The `ScaleDegree` of the `Note` to get.

        Returns
        -------
        Note
            The `Note` of the `Scale` with the specified `ScaleDegree`.

        Examples
        --------
        >>> scale = Scale(Key("C major"))
        >>> sd = ScaleDegree("b3")
        >>> scale.get_note_from_scale_degree(sd)
        E\u266d note

        """
        major_scale = self._get_major_scale_of_self()
        note = major_scale.get_notes()[scale_degree.degree-1]
        note.symbol.shift_by(scale_degree.symbol.as_int())
        return note

    def get_scale_degree_from_note(self, note):
        """Get `ScaleDegree` of a `Scale` by specifying a `Note`.

        Parameters
        ----------
        note: Note
            The `Note` of the `ScaleDegree` to get.

        Returns
        -------
        ScaleDegree
            The `ScaleDegree` of the `Scale` of the specified `Note`.

        Examples
        --------
        >>> scale = Scale(Key("C major"))
        >>> note = Note("F#")
        >>> scale.get_scale_degree_from_note(note)
        \u266f4 scale degree

        """
        major_scale = self._get_major_scale_of_self()
        degree = min([
            idx for (idx, n) in enumerate(major_scale.get_notes())
            if n.letter == note.letter
        ]) + 1
        symbol = Symbol(str(note.symbol))
        new_sd = ScaleDegree.from_components(degree, symbol)
        return new_sd

    def _get_major_scale_of_self(self):
        new_scale = Scale(self._key)
        new_scale.key.set_mode(mode="major")
        return new_scale

    def __repr__(self):
        return f"{self._key} scale"

    def __eq__(self, other):
        """Compare with other `Scales`.

        The two `Scales` must have the same key to be equal.

        Parameters
        ----------
        other
            The object to be compared with.

        Returns
        -------
        boolean
            The outcome of the comparison.

        Examples
        --------
        >>> s = Scale(Key("C major"))
        >>> s2 = Scale(Key("C major"))
        >>> s == s2
        True
        >>> s3 = Scale(Key("C# major"))
        >>> s == s3
        False

        """
        if not isinstance(other, Scale):
            return NotImplemented
        return self._key == other.key
