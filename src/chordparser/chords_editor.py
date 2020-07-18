from chordparser.keys import Key
from chordparser.scales import Scale
from chordparser.chords import Chord
from chordparser.quality import Quality
from chordparser.notes_editor import NoteEditor
from chordparser.quality_editor import QualityEditor
from typing import Union
import re


class ChordEditor:
    """
    ChordEditor class that creates a Chord from either a string or a Scale/Key.

    The ChordEditor class can parse a chord notation string to create a Chord using the 'create_chord' method, or create a Chord by specifying a Scale/Key and scale degree using the 'create_diatonic' method. The ChordEditor can also change a chord using the 'change_chord' method.
    """
    NE = NoteEditor()
    QE = QualityEditor()
    _letter_pattern = '[a-gA-G]'
    _flat_pattern = '\u266D|\U0001D12B|bb|b'
    _sharp_pattern = '\u266F|\U0001D12A|##|#'
    _symbol_pattern = f"{_flat_pattern}|{_sharp_pattern}"
    _note_pattern = f"(?:{_letter_pattern})(?:{_symbol_pattern}){{0,1}}"
    _others = f"[^/]+"
    _added = f"(?:add){{0,1}}({_symbol_pattern}){{0,1}}(2|4|6|9|11|13)"
    _pattern = (
        f"({_note_pattern})"
        f"({QE.quality_pattern})"
        f"({_others}){{0,1}}"
        f"(?:/({_note_pattern})){{0,1}}"
    )
    _symbols = {
        'b': '\u266D', 'bb': '\U0001D12B',
        '#': '\u266F', '##': '\U0001D12A',
        None: '',
    }

    def create_chord(self, value):
        """Create a chord from a string (do not use any spaces)."""
        rgx = re.match(ChordEditor._pattern, value, re.UNICODE)
        if not rgx:
            raise SyntaxError(f"'{value}' could not be parsed")
        root, quality, add, bass = self._parse_rgx(rgx)
        return Chord(root, quality, add, bass, string=rgx.group(0))

    def _parse_rgx(self, rgx):
        """Distribute regex groups and form chord notation."""
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
        return self.NE.create_note(root)

    def _parse_quality(self, string, capital_note=True):
        """Return chord quality."""
        return self.QE.create_quality(string, capital_note)

        add = []
        while True:
            reg = re.search(ChordEditor._added, string, re.UNICODE)
            if not reg:
                break
            foo = ChordEditor._symbols[reg.group(1)] + reg.group(2)
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
        root = scale_.notes[degree - 1]
        bass = None
        sus = None
        add = None
        base_chord = (
            scale_.notes[degree - 1],
            scale_.notes[degree + 1],
            scale_.notes[degree + 3],
        )
        interval = self.NE.get_intervals(*base_chord)
        quality = ChordEditor._quality_intervals[interval]
        return Chord(root, quality, sus, add, bass)

    def change_chord(
            self,
            chord,
            root: Union[str, None] = None,
            quality: Union[str, None] = None,
            sus: Union[int, bool, None] = None,
            add: Union[List[str], None] = None,
            remove: Union[List[str], None] = None,
            bass: Union[str, bool, None] = None,
            inplace=True,
    ):
        """Change the chord by specifying root, quality, sus, add, remove (you can only remove added notes), and/or bass. To remove the bass or sus note, use the argument False. To remove all added notes, use remove=True."""
        if not inplace:
            chord = Chord(
                chord.root, chord.quality, chord.sus,
                chord.add, chord.bass, chord.string
            )
        if root:
            chord.root = self.NE.create_note(root)
        if quality:
            chord.quality = self._parse_quality(quality)
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
