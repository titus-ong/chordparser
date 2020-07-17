from chordparser.notes import Note
from chordparser.keys import Key
from chordparser.notes_editor import NoteEditor
from typing import Union


class ModeError(Exception):
    """Raise when a key's mode is invalid."""
    pass


class KeyEditor:
    """
    KeyEditor class that can create/change a Key, and change keys to their relative major/minor key.

    The KeyEditor class can create a Key using the 'create_key' method by accepting a Note or string, an optional mode (default 'major') and optional submode. Submodes are only available for the minor/aeolian mode (default 'natural'). The 'relative_major' and 'relative_minor' methods change the key into its relative major/minor (submode can be specified for 'relative_minor'). The 'change_key' method can be used to alter the root, mode and/or submode.
    """
    _modes = (
        'major', 'minor', 'ionian', 'dorian', 'phrygian',
        'lydian', 'mixolydian', 'aeolian', 'locrian'
    )
    _modes_with_submodes = ('minor', 'aeolian')
    _submodes = ('harmonic', 'melodic', 'natural')
    NE = NoteEditor()

    def create_key(
            self,
            root,
            mode: str = 'major',
            submode: Union[str, None] = None
    ):
        """Create a Key from a root note, optional mode (default 'major') and optional submode.

        Arguments:
        root -- root note of the key(Union[Note, str])

        Keyword arguments:
        mode -- mode of the key e.g. major (str)
        submode -- alternate forms of the same mode e.g. harmonic, natural (str)
        """
        root = self._check_root(root)
        mode = self._check_mode(mode)
        submode = self._check_submode(mode, submode)
        return Key(root, mode, submode)

    def _check_root(self, root):
        if not isinstance(root, Note):
            root = KeyEditor.NE.create_note(root)
        return root

    def _check_mode(self, mode):
        if mode.lower() not in KeyEditor._modes:
            raise ValueError("Mode could not be parsed")
        return mode.lower()

    def _check_submode(self, mode, submode):
        if mode not in KeyEditor._modes_with_submodes:
            if submode is None:
                return submode
            raise ModeError("Mode does not have any submodes")
        # minor modes
        if submode is None:
            return 'natural'
        if submode.lower() not in KeyEditor._submodes:
            raise ValueError("Submode could not be parsed")
        return submode.lower()

    def relative_major(self, key):
        """Change a key to its relative major."""
        if key.mode not in {'minor', 'aeolian'}:
            raise ModeError("Key is not minor")
        key.transpose(3, 2)
        key.submode = None
        key.mode = 'major'
        return key

    def relative_minor(self, key, submode='natural'):
        """Change a key to its relative minor."""
        if key.mode not in {'major', 'ionian'}:
            raise ModeError("Key is not major")
        if submode.lower() not in KeyEditor._submodes:
            raise ValueError("Submode could not be parsed")
        key.transpose(-3, -2)
        key.submode = submode
        key.mode = 'minor'
        return key

    def change_key(self, key, root=None, mode=None, submode=None):
        """Change the key by specifying root, mode and/or submode."""
        if root:
            key.root = self._check_root(root)
        if mode:
            key.mode = self._check_mode(mode)
        submode = submode or key.submode
        key.submode = self._check_submode(key.mode, submode)
        return key
