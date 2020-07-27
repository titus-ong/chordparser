import re
import warnings

from chordparser.editors.chords_editor import ChordEditor
from chordparser.editors.notes_editor import NoteEditor
from chordparser.editors.scales_editor import ScaleEditor
from chordparser.music.roman import Roman
from chordparser.music.scales import Scale


class ChordRomanConverter:
    """A `Chord`-`Roman` converter.

    The `ChordRomanConverter` can convert `Chords` to `Romans` based on a `Scale` or `Key`.

    """
    _symbols = {
        -1: '\u266d', -2: '\U0001D12B',
        +1: '\u266f', +2: '\U0001D12A',
        0: '',
        }
    _inversions = {
        3: (6,), 5: (6, 4),
    }
    _inversions_ext = {
        3: (6, 5), 5: (4, 3),
        7: (4, 2),
    }
    _roman_deg = {
        1: 'I', 2: 'II', 3: 'III',
        4: 'IV', 5: 'V', 6: 'VI', 7: 'VII',
    }
    _q_dict = {
        'diminished': '\u00B0',
        'augmented': '+',
        'half-diminished': '\u00f8',
    }
    _NE = NoteEditor()
    _CE = ChordEditor()
    _SE = ScaleEditor()

    def to_roman(self, chord, scale_key):
        """Converts a `Chord` to `Roman`.

        Creates the `Roman` based on the `Chord` and a `Scale` or `Key`.

        Parameters
        ----------
        chord : Chord
            The `Chord` to be converted.
        scale_key : Scale or Key
            The `Scale` or `Key` to base the `Roman` on.

        Returns
        -------
        Roman
            The `Roman` of the `Chord`.

        Warns
        -----
        UserWarning
            If the `Chord` is a power or sus chord.

        Examples
        --------
        >>> KE = KeyEditor()
        >>> SE = ScaleEditor()
        >>> CE = ChordEditor()
        >>> CRC = ChordRomanConverter()
        >>> c_key = KE.create_key("C")
        >>> c_scale = SE.create_scale(c_key)
        >>> d = CE.create_diatonic(c_scale, 2)
        >>> CRC.to_roman(d, c_key)
        ii roman chord
        >>> f = CE.create_diatonic(c_scale, 4)
        >>> CRC.to_roman(f, c_scale)
        IV roman chord

        """
        if chord.quality.value in {"power", "sus2", "sus4"}:
            warnings.warn(
                "Warning: Power and sus chords are defaulted to major chords",
                UserWarning
            )
            chord = self._CE.change_chord(chord, quality="Maj", inplace=False)
        if isinstance(scale_key, Scale):
            scale_root = scale_key.key.root
        else:
            scale_root = scale_key.root
        scale = self._SE.create_scale(scale_root, "major")
        root = self._get_roman_root(chord, scale)
        quality = self._get_roman_quality(chord)
        inversion = self._get_roman_inversion(chord)
        return Roman(root, quality, inversion)

    def _get_roman_root(self, chord, scale):
        """Get Roman notation of the chord root."""
        degree = min(
            scale.notes.index(x)
            for x in scale.notes
            if x.letter == chord.root.letter
        ) + 1
        # lower/uppercase numeral
        if chord.quality.value in {"major", "augmented", "dominant"}:
            quality_fn = str.upper
        else:
            quality_fn = str.lower
        root = quality_fn(ChordRomanConverter._roman_deg[degree])
        (shift,) = self._NE.get_min_intervals(scale.notes[degree-1], chord.root)
        sym = ChordRomanConverter._symbols[shift]  # accidental of root
        return sym + root

    def _get_roman_inversion(self, chord):
        """Get Roman inversion notation of the chord."""
        notes = len(chord.base_notes)
        if chord.inversion and notes <= 4:  # get inversion notation
            if chord.quality.ext:
                inv_dict = ChordRomanConverter._inversions_ext
            else:
                inv_dict = ChordRomanConverter._inversions
            return inv_dict.get(chord.inversion, (notes*2-1,))
        elif notes > 3:
            return (notes*2-1,)  # chord extension
        return ()

    def _get_roman_quality(self, chord):
        """Get Roman notation for chord quality."""
        q_str = ""
        if chord.quality.ext and re.match("major", chord.quality.ext):
            q_str += "M"
        q_str += ChordRomanConverter._q_dict.get(chord.quality.value, "")
        return q_str

    # def to_chord(self, roman, scale_key):
    #     pass
