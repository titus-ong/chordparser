from typing import List
import warnings

from chordparser.editors.chord_roman_converter import ChordRomanConverter
from chordparser.editors.chords_editor import ChordEditor
from chordparser.editors.notes_editor import NoteEditor
from chordparser.editors.scales_editor import ScaleEditor


class ChordAnalyser:
    """A `Chord` analyser.

    The ChordAnalyser can analyse `Chords` with reference to `Scales` and other `Chords` and find their relationships or functions.

    """
    _mode_list = [
        'major',
        'minor',
        'dorian',
        'mixolydian',
        'lydian',
        'phrygian',
        'locrian',
        ]
    _CE = ChordEditor()
    _SE = ScaleEditor()
    _CRC = ChordRomanConverter()

    def analyse_diatonic(
            self, chord, scale,
            incl_submodes: bool = False,
            allow_power_sus=False,
            default_power_sus="M",
    ) -> List[tuple]:
        """Analyse if a `Chord` is diatonic to a `Scale`.

        There may be multiple tuples in the returned list if submodes are included.

        Parameters
        ----------
        chord : Chord
            The `Chord` to be analysed.
        scale : Scale
            The `Scale` to check against.
        incl_submodes : boolean, Optional
            Selector to include the minor submodes if `scale` is minor. Default False when optional.
        allow_power_sus : boolean, Optional
            Selector to allow power and sus chords when analysing them. Default False when optional.
        default_power_sus : {"M", "m"}, Optional
            The default quality to convert power and sus chords to if analysing them. "M" is major and "m" is minor.

        Returns
        -------
        list of (Roman, str, str)
            A list of information on the `Chord` if it is diatonic. The first `str` is the `Scale`'s `mode` and the second `str` is the `Scale`'s `submode`. The list is empty if the `Chord` is not diatonic.

        Examples
        --------
        >>> CE = ChordEditor()
        >>> SE = ScaleEditor()
        >>> CA = ChordAnalyser()

        Diatonic chords

        >>> c_scale = SE.create_scale("C", "minor")
        >>> degree_1 = CE.create_diatonic(c_scale, 1)
        >>> CA.analyse_diatonic(degree_1, c_scale)
        [(i roman chord, 'minor', 'natural')]

        Checking against minor submodes

        >>> degree_7 = CE.create_chord("G")
        >>> CA.analyse_diatonic(degree_7, c_scale)
        []
        >>> CA.analyse_diatonic(degree_7, c_scale, incl_submodes=True)
        [(VII roman chord, 'minor', 'harmonic'), (VII roman chord, 'minor', 'melodic')]

        Analysing power/sus chords

        >>> power = CE.create_chord("C5")
        >>> CA.analyse_diatonic(power, c_scale)
        []
        >>> CA.analyse_diatonic(power, c_scale, allow_power_sus=True, default_power_sus="m")
        [(i roman chord, 'minor', 'natural')]

        """
        if chord.quality.value in {"power", "sus2", "sus4"}:
            if not allow_power_sus:
                return []
            chord = self._CE.change_chord(
                chord,
                quality=default_power_sus,
                inplace=False
            )
        if not incl_submodes:
            j = [scale.key.submode]
        elif scale.key.mode in {'minor', 'aeolian'}:
            j = ['natural', 'harmonic', 'melodic']
            j.remove(scale.key.submode)
            j.insert(0, scale.key.submode)  # shift to the front
        else:
            j = [None]
        chords = []
        for submode in j:
            for i in range(7):
                nscale = self._SE.create_scale(scale.key.root, scale.key.mode, submode)
                diatonic = self._CE.create_diatonic(nscale, i+1)
                if chord.base_notes[0:3] == diatonic.base_notes:
                    chords.append(
                        (self._CRC.to_roman(chord, nscale),
                         nscale.key.mode,
                         submode)
                    )
        return chords

    def analyse_all(
            self, chord, scale,
            incl_submodes: bool = False,
            allow_power_sus=False,
            default_power_sus="M",
    ):
        """Analyse if a `Chord` is diatonic to a `Scale` for any mode.

        The `Chord` is analysed against the `Scale` as well as the other modes of the `Scale`.

        Parameters
        ----------
        chord : Chord
            The `Chord` to be analysed.
        scale : Scale
            The `Scale` to check against.
        incl_submodes : boolean, Optional
            Selector to include the minor submodes if `scale` is minor. Default False when optional.
        allow_power_sus : boolean, Optional
            Selector to allow power and sus chords when analysing them. Default False when optional.
        default_power_sus : {"M", "m"}, Optional
            The default quality to convert power and sus chords to if analysing them. "M" is major and "m" is minor.

        Returns
        -------
        list of (Roman, str, str)
            A list of information on the `Chord` if it is diatonic. The first `str` is the `mode` of the scale it is diatonic to and the second `str` is the `submode`. The list is empty if the `Chord` is not diatonic.

        Examples
        --------
        >>> CE = ChordEditor()
        >>> SE = ScaleEditor()
        >>> CA = ChordAnalyser()

        Diatonic chords

        >>> c_scale = SE.create_scale("C", "minor")
        >>> degree_1 = CE.create_diatonic(c_scale, 1)
        >>> CA.analyse_all(degree_1, c_scale)
        [(i roman chord, 'minor', 'natural'), (i roman chord, 'dorian', None), (i roman chord, 'phrygian', None)]

        Checking against minor submodes

        >>> degree_7 = CE.create_chord("G")
        >>> CA.analyse_diatonic(degree_7, c_scale)
        [(V roman chord, 'major', None), (V roman chord, 'lydian', None)]
        >>> CA.analyse_diatonic(degree_7, c_scale, incl_submodes=True)
        [(V roman chord, 'minor', 'harmonic'), (V roman chord, 'minor', 'melodic'), (V roman chord, 'major', None), (V roman chord, 'lydian', None)]

        Analysing power/sus chords

        >>> power = CE.create_chord("C5")
        >>> CA.analyse_diatonic(power, c_scale)
        []
        >>> CA.analyse_diatonic(power, c_scale, allow_power_sus=True, default_power_sus="m")
        [(I roman chord, 'major', None), (I roman chord, 'mixolydian', None), (I roman chord, 'lydian', None)]

        """
        self._mode_list.remove(scale.key.mode)
        self._mode_list.insert(0, scale.key.mode)  # shift to the front
        chords = []
        for mode in self._mode_list:
            nscale = self._SE.create_scale(scale.key.root, mode)
            result = self.analyse_diatonic(
                chord, nscale, incl_submodes,
                allow_power_sus, default_power_sus
            )
            if result:
                chords += result
        return chords

    def analyse_secondary(
            self, prev_chord, next_chord, scale,
            incl_submodes: bool = False,
            allow_power_sus=False,
            default_power_sus="M",
            limit=True,
    ):
        """Analyse if a `Chord` has a secondary function.

        Check if a `Chord` is a secondary chord. By default, only secondary dominant and secondary leading tone chords are checked for.

        Parameters
        ----------
        prev_chord : Chord
            The `Chord` to be analysed for secondary function.
        next_chord : Chord
            The `Chord` to be tonicised.
        scale : Scale
            The `Scale` to check against.
        incl_submodes : boolean, Optional
            Selector to include the minor submodes if `scale` is minor. Default False when optional.
        allow_power_sus : boolean, Optional
            Selector to allow power and sus chords when analysing them. Default False when optional.
        default_power_sus : {"M", "m"}, Optional
            The default quality to convert power and sus chords to if analysing them. "M" is major and "m" is minor.
        limit : boolean, Optional
            Selector to only check for secondary dominant and leading tone chords. Default True when optional.

        Returns
        -------
        str
            The secondary chord notation ``prev_roman``/``next_roman``.

        Examples
        --------
        >>> CE = ChordEditor()
        >>> SE = ScaleEditor()
        >>> CA = ChordAnalyser()

        Diatonic chords

        >>> c_scale = SE.create_scale("C")
        >>> g = CE.create_diatonic(c_scale, 5)
        >>> d = CE.create_chord("D")
        >>> CA.analyse_secondary(d, g, c_scale)
        'V/V'

        Checking against minor submodes

        >>> vii = CE.create_chord("C#dim7")
        >>> degree_2 = CE.create_diatonic(c_scale, 2)
        >>> CA.analyse_secondary(vii, degree_2, c_scale)
        ''
        >>> CA.analyse_secondary(vii, degree_2, c_scale, incl_submodes=True)
        'vii\u00B07/ii'

        Analysing power/sus chords

        >>> power = CE.create_chord("D5")
        >>> g = CE.create_diatonic(c_scale, 5)
        >>> CA.analyse_secondary(power, g, c_scale)
        ''
        >>> CA.analyse_secondary(power, g, c_scale, allow_power_sus=True)
        'V/V'

        Analysing other secondary chords

        >>> e = CE.create_chord("Em")
        >>> CA.analyse_secondary(e, g, c_scale)
        ''
        >>> CA.analyse_secondary(e, g, c_scale, limit=False)
        'vi/V'

        """
        # We only care about chords leading to major/minor/dominant chords
        if next_chord.quality.value not in {"major", "minor", "dominant"}:
            return ""
        next_roman = self._CRC.to_roman(next_chord, scale)
        if next_roman.root in {"i", "I"}:  # ignore tonic next chords
            return ""
        if next_chord.quality.value == "dominant":
            next_scale = self._SE.create_scale(next_chord.root, "major")
        else:
            next_scale = self._SE.create_scale(
                next_chord.root, next_chord.quality.value
            )
        results = self.analyse_diatonic(
            prev_chord, next_scale, incl_submodes,
            allow_power_sus, default_power_sus
        )
        if results and (not limit or results[0][0].root in {"V", "vii"}):
            return "{}/{}".format(results[0][0], next_roman.root)
        return ""

