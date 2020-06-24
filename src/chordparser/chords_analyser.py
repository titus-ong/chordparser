from chordparser.notes_editor import NoteEditor
from chordparser.scales_editor import ScaleEditor
from chordparser.chords_editor import ChordEditor
from typing import Union, List
import warnings


class ChordAnalyser:
    """
    ChordAnalyser class that analyses the relationship between a chord and a scale.

    The ChordAnalyser can return the roman numeral notation of a chord using the 'roman' method. It also analyses the chord's relationship to a scale using the 'analyse_diatonic' and 'analyse_all' methods, which account for only diatonic chords and chords from all modes respectively.
    """
    intervals = {
        (4, 3): str.upper,
        (3, 4): str.lower,
        (3, 3): str.lower,
        (4, 4): str.upper,
    }
    symbols = {
        -1: '\u266d', -2: '\U0001D12B',
        +1: '\u266f', +2: '\U0001D12A',
        0: '',
        }
    inversions = {
        (1, 3): '6', (2, 3): '64',
        (1, 4): '65', (2, 4): '43',
        (3, 4): '42',
    }
    roman_deg = {
        1: 'I', 2: 'II', 3: 'III',
        4: 'IV', 5: 'V', 6: 'VI', 7: 'VII',
    }
    q_dict = {
        'major': 'M',
        'minor': '',
        'diminished': '\u00B0',
        'augmented': '+',
        'dominant': '',
        'minor-major': 'M',
        'half-diminished': '\u00f8',
        'augmented-major': '+M',
    }
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

    def roman(self, chord, scale):
        """Return roman numeral notation."""
        if chord.quality == 'power':
            raise ValueError("Cannot parse power chords")
        if chord.sus:
            warnings.warn("Warning: sus chords may not be parsed correctly", UserWarning)
        c_int = (self.NE.get_intervals(*chord.base_chord[0:3]))
        scale = self.SE.create_scale(scale.key.root, "major")
        degree = min(scale.notes.index(x) for x in scale.notes if x.letter()==chord.root.letter())+1
        q_fn = self.intervals[c_int]
        c_qual = q_fn(self.roman_deg[degree])  # lower/uppercase numeral
        (shift,) = self.NE.get_min_intervals(scale.notes[degree-1], chord.root)
        symb = self.symbols[shift]  # accidental of root
        notes = len(chord.base_tones)
        if chord.bass and chord.tones[0] in chord.base_tones:
            inversion = chord.base_tones.index(chord.tones[0])
            inv_str = self.inversions.get((inversion, notes), str(notes*2-1))  # inversion notation
        elif notes > 3:
            inv_str = str(notes*2-1)
        else:
            inv_str = ''
        qual = chord.quality.split()[0]
        if notes > 3 or qual == 'augmented' or qual == 'diminished':
            q_str = self.q_dict[qual]  # quality notation
        else:
            q_str = ''
        numeral = symb+c_qual+q_str+inv_str
        return numeral

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
