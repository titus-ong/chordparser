"""
Parse chord notation and return key and mode.
"""
from .notes import Note, Key
from .scales import Scale
from typing import Union
import re


class Chord:
    """
    Chord class that is composed of a root, chord quality, base triad, and optionally a bass note and altered or added notes.

    Arguments:
    value -- the chord notation (str)

    The Chord class is built from the chord notation. It parses the notation and provides the 'root', 'quality' and 'base_chord' attributes for the root, chord quality and base chord respectively. The bass note and additional alterations to the chord can be accessed via the 'bass_note' and 'other' attributes.

    The Chord class can be transposed using the 'transpose' method. Its string form can also be altered using the 'format' method.
    """
    _note_pattern = '([a-gA-G])'
    _symbol_pattern = '(\u266F|\u266D|\U0001D12B|\U0001D12A|bb|##|b|#)'
    _major_pattern = '(Maj|Ma|M|maj|\u0394)'
    _minor_pattern = '(min|m|-)'
    _dim_pattern = '(dim|o|\u00B0)'
    _aug_pattern = '(aug|\+)'
    _halfdim_pattern = '(\u00f8|\u00d8)'
    _dom_pattern = '(dom7|dom)'
    _pattern = (
        f"{_note_pattern}{_symbol_pattern}{{0,1}}"
        f"({_major_pattern}|{_minor_pattern}|"
        f"{_dim_pattern}|{_aug_pattern}|"
        f"{_halfdim_pattern}|{_dom_pattern}){{0,1}}(.*)"
        )
    _power_chord = "5"
    _extended_str = f"{_symbol_pattern}{{0,1}}(13|11|9)"
    _altered_5 = f"{_symbol_pattern}(5)"
    _added = "add(13|11|9|2|4|6)"
    _suspended = "sus(2|4){0,1}"
    _symbols = {
        '\u266D': -1, '\U0001D12B': -2,
        '\u266F': +1, '\U0001D12A': +2,
        'b': -1, 'bb': -2,
        '#': +1, '##': +2,
        'flat': -1, 'doubleflat': -2,
        'sharp': +1, 'doublesharp': +2,
        None: 0,
        }

    def __init__(self, value):
        if not isinstance(value, str):
            raise TypeError("Only strings are accepted")
        self.rgx = re.match(Chord._pattern, value, re.UNICODE)
        if not self.rgx:
            raise ValueError("Chord could not be recognised")
        self._parse_rgx()

    def _parse_rgx(self):
        """Parse chord notation regex."""
        self.root = self._parse_root()
        self.other, self.bass_note = self._split_other_bass()
        self.quality, self.quality_short = self._parse_quality()
        self.base_chord = self._parse_base_chord()
        self._parse_other_bass()

    def _parse_root(self):
        """Return chord root."""
        note = self.rgx.group(1)
        accidental = self.rgx.group(2) or ''
        return Note(note + accidental)

    def _split_other_bass(self):
        """Return other alterations and bass note. Return None, None if they do not exist."""
        if not self.rgx.group(10):
            return None, None
        pattern = f'/{Chord._note_pattern}{Chord._symbol_pattern}''{0,1}$'
        regex = re.search(pattern, self.rgx.group(10), re.UNICODE)
        if regex:
            bass_note = Note(regex.group(1) + self._xstr(regex.group(2)))
        else:
            bass_note = None
        other = self.rgx.group(10).split("/")[0]
        return other, bass_note

    def _parse_quality(self):
        """Return chord quality."""
        quality_short = {
            "major": '',
            "minor": 'm',
            "diminished": 'dim',
            "augmented": 'aug',
            "half-diminished": '\u00d8',
            "dominant": 'dom',
            "major7": 'maj',
            }
        if not self.rgx.group(3) and self.rgx.group(1).isupper():
            if re.match('13|11|9|7', self.rgx.group(10)):
                # E.g. C7
                quality = 'dominant'
            else:
                # E.g. C
                quality = 'major'
        elif not self.rgx.group(3):
            # lowercase root
            quality = 'minor'
        elif self.rgx.group(4):
            quality = 'major'
        elif self.rgx.group(5):
            quality = 'minor'
        elif self.rgx.group(6):
            quality = 'diminished'
        elif self.rgx.group(7):
            quality = 'augmented'
        elif self.rgx.group(8):
            quality = 'half-diminished'
        elif self.rgx.group(9):
            quality = 'dominant'
        else:
            raise SyntaxError("Quality could not be parsed")
        # Account for major7
        quality = self._parse_maj7(quality)
        return quality, quality_short[quality]

    def _parse_maj7(self, quality):
        """Include 7 if major seventh chord."""
        if not self.other:
            string = ''
        elif self.rgx.group(4) and re.match('13|11|9|7', self.other):
            string = '7'
        else:
            string = ''
        return (quality + string)

    def _parse_base_chord(self):
        """Return base triad."""
        base_quality = {
            'major': ("major", 0),
            'minor': ("minor", 0),
            'diminished': ("minor", -1, -1),
            'augmented': ("major", 1),
            'half-diminished': ("minor", -1, 0),
            'dominant': ("major", 0, -1),
            'major7': ("major", 0, 0),
        }
        info = base_quality[self.quality]
        self._key = Key(self.root, info[0])
        self._scale = Scale(self._key)
        base_chord = [
                self._scale.notes[0],
                self._scale.notes[2],
                self._scale.notes[4].shift(info[1]),
                ]
        if len(info) == 3:
            base_chord.append(
                self._scale.notes[6].shift(info[2]),
                )
        return tuple(base_chord)

    def _parse_other_bass(self):
        """Build notes attribute from other and bass attributes."""
        self._parse_other()
        self._parse_bass()
        return

    def _parse_other(self):
        """Modify notes based on additional strings."""
        self.notes = list(self.base_chord)
        self._string = self.other
        if self.other is None:
            return
        if self.other[0] == '7':  # 7th has already been parsed
            self._string = self._string[1::].strip()
        while self._string.strip():
            regex = re.match(Chord._power_chord, self._string)
            if regex:
                self._parse_power_chord(regex)
            regex = re.match(Chord._extended_str, self._string, re.UNICODE)
            if regex:
                self._parse_ext_chord(regex)
            regex = re.match(Chord._altered_5, self._string, re.UNICODE)
            if regex:
                self._parse_alt5_chord(regex)
            regex = re.match(Chord._added, self._string)
            if regex:
                self._parse_add_chord(regex)
            regex = re.match(Chord._suspended, self._string)
            if regex:
                self._parse_sus_chord(regex)
        return

    def _parse_power_chord(self, regex):
        """Remove the third."""
        self.notes.pop(1)
        self._string = self._string[1::].strip()

    def _parse_ext_chord(self, regex):
        """Extend the chord."""
        symbol = regex.group(1)
        interval = int(regex.group(2))
        extend = []
        while interval > 7:
            extend.insert(0, self._scale.notes[interval - 1])
            interval -= 2
        extend[-1].shift(Chord._symbols[symbol])
        self.notes += extend
        self._string = self._string[len(regex.groups())::].strip()

    def _parse_alt5_chord(self, regex):
        """Alter the fifth."""
        symbol = regex.group(1)
        self.notes[2].shift(Chord._symbols[symbol])
        self._string = self._string[len(regex.groups())::].strip()

    def _parse_add_chord(self, regex):
        """Add note in correct position."""
        position = {
            '2': 1, '4': 2, '6': 3,
        }
        idx = int(regex.group(1)) - 1
        note = self._scale.notes[idx]
        if regex.group(1) in position.keys():
            self.notes.insert(position[regex.group(1)], note)
        else:
            self.notes.append(note)
        self._string = self._string[len(regex.groups())+3::].strip()

    def _parse_sus_chord(self, regex):
        """Replace third with suspended note."""
        idx = int(regex.group(1)) - 1
        note = self._scale.notes[idx]
        self.notes[1] = note
        self._string = self._string[len(regex.groups())+3::].strip()

    def _parse_bass(self):
        """Modify notes to put bass note in front."""
        # Check if bass is already part of chord
        for each in self.notes:
            if self.bass_note == each:
                self.notes.pop(each)
        self.notes.insert(0, self.bass_note)
        return

    def transpose(self, value: int = 0, use_flats: bool = False):
        """Transpose chord."""
        if not isinstance(value, int):
            raise TypeError("Only integers are accepted")
        self.root.transpose(value, use_flats=use_flats)
        if self.bass_note:
            self.bass_note.transpose(value, use_flats=use_flats)
            print(self.bass_note, self.bass_note.num_value())
            # Make sure bass note is in the correct key e.g. D#/F## not D#/G
            self._key.root = self.root
            self._scale.key = self._key
            for each in self._scale.notes:
                print(each, each.num_value())
                if self.bass_note.num_value() == each.num_value():
                    self.bass_note = each
        # for each in self.notes:
        #     each.transpose(value, use_flats=use_flats)
        # transpose base_chord as well
        return self

    def format(self, options):
        """Specify options to format string output."""
        pass

    def _xstr(self, value):
        # To print blank for None values
        if value is None:
            return ''
        return value

    def __repr__(self):
        if self.bass_note:
            return (
                f'{self.root}{self.quality_short}{self._xstr(self.other)}'
                f'/{self.bass_note} chord'
                )
        else:
            return (
                f'{self.root}{self.quality_short}{self._xstr(self.other)}'
                f' chord'
                )
