from chordparser.music.notationparser import NotationParserTemplate
from chordparser.music.note import NoteNotationParser, Note
from chordparser.utils.note_lists import (harmonic_intervals,
                                          melodic_intervals,
                                          natural_semitone_intervals,
                                          mode_order)
from chordparser.utils.regex_patterns import (submode_pattern,
                                              mode_pattern,
                                              short_minor_pattern,
                                              short_major_pattern)


class ModeError(Exception):
    """Exception where a `Key`'s `mode` is invalid."""

    pass


class ModeNotationParser(NotationParserTemplate):
    """Parse mode notation into mode and submode."""

    _pattern = (
        fr"(\s?({submode_pattern})?\s?({mode_pattern}))|"
        f"({short_minor_pattern})|"
        f"({short_major_pattern})"
    )

    def _split_into_groups(self, regex):
        """Split into mode and submode."""
        mode = self._get_mode(
            regex.group(3), regex.group(4), regex.group(5)
        )
        submode = self._get_submode(
            regex.group(2), mode
        )
        return mode, submode

    def _get_mode(self, long_mode, short_minor, short_major):
        # Cannot use truthy because short_major searches for ""
        if short_major is not None:
            return "major"
        if short_minor:
            return "minor"
        return long_mode.lower()

    def _get_submode(self, submode, mode):
        is_minor = self._is_minor(mode)
        if submode and not is_minor:
            raise ModeError(f"'{mode}' does not have a submode")
        if not is_minor:
            return ""
        if is_minor and not submode:
            return "natural"
        return submode.lower()

    def _is_minor(self, mode):
        return mode in ("minor", "aeolian")


class Mode:
    """A class representing the mode of a key.

    The `Mode` class consists of a mode {major, minor, ionian, dorian,
    phrygian, lydian, mixolydian, aeolian, locrian} and an optional
    submode {natural, harmonic, melodic} (only applicable for minor
    or aeolian mode).

    Attributes
    ----------
    mode : str
        The mode.
    submode : str, Optional
        The submode. It is an empty string for non-minor modes, and
        defaults to 'natural' for minor modes.

    """

    _MNP = ModeNotationParser()

    def __init__(self, notation):
        mode, submode = self._MNP.parse_notation(notation)
        self._mode = mode
        self._submode = submode

    @property
    def mode(self):
        return self._mode

    @property
    def submode(self):
        return self._submode

    def get_step_pattern(self):
        """Return the semitone step pattern of the `Mode`.

        Submode accidentals are accounted for (i.e. harmonic or
        melodic).

        Returns
        -------
        tuple of int
            The semitone step pattern of the mode.

        Examples
        --------
        >>> harm_minor = Mode("harmonic minor")
        >>> harm_minor.get_step_pattern()
        (2, 1, 2, 2, 1, 3, 1, 2, 1, 2, 2, 1, 3, 1)

        """
        mode_pattern = self._get_mode_pattern()
        submode_pattern = self._get_submode_pattern()
        return self._combine_patterns(mode_pattern, submode_pattern)

    def _combine_patterns(self, mode_pattern, submode_pattern):
        return tuple(
            sum(x) for x in zip(mode_pattern, submode_pattern)
        )

    def _get_mode_pattern(self):
        starting_idx = mode_order[self._mode]
        return (
            natural_semitone_intervals[starting_idx:]
            + natural_semitone_intervals[:starting_idx]
        )

    def _get_submode_pattern(self):
        if self._submode == "harmonic":
            return harmonic_intervals
        if self._submode == "melodic":
            return melodic_intervals
        return [0]*len(natural_semitone_intervals)

    def __repr__(self):
        return f"{self} mode"

    def __str__(self):
        if self._submode:
            return f"{self._submode} {self._mode}"
        return self._mode

    def __eq__(self, other):
        """Compare with other `Modes`.

        The two `Modes` must have the same mode and submode to be equal.

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
        >>> m = Mode("harmonic minor")
        >>> m2 = Mode("harmonic minor")
        >>> m3 = Mode("minor")
        >>> m == m2
        True
        >>> m == m3
        False

        """
        if not isinstance(other, Mode):
            return NotImplemented
        return (
            self._mode == other.mode and
            self._submode == other._submode
        )


class KeyNotationParser(NotationParserTemplate):
    """Parse key notation into tonic and mode groups."""

    _NNP = NoteNotationParser()
    _MNP = ModeNotationParser()
    _pattern = (
        f"({_NNP.pattern})"
        f"({_MNP.pattern})"
    )

    def _split_into_groups(self, regex):
        tonic = regex.group(1)
        mode_group_num = self._NNP.get_num_groups() + 2
        mode = regex.group(mode_group_num)
        return tonic, mode


class Key:
    """A class representing a musical key.

    The `Key` class composes of a `Note` object as its `tonic` and a
    `Mode` object with the attributes `mode` and `submode`. It can be
    created from its string notation or by specifying its tonic, mode
    and submode using the class method Key.from_args().

    Parameters
    ----------
    notation : str
        The `Key` notation. This is in the format of:
        {tonic} {submode(optional)} {mode}
        e.g. C# harmonic minor, C major, Dm. If only the tonic is
        specified, the `Key` is assumed to be major.

    Attributes
    ----------
    tonic : Note
        The tonic of the `Key`.
    mode : Mode
        The mode of the `Key`.

    Raises
    ------
    SyntaxError
        If the tonic, mode or submode is invalid.
    ModeError
        If the submode does not match the mode (e.g. harmonic major).

    Examples
    --------
    >>> key = Key("C# minor")
    >>> key.tonic
    C\u266f note
    >>> key.mode.mode
    minor
    >>> key.mode.submode
    natural

    """

    _KNP = KeyNotationParser()

    def __init__(self, notation):
        tonic, mode = self._KNP.parse_notation(notation)
        self._tonic = Note(tonic)
        self._mode = Mode(mode)

    @classmethod
    def from_components(cls, tonic, mode, submode=""):
        """Create a `Key` from its tonic, mode and submode components.

        Parameters
        ----------
        tonic : Note or str
            The tonic of the `Key`.
        mode : str
            The mode of the `Key`.
        submode : str, Optional
            The submode of the `Key`. Defaults to "" for non-minor and
            'natural' for minor modes.

        Raises
        ------
        SyntaxError
            If the tonic, mode or submode is invalid.
        ModeError
            If the submode does not match the mode
            (e.g. harmonic major).

        Examples
        --------
        >>> key = Key.from_components("C", "major")
        >>> key
        C major key

        >>> key = Key.from_components(Note("D"), "minor", "harmonic")
        >>> key
        D harmonic minor key

        """
        notation = f"{tonic} {submode} {mode}"
        return cls(notation)

    @property
    def tonic(self):
        return self._tonic

    @property
    def mode(self):
        return self._mode

    def get_step_pattern(self):
        """Return the semitone step pattern of the `Key`.

        Submode accidentals are accounted for (i.e. harmonic or
        melodic).

        Returns
        -------
        tuple of int
            The semitone step pattern of the key.

        Examples
        --------
        >>> key = Key("C harmonic minor")
        >>> key.get_step_pattern()
        (2, 1, 2, 2, 1, 3, 1, 2, 1, 2, 2, 1, 3, 1)

        """
        return self._mode.get_step_pattern()

    def set_mode(self, mode=None, submode=None):
        """Set the `Key`'s mode.

        The mode and submode arguments are optional. The mode will
        default to the current `Key`'s mode, while the submode will
        default to "natural" for minor and "" for non-minor.

        Parameters
        ----------
        mode : str, Optional
            The new mode.
        submode : str, Optional
            The new submode.

        Raises
        ------
        SyntaxError
            If the tonic, mode or submode is invalid.
        ModeError
            If the submode does not match the mode (e.g. harmonic
            major).
        TypeError
            If neither the mode nor submode are specified.

        Examples
        --------
        >>> key = Key("C major")
        >>> key.set_mode("minor", "melodic")
        >>> key.mode
        melodic minor mode

        """
        if mode is None and submode is None:
            raise TypeError(
                "At least one argument must be specified (0 given)"
                )
        if mode is None:
            mode = self._mode.mode
        mode_notation = self._create_mode_notation(mode, submode)
        self._mode = Mode(mode_notation)

    def _create_mode_notation(self, mode, submode):
        if submode:
            return f"{submode} {mode}"
        return mode

    def to_relative_major(self):
        """Change the `Key` to its relative major.

        The `Key`'s mode must be minor or aeolian.

        Raises
        ------
        ModeError
            If the `Key` is not minor or aeolian.

        Examples
        --------
        >>> key = Key("D minor")
        >>> key.to_relative_major()
        >>> key
        F major key

        """
        if not self._is_minor():
            raise ModeError(f"'{self}' is not minor")
        self.transpose(3, 2)
        self.set_mode("major")

    def _is_minor(self):
        return self.mode.mode in {"minor", "aeolian"}

    def to_relative_minor(self, submode="natural"):
        """Change the `Key` to its relative minor.

        The `Key`'s `mode` must be major or ionian.

        Parameters
        ----------
        key : Key
            The `Key` to be changed.
        submode : {"natural", "harmonic", "melodic"}, Optional
            The new submode of the relative minor `Key`.

        Raises
        ------
        ModeError
            If the `Key` is not major or ionian.
        SyntaxError
            If the submode is invalid.

        Examples
        --------
        >>> key = Key("D major")
        >>> key.to_relative_minor()
        >>> key
        B natural minor
        >>> key = Key("E major")
        >>> key.to_relative_minor("melodic")
        C\u266f melodic minor

        """
        if not self._is_major():
            raise ModeError(f"'{self}' is not major")
        self.transpose(-3, -2)
        self.set_mode("minor", submode)

    def _is_major(self):
        return self.mode.mode in {"major", "ionian"}

    def transpose(self, semitones, letters):
        """Transpose the `Key` by some semitone and letter intervals.

        Parameters
        ----------
        semitones : int
            The difference in semitones to the transposed `Key`.
        letters : int
            The difference in scale degrees to the transposed `Key`.

        Examples
        --------
        >>> key = Key("C")
        >>> key.transpose(6, 3)
        >>> key
        F\u266f major key
        >>> key.transpose(0, 1)
        >>> key
        G\u266d major key

        """
        self._tonic.transpose(semitones, letters)

    def transpose_simple(self, semitones, use_flats=False):
        """Transpose the `Key` by some semitone interval.

        Parameters
        ----------
        semitones : int
            The difference in semitones to the transposed `Key`.
        use_flats : boolean, Optional
            Selector to use flats or sharps for black keys. Default
            False when optional.

        Examples
        --------
        >>> key = Key("C")
        >>> key.transpose_simple(6)
        F\u266f major key
        >>> key.transpose_simple(2, use_flats=True)
        A\u266d major key

        """
        self._tonic.transpose_simple(semitones, use_flats)

    def __repr__(self):
        return f"{self} key"

    def __str__(self):
        return f"{self._tonic} {self._mode}"

    def __eq__(self, other):
        """Compare with other `Keys`.

        The two `Keys` must have the same tonic and mode to be equal.

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
        >>> k = Key("C major")
        >>> k2 = Key("C major")
        >>> k == k2
        True
        >>> k3 = Key("C# major")
        >>> k == k3
        False
        >>> k4 = Key("C minor")
        >>> k == k4
        False

        """
        if not isinstance(other, Key):
            return NotImplemented
        return self._tonic == other.tonic and self._mode == other.mode
