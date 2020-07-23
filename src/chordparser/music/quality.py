class Quality:
    """
    Quality class that is built from a chord's quality and provides intervals and scale degrees.

    The Quality class is built from the base chord quality, extensions, and optional flat extension. It has the 'base_intervals' and 'base_degrees' attributes for the intervals and scale degrees of the base chord, and 'intervals' and 'degrees' attributes for that of the proper chord.

    The Quality is represented by its full name by default. The short form of the Quality can be accessed via the 'short' method.
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
        """Quality that composes of chord quality, chord extension and any alterations to the extension.

        Arguments:
        quality_str -- chord quality e.g. major, minor (str)
        ext_str -- chord extension e.g. seventh, major ninth (str)
        flat_ext -- if flat extension e.g. flat ninth (bool)
        """
        self.value = quality_str
        self.ext = ext_str
        self.flat_ext = flat_ext
        self.build()

    def build(self):
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

    def short(self):
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
            return self.value
        if self.value in {"major", "diminished"}:
            # avoid word overlap
            string = self.ext
        else:
            string = self.value + " " + self.ext
        if not self.flat_ext:
            return string
        split_string = string.split()
        split_string.insert(-1, "flat")
        return " ".join(split_string)

    def __str__(self):
        return self.short()

    def __eq__(self, other):
        if not isinstance(other, Quality):
            return NotImplemented
        return (
            self.value == other.value
            and self.ext == other.ext
            and self.flat_ext == other.flat_ext
            )
