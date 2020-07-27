import re
from typing import Union

from chordparser.editors.notes_editor import NoteEditor
from chordparser.editors.quality_editor import QualityEditor
from chordparser.music.chords import Chord
from chordparser.music.keys import Key
from chordparser.music.quality import Quality
from chordparser.music.scales import Scale


class ChordEditor:
    """A `Chord` editor that can create and change `Chords`.

    The `ChordEditor` can create a `Chord` from standard chord notation, or by specifying a scale degree based on a `Scale`. It can also change the `Chord`'s attributes.

    """

    _NE = NoteEditor()
    _QE = QualityEditor()
    _letter_pattern = '[a-gA-G]'
    _flat_pattern = '\u266D|\U0001D12B|bb|b'
    _sharp_pattern = '\u266F|\U0001D12A|##|#'
    _symbol_pattern = f"{_flat_pattern}|{_sharp_pattern}"
    _note_pattern = f"(?:{_letter_pattern})(?:{_symbol_pattern}){{0,1}}"
    _others = f"[^/]+"
    _added = f"(?:add){{0,1}}({_symbol_pattern}){{0,1}}(2|4|6|9|11|13)"
    _pattern = (
        f"({_note_pattern})"
        f"({_QE.quality_pattern})"
        f"({_others}){{0,1}}"
        f"(?:/({_note_pattern})){{0,1}}"
    )
    _symbols = {
        'b': '\u266D', 'bb': '\U0001D12B',
        '#': '\u266F', '##': '\U0001D12A',
        None: '',
    }

    def create_chord(self, notation):
        """Create a `Chord`.

        Parameters
        ----------
        notation : str
            The `Chord` notation. Standard chord notation [1]_ is accepted.

        Returns
        -------
        Chord
            The created `Chord`.

        Raises
        ------
        SyntaxError
            If the notation is invalid.
        SyntaxError
            If the string of added notes is invalid.

        References
        ----------
        .. [1] 'Chord letters' (2020) *Wikipedia*. Available at `https://en.wikipedia.org/wiki/Chord_letters <https://en.wikipedia.org/wiki/Chord_letters>`_ (Accessed: 28 July 2020)

        Examples
        --------
        >>> CE = ChordEditor()
        >>> CE.create_chord("C#dim7addb4/E")
        C\u266fdim7add\u266d4/E chord
        >>> CE.create_chord("Ebsus4add#9/G")
        E\u266dsus\u266f9/G chord

        """

        rgx = re.match(ChordEditor._pattern, notation, re.UNICODE)
        if not rgx:
            raise SyntaxError(f"'{notation}' could not be parsed")
        root, quality, add, bass = self._parse_rgx(rgx)
        return Chord(root, quality, add, bass, string=rgx.group(0))

    def _parse_rgx(self, rgx):
        """Distribute regex groups and form chord notation."""
        root = self._parse_root(rgx.group(1))
        quality = self._parse_quality(rgx.group(2), rgx.group(1)[0].isupper())
        add = self._parse_add(rgx.groups()[-2])
        bass_note = self._parse_bass(rgx.groups()[-1])
        return root, quality, add, bass_note

    def _parse_root(self, root):
        """Return chord root."""
        return self._NE.create_note(root)

    def _parse_quality(self, string, capital_note=True):
        """Return chord quality."""
        return self._QE.create_quality(string, capital_note)

    def _parse_add(self, string):
        """Parse added notes."""
        if string is None:
            return None
        add = []
        while True:
            reg = re.search(ChordEditor._added, string, re.UNICODE)
            if not reg:
                break
            foo = (ChordEditor._symbols[reg.group(1)], int(reg.group(2)))
            add.append(foo)
            string = ''.join(string.split(reg.group(0)))
        if string.strip():
            raise SyntaxError(f"'{string.strip()}' could not be parsed")
        add.sort(key=lambda x: x[1])  # sort by scale degree
        return add

    def _parse_bass(self, string):
        """Parse the bass note."""
        if not string:
            return None
        return self._NE.create_note(string)

    def create_diatonic(self, scale_key: Union[Scale, Key], degree: int = 1):
        """Create a diatonic `Chord` from a `Scale` or `Key`.

        Parameters
        ----------
        scale_key : Scale or Key
            The `Scale` or `Key` to create the diatonic `Chord` from.
        degree : int, Optional
            The scale degree of the diatonic `Chord`. Default 1 when optional.

        Returns
        -------
        Chord
            The created diatonic `Chord`.

        Raises
        ------
        ValueError
            If `degree` is not in the range [1, 7].

        Examples
        --------
        >>> KE = KeyEditor()
        >>> SE = ScaleEditor()
        >>> c_key = KE.create_key("C", "major")
        >>> c_scale = SE.create_scale(c_key)
        >>> CE = ChordEditor()
        >>> CE.create_diatonic(c_key, 3)
        Em chord
        >>> CE.create_diatonic(c_scale, 7)
        Bdim chord

        """
        if degree not in range(1, 8):
            raise ValueError("Scale degree must be between 1 and 7")
        if not isinstance(scale_key, Scale):
            scale_ = Scale(scale_key)
        else:
            scale_ = scale_key
        root = scale_.notes[degree - 1]
        bass = None
        add = None
        base_chord = (
            scale_.notes[degree - 1],
            scale_.notes[degree + 1],
            scale_.notes[degree + 3],
        )
        quality_intervals = {
            (4, 3): 'M',
            (3, 4): 'm',
            (3, 3): 'dim',
            (4, 4): 'aug',
        }
        interval = self._NE.get_intervals(*base_chord)
        q_str = quality_intervals[interval]
        quality = self._QE.create_quality(q_str)
        return Chord(root, quality, add, bass)

    def change_chord(
            self,
            chord,
            root: Union[str, None] = None,
            quality: Union[str, None] = None,
            add: Union[str, None] = None,
            remove: Union[str, None] = None,
            bass: Union[str, bool, None] = None,
            inplace=True,
    ):
        """Change a `Chord`'s attributes.

        Alter parts of the `Chord` by specifying the standard chord notation for each attribute.

        Parameters
        ----------
        chord : Chord
            The `Chord` to be changed.
        root : str, Optional
            The root of the `Chord`.
        quality : str, Optional
            The quality of the `Chord`.
        add : str, Optional
            The added notes of the `Chord`.
        remove : str, Optional
            The added notes of the `Chord` that are to be removed.
        bass : str or boolean, Optional
            The bass note of the `Chord`. Specify False to remove the bass note.
        inplace : boolean, Optional
            Selector to change the current `Chord` or to return a new `Chord`. Default True when optional.

        Returns
        -------
        Chord
            The changed `Chord`.

        Examples
        --------
        >>> CE = ChordEditor()
        >>> c = CE.create_chord("C7add4/G")
        >>> CE.change_chord(c, root="D#", quality="maj7", add="b6", remove="4", bass=False)
        D\u266fmaj7\u266d6 chord
        >>> CE.change_chord(c, root="E", quality="m", bass="C#", inplace=False)
        Em\u266d6/C\u266f chord
        >>> c
        D\u266fmaj7\u266d6 chord

        """
        if not inplace:
            chord = Chord(
                chord.root, chord.quality,
                chord.add, chord.bass, chord.string
            )
        if root:
            chord.root = self._parse_root(root)
        if quality:
            chord.quality = self._parse_quality(quality)
        if remove is True:
            chord.add = None
        elif remove:
            removed = self._parse_add(remove)
            for each in removed:
                try:
                    chord.add.remove(each)
                except ValueError:
                    raise ValueError(f"'{each}' is not an added note")
                except AttributeError:
                    raise IndexError("No added notes to be removed")
            chord.add = chord.add or None
        if add:
            chord.add = chord.add or []
            chord.add += self._parse_add(add)
            # re-sort after adding new added notes
            chord.add.sort(key=lambda x: x[1])
        if bass:
            chord.bass = self._parse_bass(bass)
        if bass is False:
            chord.bass = None
        chord.build()
        return chord
