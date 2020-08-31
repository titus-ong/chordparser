from chordparser.music.symbol import Symbol


class HasSymbol:
    """Abstract class that contains a `Symbol`."""

    _symbol: Symbol  # To be defined in concrete class

    @property
    def symbol(self):
        return self._symbol

    def raise_by(self, steps=1):
        """Raise the pitch by changing only its `Symbol`.

        The number of steps must be positive. If you wish to change
        the pitch without knowing the number of steps, use shift_by()
        instead.

        Parameters
        ----------
        steps: int, Optional
            The number of steps to raise by. Default 1 when optional.

        Raises
        ------
        ValueError
            If the number of steps is not positive.
        IndexError
            If the new Symbol is not within the range of DOUBLEFLAT and
            DOUBLESHARP.

        Examples
        --------
        The examples are given using `Notes`. They will apply similarly
        to other classes with `Symbols`.

        >>> note = Note("Cb")
        >>> note.raise_by()
        >>> note
        C Note
        >>> note.raise_by(2)
        >>> note
        C\U0001D12A Note

        """
        if steps <= 0:
            raise ValueError(
                f"Expected positive steps, {steps} given. Use lower_by() or "
                "shift_by() instead"
            )
        self.shift_by(steps)

    def lower_by(self, steps=1):
        """Lower the pitch by changing only its `Symbol`.

        The number of steps must be positive. If you wish to change
        the pitch without knowing the number of steps, use shift_by()
        instead.

        Parameters
        ----------
        steps: int, Optional
            The number of steps to lower by. Default 1 when optional.

        Raises
        ------
        ValueError
            If the number of steps is not positive.
        IndexError
            If the new Symbol is not within the range of DOUBLEFLAT and
            DOUBLESHARP.

        Examples
        --------
        The examples are given using `Notes`. They will apply similarly
        to other classes with `Symbols`.

        >>> note = Note("C#")
        >>> note.lower_by()
        >>> note
        C Note
        >>> note.lower_by(2)
        >>> note
        C\U0001D12B Note

        """
        if steps <= 0:
            raise ValueError(
                f"Expected positive steps, {steps} given. Use raise_by() or "
                "shift_by() instead"
            )
        self.shift_by(-steps)

    def shift_by(self, steps):
        """Shift the pitch by changing only its `Symbol`.

        A positive number of steps will raise the pitch, while a
        negative number of steps will lower the pitch.

        Parameters
        ----------
        steps: int
            The number of steps to shift by.

        Raises
        ------
        IndexError
            If the new Symbol is not within the range of DOUBLEFLAT and
            DOUBLESHARP.

        Examples
        --------
        The examples are given using `Notes`. They will apply similarly
        to other classes with `Symbols`.

        >>> note = Note("C#")
        >>> note.shift_by(-1)
        >>> note
        C Note
        >>> note.shift_by(1)
        >>> note
        C\u266f Note

        """
        old_pitch = self._symbol.as_steps()
        new_pitch = old_pitch + steps
        try:
            self._symbol = next(
                symbol for symbol in list(Symbol)
                if new_pitch == symbol.as_steps()
            )
        except StopIteration:
            raise IndexError(
                "New symbol is not within the range of DOUBLEFLAT and "
                "DOUBLESHARP"
            )
