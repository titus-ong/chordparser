from chordparser.music.notes import Note


class Key:
    """A class representing a musical key.

    The `Key` class composes of a `Note` class as its `root` as well as the attributes `mode` and `submode`. It is created by the `KeyEditor`. `Keys` can use the same methods as `Notes` to manipulate their `root`.

    Parameters
    ----------
    root : Note
        The root note of the `Key`.
    mode : {'major', 'minor', 'ionian', 'dorian', 'phrygian', 'lydian', 'mixolydian', 'aeolian', 'locrian'}
        The mode of the `Key`.
    submode : {None, 'natural', 'harmonic', 'melodic'}
        The submode of the `Key`. If the `mode` is not 'minor'/'aeolian', `submode` is None. Else, `submode` is one of the strings.

    Attributes
    ----------
    root : Note
        The root note of the `Key`.
    mode : {'major', 'minor', 'ionian', 'dorian', 'phrygian', 'lydian', 'mixolydian', 'aeolian', 'locrian'}
        The mode of the `Key`.
    submode : {None, 'natural', 'harmonic', 'melodic'}
        The submode of the `Key`. If the `mode` is not 'minor'/'aeolian', `submode` is None. Else, `submode` is one of the strings.

    """

    def __init__(self, root, mode, submode):
        self.root = root
        self.mode = mode
        self.submode = submode

    def __getattr__(self, attribute):
        """Allow `Note` methods to be used on the `Key`'s `root`.

        See Also
        --------
        chordparser.music.notes.Note : For a list of `Note` methods.
        """
        if attribute in Note.__dict__:
            return getattr(self.root, attribute)
        raise AttributeError(f"'Key' object has no attribute '{attribute}'")

    def __repr__(self):
        if not self.submode:
            return f'{self.root} {self.mode}'
        return f'{self.root} {self.submode} {self.mode}'

    def __eq__(self, other):
        """Compare between other `Keys`.

        Checks if the other `Key` has the same attributes.

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
        >>> KE = KeyEditor()
        >>> d = KE.create_key("D", "minor")
        >>> d2 = KE.create_key("D", "minor", "natural")
        >>> d == d2
        True
        >>> d3 = KE.create_key("D", "minor", "harmonic")
        >>> d == d3
        False

        Note that the major mode is the same as ionian, and the minor mode is the same as aeolian.

        >>> KE = KeyEditor()
        >>> e = KE.create_key("E", "major")
        >>> e2 = KE.create_key("E", "ionian")
        >>> e == e2
        True
        >>> f = KE.create_key("F", "minor")
        >>> f2 = KE.create_key("F", "aeolian")
        >>> f == f2
        True

        """
        if not isinstance(other, Key):
            return NotImplemented
        if self.mode in {'major', 'ionian'}:
            return (
                self.root == other.root
                and other.mode in {'major', 'ionian'}
                and self.submode == other.submode
            )
        if self.mode in {'minor', 'aeolian'}:
            return (
                self.root == other.root
                and other.mode in {'minor', 'aeolian'}
                and self.submode == other.submode
            )
        return (
            self.root == other.root
            and self.mode == other.mode
            and self.submode == other.submode
        )
