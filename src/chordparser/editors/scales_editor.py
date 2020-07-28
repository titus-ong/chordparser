from chordparser.editors.keys_editor import KeyEditor
from chordparser.music.keys import Key
from chordparser.music.scales import Scale


class ScaleEditor:
    """A `Scale` editor that can create and change `Scales`.

    The `ScaleEditor` class can create a `Scale` from a `Key` or a `Key`'s notation. It can change the `Scale` by specifying a different `Key` it is based on.

    """

    _KE = KeyEditor()

    def create_scale(self, value, *args, **kwargs):
        """Create a `Scale`.

        Specify either a `Key` or the parameters necessary to create a `Key`.

        Parameters
        ----------
        value
            Either a `Key` or the first parameter for creating a `Key` (i.e. the `root`).
        *args : iterable
            The parameters for creating a `Key`.
        **kwargs : dict
            The keyword parameters for creating a `Key`.

        Returns
        -------
        Scale
            The created `Scale`.

        See Also
        --------
        chordparser.KeyEditor.create_key : See the necessary parameters for creating a `Key`.

        Examples
        --------
        >>> SE = ScaleEditor()
        >>> KE = KeyEditor()
        >>> c_key = KE.create_key("C", "minor")
        >>> SE.create_scale(c_key)
        C natural minor scale
        >>> SE.create_scale("C", "major")
        C major scale

        """
        if not isinstance(value, Key):
            key = self._KE.create_key(value, *args, **kwargs)
        else:
            key = value
        return Scale(key)

    def change_scale(self, scale, *args, inplace=True, **kwargs):
        """Change a `Scale` based on its `Key`.

        The parameters accepted are the same parameters accepted for changing a `Key`: the `root`, `mode` and `submode`. The `root` must be a valid `Note` notation if type `str`. The `submode` refers to the different types of 'minor'/ 'aeolian' mode, i.e. 'natural', 'harmonic' and 'melodic'. Hence, other than the 'minor'/ 'aeolian' `mode`, the `submode` must be None.

        Parameters
        ----------
        scale : Scale
            The `Scale` which key you want to change.
        *args : iterable
            The parameters for changing the `Scale`'s `Key`.
        inplace : boolean, Optional
            Selector to change the current `Scale` or to return a new `Scale`. Default True when optional.
        **kwargs : dict
            The keyword parameters for changing the `Scale`'s `Key`.

        Returns
        -------
        Scale
            The `Scale` with the new `Key`.

        Examples
        --------
        >>> SE = ScaleEditor()
        >>> c = SE.create_scale("C", "major")
        >>> SE.change_scale(c, "D", "lydian")
        D lydian scale
        >>> SE.change_scale(c, "E", "dorian", inplace=False)
        E dorian scale
        >>> c
        D lydian scale

        """
        if not inplace:
            scale = self.create_scale(scale.key)
        self._KE.change_key(scale.key, *args, **kwargs)
        scale.build()
        return scale
