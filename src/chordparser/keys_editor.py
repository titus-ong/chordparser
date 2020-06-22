from chordparser.notes import Note
from chordparser.keys import Key
from chordparser.notes_editor import NoteEditor
from typing import Union
import re


class KeyEditor:
    """
    KeyEditor class that can create a Key and change keys to their relative major/minor.

    The KeyEditor class can create a Key using the 'create_key' method by accepting a Note (or a string that can be parsed by NoteEditor), an optional mode (default 'major') and optional submode. Submodes are only available for the minor/aeolian mode. The 'relative_major' and 'relative_minor' methods change the key into its relative major/minor (submode can be specified for relative_minor).
    """
    _modes = (
        'major', 'minor', 'ionian', 'dorian', 'phrygian',
        'lydian', 'mixolydian', 'aeolian', 'locrian'
        )
    _submodes = {
        'minor': ('harmonic', 'melodic', 'natural'),
        'aeolian': ('harmonic', 'melodic', 'natural'),
        }
    _notes_tuple = (
        'C', 'D', 'E', 'F', 'G', 'A', 'B',
        'C', 'D', 'E', 'F', 'G', 'A', 'B')

    def create_key(
            self,
            root,
            mode: str = 'major',
            submode: Union[str, None] = None
    ):
        """Create a Key from a root note, optional mode (default 'major') and optional submode."""
        # root note
        if not isinstance(root, Note):
            try:
                NE = NoteEditor()
                root = NE.create_note(root)
            except TypeError:
                raise TypeError("Only Notes and strings are accepted for root note")
        # mode
        if not isinstance(mode, str):
            raise TypeError("Only strings are accepted for mode")
        if mode.lower() not in KeyEditor._modes:
            raise KeyError("Mode could not be found")
        # submode
        if submode is None:
            pass
        elif not isinstance(submode, str):
            raise TypeError("Only strings are accepted")
        else:
            submode_tuple = KeyEditor._submodes.get(mode.lower())
            if submode_tuple is None:
                raise KeyError("Mode does not have any submodes")
            if submode.lower() not in submode_tuple:
                raise KeyError("Submode could not be found")
            submode = submode.lower()
        return Key(root, mode.lower(), submode)

    def relative_major(self, key):
        if not key.mode in {'minor', 'aeolian'}:
            raise KeyError("Key is not minor")
        idx = KeyEditor._notes_tuple.index(key.letter())
        key.transpose(3)
        new_idx = KeyEditor._notes_tuple.index(key.letter())
        if new_idx-idx != 2:  # must transpose 2 letters
            key.transpose(0, use_flats=True)
        key.submode = None
        key.mode = 'major'
        return key

    def relative_minor(self, key, submode='natural'):
        if not key.mode in {'major', 'ionian'}:
            raise KeyError("Key is not major")
        if submode not in KeyEditor._submodes['minor']:
            raise KeyError("Submode could not be found")
        idx = KeyEditor._notes_tuple.index(key.letter())
        key.transpose(-3)
        new_idx = KeyEditor._notes_tuple.index(key.letter())
        if new_idx-idx != -2:  # transpose 2 letters
            key.transpose(0, use_flats=True)
        key.submode = submode
        key.mode = 'minor'
        return key
