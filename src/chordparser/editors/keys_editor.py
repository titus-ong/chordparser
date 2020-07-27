from typing import Union

from chordparser.editors.notes_editor import NoteEditor
from chordparser.music.keys import Key
from chordparser.music.notes import Note


class ModeError(Exception):
    """Exception where a `Key`'s `mode` is invalid for an operation."""
    pass


class KeyEditor:
    """A `Key` editor that can create `Keys` and manipulate them.

    The `KeyEditor` can create a `Key` from its notation and change it by specifying a different notation. It can also return the relative minor and major of a `Key`.

    """

    _modes = (
        'major', 'minor', 'ionian', 'dorian', 'phrygian',
        'lydian', 'mixolydian', 'aeolian', 'locrian'
    )
    _modes_with_submodes = ('minor', 'aeolian')
    _submodes = ('harmonic', 'melodic', 'natural')
    _NE = NoteEditor()

    def create_key(
            self,
            root,
            mode: str = 'major',
            submode: Union[str, None] = None
    ):
        """Create a `Key` from a root note, mode and submode.

        The root note must be a valid `Note` notation if type `str`. The submode refers to the different types of minor/aeolian mode, i.e. natural, harmonic and melodic. Hence, other than the 'minor'/'aeolian' mode, the submode must be None.

        Parameters
        ----------
        root : Note or str
            The root note of the `Key`.
        mode : {'major', 'minor', 'ionian', 'dorian', 'phrygian', 'lydian', 'mixolydian', 'aeolian', 'locrian'}, Optional
            The mode of the `Key`.
        submode: {None, 'natural', 'harmonic', 'melodic'}, Optional
            The submode of the `Key`. Default 'natural' for the 'minor'/'aeolian' mode and None for the other modes when optional.

        Returns
        -------
        Key
            The created `Key`.

        Raises
        ------
        ModeError
            If the `mode` is not 'minor'/'aeolian' and the `submode` has been specified.
        SyntaxError
            If the `mode` is 'minor'/'aeolian' and the `submode` is invalid.

        Examples
        --------
        >>> KE = KeyEditor()
        >>> KE.create_key("C")
        C major
        >>> KE.create_key("D", "dorian")
        D dorian
        >>> KE.create_key("E", "minor")
        E natural minor
        >>> KE.create_key("F", "minor", "harmonic")
        F harmonic minor

        """
        root = self._check_root(root)
        mode = self._check_mode(mode)
        submode = self._check_submode(mode, submode)
        return Key(root, mode, submode)

    def _check_root(self, root):
        """Check if root note is valid."""
        if not isinstance(root, Note):
            root = KeyEditor._NE.create_note(root)
        return root

    def _check_mode(self, mode):
        """Check if mode is valid."""
        if mode.lower() not in KeyEditor._modes:
            raise SyntaxError(f"'{mode}' could not be parsed")
        return mode.lower()

    def _check_submode(self, mode, submode):
        """Check if submode is valid."""
        if mode not in KeyEditor._modes_with_submodes:
            if submode is None:
                return submode
            raise ModeError(f"'{mode}' does not have any submodes")
        # minor modes
        if submode is None:
            return 'natural'
        if submode.lower() not in KeyEditor._submodes:
            raise SyntaxError(f"'{submode}' could not be parsed")
        return submode.lower()

    def relative_major(self, key):
        """Change a `Key` to its relative major.

        The `Key`'s `mode` must be 'minor'/'aeolian'.

        Parameters
        ----------
        key : Key
            The `Key` to be changed.

        Raises
        ------
        ModeError
            If the `Key` is not 'minor'/'aeolian'.

        Examples
        --------
        >>> KE = KeyEditor()
        >>> key = KE.create_key("D", "minor")
        >>> KE.relative_major(key)
        D major

        """
        if key.mode not in {'minor', 'aeolian'}:
            raise ModeError(f"'{key}' is not minor")
        key.transpose(3, 2)
        key.submode = None
        key.mode = 'major'
        return key

    def relative_minor(self, key, submode='natural'):
        """Change a `Key` to its relative minor.

        The `Key`'s `mode` must be 'major'/'ionian'.

        Parameters
        ----------
        key : Key
            The `Key` to be changed.
        submode : {'natural', 'harmonic', 'melodic'}, Optional
            The new submode of the relative minor `Key`.

        Raises
        ------
        ModeError
            If the `Key` is not 'major'/'ionian'.
        SyntaxError
            If the `submode` is invalid.

        Examples
        --------
        >>> KE = KeyEditor()
        >>> key = KE.create_key("D", "major")
        >>> KE.relative_minor(key)
        D natural minor
        >>> key2 = KE.create_key("E", "major")
        >>> KE.relative_minor(key, "melodic")
        E melodic minor

        """
        if key.mode not in {'major', 'ionian'}:
            raise ModeError(f"'{key}' is not major")
        if submode.lower() not in KeyEditor._submodes:
            raise SyntaxError(f"'{submode}' could not be parsed")
        key.transpose(-3, -2)
        key.submode = submode
        key.mode = 'minor'
        return key

    def change_key(self, key, root=None, mode=None, submode=None, inplace=True):
        """Change a `Key`'s `root`, `mode` and/or `submode` attributes.

        The root note must be a valid `Note` notation if type `str`. The submode refers to the different types of 'minor'/'aeolian' mode, i.e. 'natural', 'harmonic' and 'melodic'. Hence, other than the 'minor'/'aeolian' mode, the submode must be None.

        Parameters
        ----------
        key : Key
            The `Key` which attributes you want to change.
        root : Note, Optional
            The `root` of the `Key` to be changed.
        mode : {None, 'major', 'minor', 'ionian', 'dorian', 'phrygian', 'lydian', 'mixolydian', 'aeolian', 'locrian'}, Optional
            The `mode` of the `Key` to be changed.
        submode: {None, 'natural', 'harmonic', 'melodic'}, Optional
            The submode of the `Key` to be changed. Default 'natural' for the 'minor'/'aeolian' mode and None for the other modes when optional.
        inplace : boolean, optional
            Selector to change the notation of current `Key` or to return a new `Key`. Default True when optional.

        Returns
        -------
        Key
            The `Key` with the new attributes.

        Examples
        --------
        >>> KE = KeyEditor()
        >>> c = KE.create_key("C", "dorian")
        >>> KE.change_key(c, root="D", mode="minor", submode="harmonic")
        D harmonic minor
        >>> KE.change_key(c, mode="major", inplace=False)
        D major
        >>> c
        D harmonic minor

        """
        if not inplace:
            key = self.create_key(key.root, key.mode, key.submode)
        if root:
            key.root = self._check_root(root)
        if mode:
            key.mode = self._check_mode(mode)
        submode = submode or key.submode
        key.submode = self._check_submode(key.mode, submode)
        return key
