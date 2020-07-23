from typing import List
import warnings

from chordparser.editors.chord_roman_converter import ChordRomanConverter
from chordparser.editors.chords_editor import ChordEditor
from chordparser.editors.notes_editor import NoteEditor
from chordparser.editors.scales_editor import ScaleEditor


class ChordAnalyser:
    """
    ChordAnalyser class that analyses the relationship between a chord and a scale.

    The ChordAnalyser can return the roman numeral notation of a chord using the 'roman' method. It also analyses the chord's relationship to a scale using the 'analyse_diatonic' and 'analyse_all' methods, which account for only diatonic chords and chords from all modes respectively.
    """
    mode_list = [
        'major',
        'minor',
        'dorian',
        'mixolydian',
        'lydian',
        'phrygian',
        'locrian',
        ]
    NE = NoteEditor()
    CE = ChordEditor()
    SE = ScaleEditor()
    CRC = ChordRomanConverter()

    def analyse_diatonic(
            self, chord, scale,
            incl_submodes: bool = False,
            allow_power_sus=False,
            default_power_sus="M",
    ) -> List[tuple]:
        """Return all possible chord function. Format: List[(Roman numeral, scale mode, scale submode)]. To convert power and sus chords to be parsed as Roman notation, use allow_power_sus=True and set default_power_sus ("M" for major, "m" for minor)."""
        if chord.quality.value in {"power", "sus2", "sus4"}:
            if not allow_power_sus:
                return []
            chord = self.CE.change_chord(
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
                nscale = self.SE.create_scale(scale.key.root, scale.key.mode, submode)
                diatonic = self.CE.create_diatonic(nscale, i+1)
                if chord.base_notes[0:3] == diatonic.base_notes:
                    chords.append(
                        (self.CRC.to_roman(chord, nscale),
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
        """Return all possible chord function accounting for all modes."""
        self.mode_list.remove(scale.key.mode)
        self.mode_list.insert(0, scale.key.mode)  # shift to the front
        chords = []
        for mode in self.mode_list:
            nscale = self.SE.create_scale(scale.key.root, mode)
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
    ):
        """Return secondary chord notation."""
        # We only care about chords leading to major/minor/dominant chords
        if next_chord.quality.value not in {"major", "minor", "dominant"}:
            return ""
        if next_chord.quality.value == "dominant":
            next_scale = self.SE.create_scale(next_chord.root, "major")
        else:
            next_scale = self.SE.create_scale(
                next_chord.root, next_chord.quality.value
            )
        results = self.analyse_diatonic(
            prev_chord, next_scale, incl_submodes,
            allow_power_sus, default_power_sus
        )
        if results:
            next_roman = self.CRC.to_roman(next_chord, scale)
            return "{}/{}".format(results[0][0], next_roman.root)
        return ""

