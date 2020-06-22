from chordparser.notes import Note
from chordparser.notes_editor import NoteEditor
from chordparser.keys import Key
from chordparser.scales_editor import ScaleEditor
from typing import Union, List
import re
import copy


class Chord:
    """
    Chord class that is composed of a root note, chord quality, optional suspended and/or added notes, and an optional bass note.

    Arguments:
    root -- root note of the chord
    quality -- chord quality

    Keyword arguments:
    sus -- suspended notes
    add -- added notes
    bass -- bass_note
    string -- original chord notation (str)

    The Chord class accepts the chord components and builds a tuple of notes provided by the 'notes' method.

    The Chord class can be transposed using the 'transpose' method.
    """
    SE = ScaleEditor()
    NE = NoteEditor()

    def __init__(
            self,
            root: Note,
            quality: str,
            sus: Union[int, None] = None,
            add: Union[List[str], None] = None,
            bass: Union[Note, str, None] = None,
            string: str = None,
    ):
        self.root = root
        self.quality = quality
        self.sus = sus
        self.add = add
        self.bass = bass
        self.string = string
        self._first_build()

    def _first_build(self):
        self._build_no_bass()
        if self.bass:
            self._build_bass()
        self._build_notation()

    def _build_no_bass(self):
        self._build_base_triad()
        self._build_quality()
        self._build_base_chord()
        if self.sus:
            self._build_sus()
        if self.add:
            self._build_add()

    def _build_base_triad(self):
        triad_quality = {
            'major': ("major", 0),
            'minor': ("minor", 0),
            'diminished': ("minor", -1),
            'augmented': ("major", 1),
            'dominant': ("major", 0),
            'minor-major': ("minor", 0),
            'half-diminished': ("minor", -1),
            'augmented-major': ("major", 1),
        }
        quality = self.quality.split()[0]
        if quality == 'power':
            self.base_triad = None
            self._scale = self.SE.create_scale(self.root)
            return
        (triad_q, adjust) = triad_quality[quality]
        self._scale = self.SE.create_scale(self.root, triad_q)
        last_note = copy.copy(self._scale.notes[4])
        self.base_triad = (
                self._scale.notes[0],
                self._scale.notes[2],
                last_note.shift(adjust),
                )
        return

    def _build_quality(self):
        intervals = {
            'dominant': -1,
            'major': 0,
            'minor': 0,
            'minor-major': 1,
            'diminished': -1,
            'half-diminished': 0,
            'augmented': -1,
            'augmented-major': 0,
        }
        q_list = self.quality.split()
        if q_list[0] == 'power':
            self.notes = [
                self._scale.notes[0],
                self._scale.notes[4],
                ]
            self.tones = [[None, 1], [None, 5]]
            return
        self.notes = list(self.base_triad)
        self.tones = [[None, 1], [None, 3], [None, 5]]
        if len(q_list) == 1:
            return
        self.notes.append(self._scale.notes[6].shift(intervals[q_list[0]]))
        self.tones.append([None, 7])
        if q_list[-1] == 'ninth':
            self.notes.append(self._scale.notes[8])
            self.tones.append([None, 9])
        if q_list[-1] == 'eleventh':
            self.notes += [
                self._scale.notes[8],
                self._scale.notes[10],
                ]
            self.tones += [[None, 9], [None, 11]]
        if q_list[-1] == 'thirteenth':
            self.notes += [
                self._scale.notes[8],
                self._scale.notes[10],
                self._scale.notes[12],
                ]
            self.tones += [[None, 9], [None, 11], [None, 13]]
        if q_list[1] == 'minor':
            self.notes[-1].shift(-1)
            self.tones[-1][0] = '\u266D'
        return

    def _build_base_chord(self):
        self.base_chord = tuple(self.notes)
        self.base_tones = tuple(self.tones)
        return

    def _build_sus(self):
        if self.sus == 2:
            self.notes[1] = self._scale.notes[1]
            self.tones[1][1] -= 1
        else:
            self.notes[1] = self._scale.notes[3]
            self.tones[1][1] += 1
        return

    def _build_add(self):
        symbols = {
            '\u266d': -1, '\U0001D12B': -2,
            '\u266f': +1, '\U0001D12A': +2,
            }
        for each in self.add:
            adjustment = 0
            accidental = None
            if each[0] in symbols.keys():
                adjustment = symbols[each[0]]
                accidental = each[0]
                each = each[1:]
            tone = int(each)
            pos = max(self.tones.index(i) for i in self.tones if i[1] < tone)+1
            self.tones.insert(pos, [accidental, tone])
            self.notes.insert(pos, self._scale.notes[tone-1].shift(adjustment))
        return

    def _build_bass(self):
        if isinstance(self.bass, Note):
            self._build_bass_note()
        else:
            self._build_bass_str()

    def _build_bass_note(self):
        if self.bass in self.notes:
            idx = self.notes.index(self.bass)
            self.notes.pop(idx)
            self.notes.insert(0, self.bass)
            tone = self.tones.pop(idx)
            self.tones.insert(0, tone)
            return
        self.notes.insert(0, self.bass)
        degree = min(
            self._scale.notes.index(x) for x in self._scale.notes if x.letter() == self.bass.letter()
            )+1
        interval = self.NE.get_interval(self._scale.notes[degree-1], self.bass)
        symbols = {
            -1: '\u266d', -2: '\U0001D12B',
            +1: '\u266f', +2: '\U0001D12A',
            0: None,
            }
        accidental = symbols[interval]
        self.tones.insert(0, [accidental, degree])
        return

    def _build_bass_str(self):
        # build from diatonic - inversion or degree?
        # rmb to set self.bass
        pass

    def _build_notation(self):
        q_dict = {
            'power': ('5', ''),
            'major': ('maj', ''),
            'minor': ('m', ''),
            'diminished': ('dim', ''),
            'augmented': ('aug', ''),
            'dominant': ('', ''),
            'minor-major': ('minmaj', ''),
            'half-diminished': ('m', '\u266D5'),
            'augmented-major': ('maj', '\u266F5'),
        }
        ext_dict = {
            '': '',
            'seventh': '7',
            'ninth': '9',
            'eleventh': '11',
            'thirteenth': '13',
            'minor ninth': '\u266D9',
            'minor eleventh': '\u266D11',
            'minor thirteenth': '\u266D13',
        }
        if self.quality == 'major':
            q_short = ''
        else:
            q_list = self.quality.split()
            (first, last) = q_dict[q_list.pop(0)]
            mid = ext_dict[' '.join(q_list)]
            q_short = first+mid+last
        if self.sus:
            sus = 'sus'+str(self.sus)
        else:
            sus = ''
        add = ''
        if self.add:
            for each in self.add:
                if not each[0] in {'\u266d', '\U0001D12B', '\u266f', '\U0001D12A'}:
                    add += 'add'
                add += each
        if self.bass:
            bass = '/'+str(self.bass)
        else:
            bass = ''
        self.notation = str(self.root)+q_short+sus+add+str(bass)
        return

    def transpose(self, value: int = 0, use_flats: bool = False):
        """Transpose chord."""
        if not isinstance(value, int):
            raise TypeError("Only integers are accepted for value")
        if not isinstance(use_flats, bool):
            raise TypeError("Only booleans are accepted for use_flats")
        self.root.transpose(value, use_flats=use_flats)
        bass_tone = self.tones[0]
        self._transpose_build(bass_tone)
        return self

    def _transpose_build(self, bass_tone):
        self._build_no_bass()
        if self.bass:
            self._build_bass_from_tone(bass_tone)
        self._build_notation()

    def _build_bass_from_tone(self, bass_tone):
        symbols = {
            '\u266d': -1, '\U0001D12B': -2,
            '\u266f': +1, '\U0001D12A': +2,
            }
        if bass_tone in self.base_tones:
            bass_note = self.base_chord[self.base_tones.index(bass_tone)]
            if bass_tone in self.tones:
                self.tones.remove(bass_tone)
                self.notes.remove(bass_note)
            self.tones.insert(0, bass_tone)
            self.notes.insert(0, bass_note)
        else:
            self.tones.insert(0, bass_tone)
            adjustment = symbols[bass_tone[0]]
            bass_note = copy.copy(self._scale.notes[bass_tone[1]-1])
            bass_note.shift(adjustment)
        self.bass = bass_note
        return


    # def format(self, options):
    #     """Specify options to format string output."""
    #     pass

    def _xstr(self, value):
        # To print blank for None values
        if value is None:
            return ''
        return value

    def __repr__(self):
        return f'{self.notation} chord'
