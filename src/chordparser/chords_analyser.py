from chordparser.notes_editor import NoteEditor
from chordparser.scales_editor import ScaleEditor
from chordparser.chords_editor import ChordEditor
from chordparser.chord_roman_converter import ChordRomanConverter
from typing import List
import warnings


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


    def analyse_diatonic(self, chord, scale, incl_submodes: bool = False) -> List[tuple]:
        """Return all possible chord function (None if not found). Format: List[(Roman numeral, scale mode, scale submode)]."""
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
                if chord.base_triad == diatonic.base_triad:
                    chords.append((self.roman(chord, nscale), nscale.key.mode, submode))
        return chords

    def analyse_all(self, chord, scale, incl_submodes: bool = False):
        """Return all possible chord function accounting for all modes (None if not found)."""
        self.mode_list.remove(scale.key.mode)
        self.mode_list.insert(0, scale.key.mode)  # shift to the front
        chords = []
        for mode in self.mode_list:
            nscale = self.SE.create_scale(scale.key.root, mode)
            result = self.analyse_diatonic(chord, nscale, incl_submodes)
            if result:
                chords += result
        return chords
