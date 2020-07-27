class Quality:
    """A class representing the quality of a `Chord`.

    The `Quality` class composes of its base `Chord` quality, extensions to the `Chord`, and optional flats on the extended `Note`.

    Parameters
    ----------
    quality_str : str
        The `Quality`'s notation.
    ext_str : str, Optional
        The extended `Chord`'s notation.
    flat_ext : boolean, Optional
        Selector for the flat of the extended `Note`. Default False when optional.

    Attributes
    ----------
    value : str
        The `Quality`'s notation.
    ext : str, Optional
        The extended `Chord`'s notation.
    flat_ext : boolean, Optional
        Selector for the flat of the extended `Note`. Default False when optional.
    base_intervals : tuple of int
        The intervals of the triad of a `Chord` with this `Quality`.
    base_degrees : tuple of int
        The scale degrees of the triad of a `Chord` with this `Quality`.
    base_symbols : tuple of str
        The accidentals of the triad of a `Chord` with this `Quality`.
    intervals : tuple of int
        The intervals of a `Chord` with this `Quality`.
    degrees : tuple of int
        The scale degrees of a `Chord` with this `Quality`.
    symbols : tuple of str
        The accidentals of a `Chord` with this `Quality`.

    Raises
    ------
    ValueError
        If a dominant chord has a `value` of 'major' (`value` should be 'dominant')
    ValueError
        If a diminished extended chord does not have a `ext` of 'diminished seventh'
    ValueError
        If a 'seventh' extended chord has a flat extension (should be reflected in `ext` and not in `flat_ext`)

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
    _heptatonic_base = (2, 2, 1, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 1)
    _base_int = {
        'power': (7,),
        'major': (4, 3),
        'minor': (3, 4),
        'diminished': (3, 3),
        'augmented': (4, 4),
        'dominant': (4, 3),
        'half-diminished': (3, 3),
        'sus2': (2, 5),
        'sus4': (5, 2),
    }
    _base_deg = {
        'power': (1, 5),
        'sus2': (1, 2, 5),
        'sus4': (1, 4, 5),
    }
    _ext_int = {
        'seventh': (10,),
        'ninth': (10, 14),
        'eleventh': (10, 14, 17),
        'thirteenth': (10, 14, 17, 21),
        'major seventh': (11,),
        'major ninth': (11, 14),
        'major eleventh': (11, 14, 17),
        'major thirteenth': (11, 14, 17, 21),
        'diminished seventh': (9,),
    }
    _shortform = {
        'power': "5",
        'major': "",
        'minor': 'm',
        'diminished': 'dim',
        'augmented': 'aug',
        'dominant': "",
        'half-diminished': "m",
        'sus2': "sus2",
        'sus4': "sus",
    }
    _ext_shortform = {
        'seventh': "7",
        'ninth': "9",
        'eleventh': "11",
        'thirteenth': "13",
        'major seventh': "maj7",
        'major ninth': "maj9",
        'major eleventh': "maj11",
        'major thirteenth': "maj13",
        'diminished seventh': "7",
    }

    def __init__(self, quality_str, ext_str=None, flat_ext=False):
        self.value = quality_str
        self.ext = ext_str
        self.flat_ext = flat_ext
        self._build()

    def _build(self):
        """Build intervals, scale degrees, and symbols."""
        self._check()
        self._base()
        self._ext()
        self._sym()

    def _check(self):
        if not self.ext:
            return
        # Check dominant chords do not have a value of 'major'
        if self.value == "major":
            if self.ext.split()[0] != "major":
                raise ValueError("'Major' can either be dominant or major extended chord")
        # Check diminished chords are only diminished sevenths
        if self.value == "diminished" or self.ext == "diminished seventh":
            if self.ext != "diminished seventh" or self.value != "diminished":
                raise ValueError("Diminished chords can only be seventh")
        # Check flat extension does not work with sevenths
        if self.ext.split()[-1] == "seventh" and self.flat_ext:
            raise ValueError("Flat extension does not apply to seventh chords")

    def _base(self):
        """Set base intervals and degrees."""
        self.base_intervals = Quality._base_int[self.value]
        self.base_degrees = Quality._base_deg.get(self.value, (1, 3, 5))

    def _ext(self):
        """Set intervals and degrees with chord extensions."""
        if not self.ext:
            self.intervals = self.base_intervals
            self.degrees = self.base_degrees
            return
        intervals = list(self.base_intervals)
        degrees = list(self.base_degrees)
        for idx, semitone in enumerate(Quality._ext_int[self.ext]):
            intervals.append(semitone - sum(intervals))
            degrees.append(7 + 2 * idx)
        if self.flat_ext:
            intervals[-1] = intervals[-1] - 1
        self.intervals = tuple(intervals)
        self.degrees = tuple(degrees)

    def _sym(self):
        """Build base symbols and symbols with extension."""
        symbols = [""]
        for i in range(len(self.intervals)):
            sum_interval = sum(self.intervals[:i+1])
            next_ = self.degrees[i+1]
            diff = sum(Quality._heptatonic_base[:next_-1])
            symbols.append(Quality._symbols[sum_interval-diff])
        if self.value == "power":
            self.base_symbols = tuple(symbols[0:2])
        else:
            self.base_symbols = tuple(symbols[0:3])
        self.symbols = tuple(symbols)

    def _short(self):
        """Return short form for quality."""
        string = Quality._shortform[self.value]
        if not self.ext:
            return string
        ext_string = Quality._ext_shortform[self.ext]
        if self.flat_ext:
            # add flat symbols
            if len(ext_string) < 3:
                ext_string = '\u266d' + ext_string
            else:
                ext_string = ext_string[0:3] + '\u266d' + ext_string[3:]
        if self.value == "half-diminished":
            ext_string += "\u266d5"
        if self.value == "augmented":
            string = ""
            ext_string += "\u266f5"
        if self.value in {"sus2", "sus4"}:
            # sus at the back
            return ext_string + string
        return string + ext_string

    def __repr__(self):
        if not self.ext:
            return self.value + " quality"
        if self.value in {"major", "diminished"}:
            # avoid word overlap
            string = self.ext
        else:
            string = self.value + " " + self.ext
        if not self.flat_ext:
            return string + " quality"
        split_string = string.split()
        split_string.insert(-1, "flat")
        return " ".join(split_string) + " quality"

    def __str__(self):
        return self._short()

    def __eq__(self, other):
        """Compare between other `Qualitys`.

        Checks if the other `Quality` has the same `value`, `ext` and `flat_ext`.

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
        >>> QE = QualityEditor()
        >>> q = QE.create_quality("maj9")
        >>> q2 = QE.create_quality("maj9")
        >>> q == q2
        True
        >>> q3 = QE.create_quality("majb9")
        >>> q == q3
        False

        """
        if not isinstance(other, Quality):
            return NotImplemented
        return (
            self.value == other.value
            and self.ext == other.ext
            and self.flat_ext == other.flat_ext
            )
