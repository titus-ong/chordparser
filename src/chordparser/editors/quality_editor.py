import re

from chordparser.music.quality import Quality


class QualityEditor:
    """A `Quality` editor for creating `Chords'` `Qualities`.

    The `QualityEditor` can create a `Chord`'s `Quality` from its notation.

    Attributes
    ----------
    quality_pattern : str
        The regex pattern for parsing a `Quality` notation.

    """

    _flat_pattern = '\u266D|\U0001D12B|bb|b'
    _sharp_pattern = '\u266F|\U0001D12A|##|#'
    _symbol_pattern = f"{_flat_pattern}|{_sharp_pattern}"
    _major_pattern = 'Maj|Ma|M|maj|\u0394'
    _minor_pattern = 'min|m|-'
    _dim_pattern = 'dim|o|\u00B0'
    _aug_pattern = r'aug|\+'
    _halfdim_pattern = '\u00f8|\u00d8'
    _dom_pattern = 'dom'
    _minmaj_pattern = f"(?:{_minor_pattern})(?:{_major_pattern})"
    _augmaj_pattern = f"(?:{_aug_pattern})(?:{_major_pattern})"
    _power_chord = "5"
    _extended_str = f"({_flat_pattern}){{0,1}}(7|9|11|13)"
    _altered_5 = f"({_dim_pattern}|{_aug_pattern}|{_symbol_pattern})5"
    _suspended = f"sus(2|4){{0,1}}"
    quality_pattern = (
        f"(({_power_chord})|"
        f"((({_minmaj_pattern})|({_augmaj_pattern})|"
        f"({_aug_pattern})|({_dim_pattern})|"
        f"({_halfdim_pattern})|({_major_pattern})|"
        f"({_minor_pattern})){{0,1}}"  # 0 for dominant/minor ext (lowercase note)
        f"({_extended_str}))|"
        f"(({_aug_pattern})|({_dim_pattern})|"
        f"({_major_pattern})|({_minor_pattern}))){{0,1}}"
        f"(?:{_altered_5}){{0,1}}"
        f"({_suspended}){{0,1}}"
    )

    # Pattern notation [regex group]
    # Match string [0]:
    #     {
    #         power chord [2] |
    #         extended chords [3] {
    #             (
    #                 dominant [4-none; minor if note is lowercase] |
    #                 minmaj [5] |
    #                 augmaj [6] |
    #                 aug [7] |
    #                 dim [8] |
    #                 halfdim [9] |
    #                 major [10] |
    #                 minor [11]
    #                 ) +
    #             (symbol [13] + degree [14]) [12]
    #             } |
    #         triads [15] (
    #             aug [16] |
    #             dim [17] |
    #             major [18] |
    #             minor [19]
    #             )
    #         } [1],
    #         altered 5ths [20],
    #         sus [21] 2/4 [22]

    def create_quality(self, notation, capital_note=True):
        """Create a `Quality`.

        Create a `Quality` from its notation and whether the `root` of the `Chord` was uppercase.

        Parameters
        ----------
        notation : str
            The `Quality`'s notation.
        *capital_note : boolean, Optional
            Selector for the case of the `root` of the `Chord`. Default True when optional.

        Returns
        -------
        Quality
            The created `Quality`.

        Examples
        --------
        >>> QE = QualityEditor()
        >>> QE.create_quality("sus4")
        sus4 quality
        >>> QE.create_quality("maj7")
        major seventh quality

        """
        if notation is None:
            if capital_note:
                return Quality("major")
            return Quality("minor")
        rgx = re.match(QualityEditor.quality_pattern, notation, re.UNICODE)
        if rgx.group(2):  # power
            return Quality("power")
        alt5 = self._parse_alt5(rgx.group(20))
        quality_str = self._parse_base(rgx, alt5, capital_note)
        ext_str = self._parse_ext(rgx, alt5, capital_note)
        flat_ext = self._parse_flat_ext(rgx.group(13))
        return Quality(quality_str, ext_str, flat_ext)

    def _parse_alt5(self, alt5):
        """Return state of altered 5: 0 if none, -1 if flat 5, 1 if aug 5."""
        if not alt5:
            return 0
        if alt5 in QualityEditor._dim_pattern + QualityEditor._flat_pattern:
            return -1
        return 1

    def _parse_base(self, rgx, alt5, capital_note):
        """Parse the base quality."""
        if rgx.group(21):
            return self._parse_sus(rgx)
        if rgx.group(15):
            return self._parse_triad(rgx, alt5)
        if rgx.group(3):  # extended chord
            return self._parse_base_ext(rgx, alt5, capital_note)
        if not capital_note:
            return "diminished" if alt5 < 0 else "minor"
        return "augmented" if alt5 > 0 else "major"

    def _parse_sus(self, rgx):
        """Parse sus quality."""
        note = rgx.group(22) or "4"  # if 'sus'
        return "sus" + note

    def _parse_triad(self, rgx, alt5):
        """Parse quality of triads."""
        if rgx.group(16):
            return "augmented"
        if rgx.group(17):
            return "diminished"
        if rgx.group(18):
            if alt5 > 0:
                return "augmented"
            return "major"
        if alt5 < 0:
            return "diminished"
        return "minor"

    def _parse_base_ext(self, rgx, alt5, capital_note):
        """Parse base quality of extended chords."""
        if not rgx.group(4):
            if capital_note:
                quality = "dominant"
            else:
                quality = "minor"
        elif rgx.group(5) or rgx.group(11):
            quality = "minor"
        elif rgx.group(6) or rgx.group(7):
            quality = "augmented"
        elif rgx.group(8):
            quality = "diminished"
        elif rgx.group(9):
            quality = "half-diminished"
        elif rgx.group(10):
            quality = "major"
        if alt5 < 0 and quality == "minor":
            quality = "half-diminished"
        if alt5 > 0 and quality in {"major", "dominant"}:
            quality = "augmented"
        return quality

    def _parse_ext(self, rgx, alt5, capital_note):
        """Parse quality of extended chords."""
        if not rgx.group(3):
            return None
        num_to_words = {
            '7': "seventh",
            '9': "ninth",
            '11': "eleventh",
            '13': "thirteenth",
        }
        ext_str = ""
        if rgx.group(5) or rgx.group(6) or rgx.group(10):
            ext_str += "major "
        if rgx.group(8):
            ext_str += "diminished "
        ext_str += num_to_words[rgx.group(14)]
        return ext_str

    def _parse_flat_ext(self, flat):
        """Parse extensions with flats."""
        if flat:
            return True
        return False
