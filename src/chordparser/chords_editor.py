from chordparser.notes import Note
from chordparser.keys import Key
from chordparser.scales import Scale
from chordparser.chords import Chord
from chordparser.notes_editor import NoteEditor
from chordparser.keys_editor import KeyEditor
from chordparser.scales_editor import ScaleEditor
from typing import Union, List
import re


class ChordEditor:
    """
    ChordEditor class that creates a Chord from either a string or a Scale/Key.

    The ChordEditor class can parse a chord notation string to create a Chord using the 'create_chord' method, or create a Chord by specifying a Scale/Key and scale degree using the 'create_diatonic' method. The ChordEditor can also change a chord using the 'change_chord' method.
    """
    _letter_pattern = '[a-gA-G]'
    _flat_pattern = '\u266D|\U0001D12B|bb|b'
    _sharp_pattern = '\u266F|\U0001D12A|##|#'
    _symbol_pattern = f"{_flat_pattern}|{_sharp_pattern}"
    _note_pattern = f"(?:{_letter_pattern})(?:{_symbol_pattern}){{0,1}}"
    _major_pattern = 'Maj|Ma|M|maj|\u0394'
    _minor_pattern = 'min|m|-'
    _dim_pattern = 'dim|o|\u00B0'
    _aug_pattern = 'aug|\+'
    _halfdim_pattern = '\u00f8|\u00d8'
    _dom_pattern = 'dom'
    _minmaj_pattern = f"(?:{_minor_pattern})(?:{_major_pattern})"
    _augmaj_pattern = f"(?:{_aug_pattern})(?:{_major_pattern})"
    _power_chord = "5"
    _extended_str = f"({_flat_pattern}){{0,1}}(7|9|11|13)"
    _altered_5 = f"({_dim_pattern}|{_aug_pattern}|{_symbol_pattern})5"
    _others = f"[^/]+"
    _suspended = f"sus(2|4){{0,1}}"
    _added = f"(?:add){{0,1}}({_symbol_pattern}){{0,1}}(2|4|6|9|11|13)"

    # Pattern notation [regex group]
    # Match string [0]:
    #     note [1], {
    #         power chord [3] |
    #         extended chords [4] {
    #             (
    #                 dominant [5-none; minor if note is lowercase] |
    #                 minmaj [6] |
    #                 augmaj [7] |
    #                 aug [8] |
    #                 dim [9] |
    #                 halfdim [10] |
    #                 major [11] |
    #                 minor [12]
    #                 ) +
    #             (symbol [14] + degree [15]) [13]
    #             } |
    #         triads [16] (
    #             aug [17] |
    #             dim [18] |
    #             major [19] |
    #             minor [20]
    #             )
    #         } [2],
    #         altered 5ths [21],
    #         others (sus/add) [22],
    #         bass [23]
    _pattern = (
        f"({_note_pattern})"
        f"(({_power_chord})|"
        f"((({_minmaj_pattern})|({_augmaj_pattern})|"
        f"({_aug_pattern})|({_dim_pattern})|"
        f"({_halfdim_pattern})|({_major_pattern})|"
        f"({_minor_pattern})){{0,1}}"  # 0 for dominant/minor ext (lowercase note)
        f"({_extended_str}))|"
        f"(({_aug_pattern})|({_dim_pattern})|"
        f"({_major_pattern})|({_minor_pattern}))){{0,1}}"
        f"(?:{_altered_5}){{0,1}}"
        f"({_others}){{0,1}}"
        f"(?:/({_note_pattern})){{0,1}}"
        )
    _symbols = {
        'b': '\u266D', 'bb': '\U0001D12B',
        '#': '\u266F', '##': '\U0001D12A',
        None: '',
        }
    _quality_intervals = {
        (7,): 'power',
        (4, 3): 'major',
        (3, 4): 'minor',
        (3, 3): 'diminished',
        (4, 4): 'augmented',
        (4, 3, 3): 'dominant',
        (4, 3, 4): 'major',
        (3, 4, 3): 'minor',
        (3, 4, 4): 'minor-major',
        (3, 3, 3): 'diminished',
        (3, 3, 4): 'half-diminished',
        (4, 4, 2): 'augmented',
        (4, 4, 3): 'augmented-major',
    }
    _ext_words = {
        None: '',
        'M7': 'seventh',
        'M9': 'ninth',
        'M11': 'eleventh',
        'M13': 'thirteenth',
        'm9': 'minor ninth',
        'm11': 'minor eleventh',
        'm13': 'minor thirteenth',
    }
    NE = NoteEditor()

    def create_chord(self, value):
        """Create a chord from a string (do not use any spaces)."""
        if not isinstance(value, str):
            raise TypeError("Only strings are accepted")
        rgx = re.match(ChordEditor._pattern, value, re.UNICODE)
        if not rgx:
            raise ValueError("Chord could not be recognised")
        root, quality, sus, add, bass = self._parse_rgx(rgx)
        return Chord(root, quality, sus, add, bass, string=rgx.group(0))

    def _parse_rgx(self, rgx):
        """Parse chord notation regex."""
        root = self._parse_root(rgx)
        temp_q, extension = self._parse_quality(rgx)
        q = self._parse_alt5(rgx, temp_q)  # altered 5th may change quality
        quality = "{} {}".format(
            ChordEditor._quality_intervals[tuple(q)],
            ChordEditor._ext_words[extension],
            ).strip()
        sus, add = self._parse_others(rgx)
        bass_note = self._parse_bass(rgx)
        return root, quality, sus, add, bass_note

    def _parse_root(self, rgx):
        """Return chord root."""
        return self.NE.create_note(rgx.group(1))

    def _parse_quality(self, rgx):
        """Return chord quality and extension."""
        if rgx.group(3):
            return [7], None
        if rgx.group(4):
            return self._parse_ext(rgx)
        if rgx.group(16):
            return self._parse_triad(rgx)
        if rgx.group(1)[0].isupper():
            return [4, 3], None
        return [3, 4], None

    def _parse_ext(self, rgx):
        """Parse quality of extended chords."""
        if not rgx.group(5):
            if rgx.group(1)[0].isupper():
                quality = [4, 3, 3]
            else:
                quality = [3, 4, 3]
        elif rgx.group(6):
            quality = [3, 4, 4]
        elif rgx.group(7):
            quality = [4, 4, 3]
        elif rgx.group(8):
            quality = [4, 4, 2]
        elif rgx.group(9):
            quality = [3, 3, 3]
        elif rgx.group(10):
            quality = [3, 3, 4]
        elif rgx.group(11):
            quality = [4, 3, 4]
        elif rgx.group(12):
            quality = [3, 4, 3]
        if rgx.group(14):
            ext = 'm'
        else:
            ext = 'M'
        ext += rgx.group(15)
        return quality, ext

    def _parse_triad(self, rgx):
        """Parse quality of triads."""
        if rgx.group(17):
            return [4, 4], None
        if rgx.group(18):
            return [3, 3], None
        if rgx.group(19):
            return [4, 3], None
        return [3, 4], None

    def _parse_alt5(self, rgx, temp_q):
        """Change the quality for chords with altered fifths."""
        if not rgx.group(21):
            return temp_q
        if rgx.group(21) in ChordEditor._dim_pattern+ChordEditor._flat_pattern:
            temp_q[1] -= 1
            if len(temp_q) > 2:
                temp_q[2] += 1
        else:
            temp_q[1] += 1
            if len(temp_q) > 2:
                temp_q[2] -= 1
        return temp_q

    def _parse_others(self, rgx):
        """Parse suspended and added notes."""
        if not rgx.group(22):
            return None, None
        string = rgx.group(22)
        # sus
        reg = re.search(ChordEditor._suspended, string, re.UNICODE)
        if reg:
            note = reg.group(1) or 4  # if 'sus'
            sus = int(note)
            string = ''.join(string.split(reg.group(0)))
        else:
            sus = None
        # add
        add = []
        while True:
            reg = re.search(ChordEditor._added, string, re.UNICODE)
            if not reg:
                break
            foo = ChordEditor._symbols[reg.group(1)]+reg.group(2)
            add.append(foo)
            string = ''.join(string.split(reg.group(0)))
        if string.strip():
            raise SyntaxError(f"String '{string.strip()}' could not be parsed")
        return sus, add or None

    def _parse_bass(self, rgx):
        """Parse the bass note."""
        if not rgx.group(23):
            return None
        return self.NE.create_note(rgx.group(23))

    def _xstr(self, value):
        # To print blank for None values
        if value is None:
            return ''
        return value

    def create_diatonic(
            self,
            value: Union[Scale, Key],
            degree: int = 1,
    ):
        """Create a diatonic chord from a scale/key by specifying the scale degree."""
        if degree not in {1, 2, 3, 4, 5, 6, 7}:
            raise ValueError("Scale degree must be between 1 and 7")
        if isinstance(value, Key):
            scale_ = Scale(value)
        else:
            scale_ = value
        root = scale_.notes[degree-1]
        bass = None
        sus = None
        add = None
        base_chord = (
            scale_.notes[degree-1],
            scale_.notes[degree+1],
            scale_.notes[degree+3],
            )
        interval = self.NE.get_intervals(*base_chord)
        quality = ChordEditor._quality_intervals[interval]
        return Chord(root, quality, sus, add, bass)

    def change_chord(
            self,
            chord,
            root: Union[Note, None] = None,
            quality: Union[str, None] = None,
            sus: Union[int, bool, None] = None,
            add: Union[List[str], None] = None,
            remove: Union[List[str], None] = None,
            bass: Union[Note, bool, None] = None,
    ):
        """Change the chord by specifying root, quality, sus, add, remove (you can only remove added notes), and/or bass. To remove the bass or sus note, use the argument False. To remove all added notes, use remove=True."""
        if not isinstance(chord, Chord):
            raise TypeError(f"Object {chord} is not a 'Chord'")
        if root:
            chord.root = self.NE.create_note(root)
        if quality:
            q_list = quality.split()
            words = len(q_list)
            if q_list[0] not in ChordEditor._quality_intervals.values():
                raise ValueError(f"Could not parse {quality}")
            if words == 2:
                if q_list[1] not in ChordEditor._ext_words.values():
                    raise ValueError(f"Could not parse {quality}")
            if words == 3:
                if f"{q_list[1]} {q_list[2]}" not in ChordEditor._ext_words.values():
                    raise ValueError(f"Could not parse {quality}")
            if words < 1 or words > 3:
                raise ValueError(f"Could not parse {quality}")
            if words != 1 and q_list[0] == 'power':
                raise ValueError(f"Could not parse {quality}")
            chord.quality = quality
        if sus not in {2, 4, False, None}:
            raise ValueError(f"Could not parse {sus}")
        elif sus is not None:
            chord.sus = sus or None
        if remove is True:
            chord.add = None
        elif remove:
            for each in remove:
                rgx = re.match(f"^{ChordEditor._added}$", each)
                if not rgx:
                    raise ValueError(f"Could not parse {each}")
                new_each = ChordEditor._symbols[rgx.group(1)] + rgx.group(2)
                if not chord.add or new_each not in chord.add:
                    raise ValueError(f"{each} is not an added note")
                chord.add.remove(new_each)
            chord.add = chord.add or None
        if add:
            chord.add = chord.add or []
            for each in add:
                rgx = re.match(f"^{ChordEditor._added}$", each)
                if not rgx:
                    raise ValueError(f"Could not parse {each}")
                new_each = ChordEditor._symbols[rgx.group(1)] + rgx.group(2)
                chord.add.append(new_each)
        if bass:
            chord.bass = self.NE.create_note(bass)
        if bass is False:
            chord.bass = None
        chord.build()
        return chord

