class Roman:
    """A class representing Roman numeral notation.

    The `Roman` is composed of its `root`, `quality` and `inversion`. When printed, the standard Roman numeral notation is displayed.

    Parameters
    ----------
    root : str
        The scale degree of the `Roman`. Uppercase if major/augmented and lowercase if minor/diminished.
    quality : str
        The quality of the `Roman`.
    inversion : tuple of int
        The inversion of the `Roman` in figured bass notation (e.g. (6, 4) for second inversion).

    Attributes
    ----------
    root : str
        The scale degree of the `Roman`. Uppercase if major/augmented and lowercase if minor/diminished.
    quality : str
        The quality of the `Roman`.
    inversion : tuple of int
        The inversion of the `Roman` in figured bass notation (e.g. (6, 4) for second inversion).

    """

    def __init__(self, root, quality, inversion):
        self.root = root
        self.quality = quality
        self.inversion = inversion
        self._build_notation()

    def _build_notation(self):
        inv_str = "".join(map(str, self.inversion))
        self._notation = self.root + self.quality + inv_str

    def __repr__(self):
        return self._notation + " roman chord"

    def __str__(self):
        return self._notation

    def __eq__(self, other):
        """Compare between other `Romans`.

        Checks if the other `Roman` has the same `root`, `quality` and `inversion`.

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
        >>> KE = KeyEditor()
        >>> SE = ScaleEditor()
        >>> CE = ChordEditor()
        >>> CRC = ChordRomanConverter()
        >>> c_key = KE.create_key("C")
        >>> c_scale = SE.create_scale(c_key)
        >>> d = CE.create_diatonic(c_scale, 2)
        >>> r = CRC.to_roman(d, c_key)
        >>> r2 = CRC.to_roman(d, c_key)
        >>> r == r2
        True
        >>> e = CE.create_diatonic(c_scale, 3)
        >>> r3 = CRC.to_roman(e, c_key)
        >>> r == r3
        False

        """
        if isinstance(other, Roman):
            return (
                self.root == other.root and
                self.quality == other.quality and
                self.inversion == other.inversion
            )
        if isinstance(other, str):
            return str(self) == other
        return NotImplemented
