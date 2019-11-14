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
    note_pattern = '([a-gA-G])'
    symbol_pattern = '(\u266F|\u266D|\U0001D12B|\U0001D12A|bb|##|b|#)'
    major_pattern = '(Maj|Ma|M|maj|\u0394)'
    minor_pattern = '(min|m|-)'
    dim_pattern = '(dim|o|\u00B0)'
    aug_pattern = '(aug|\+)'
    halfdim_pattern = '(\u00f8|\u00d8)'
    dom_pattern = '(dom7|dom)'
    pattern = (
        f"{note_pattern}{symbol_pattern}{{0,1}}"
        f"({major_pattern}|{minor_pattern}|"
        f"{dim_pattern}|{aug_pattern}|"
        f"{halfdim_pattern}|{dom_pattern}){{0,1}}(.*)"
        )

    def __init__(self, value):
        if not isinstance(value, str):
            raise TypeError("Only strings are accepted")
        self.rgx = re.match(Chord.pattern, value, re.UNICODE)
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
        pattern = f'/{Chord.note_pattern}{Chord.symbol_pattern}''{0,1}$'
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
            if re.match('7', self.rgx.group(10)):
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
        elif self.rgx.group(4) and re.match('7', self.other):
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
        """Modify notes based on other and bass attributes."""
        self._parse_other()
        self._parse_bass()
        return
        # then read other and bass to modify it - notes

    def _parse_other(self):
        """Modify notes based on other."""
        pass

    def _parse_bass(self):
        """Modify notes to put bass note on the bass."""
        pass

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
