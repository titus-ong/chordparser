class NoteComparer:
    """A class that contains methods for comparing `Note` values.

    The NoteComparer provides methods to find intervals between
    `Notes`. It does not have to be initialised for the methods to be
    used.

    """

    @staticmethod
    def get_semitone_intervals(notes):
        """Get the semitone intervals between an array of `Notes`.

        An array of length greater or equal to 2 is required. The
        interval for each `Note` is relative to the previous `Note`.

        Parameters
        ----------
        notes : array-like
            An array of `Notes`.

        Returns
        -------
        list of int
            The list of semitone intervals between all adjacent `Notes`.

        Raises
        ------
        IndexError
            If the array has a length less than 2.

        Examples
        --------
        >>> c = Note("C")
        >>> f = Note("F")
        >>> a = Note("A")
        >>> NoteComparer.get_semitone_intervals([c, f, a])
        [5, 4]

        """
        NoteComparer._check_array_len("get_semitone_intervals", notes)
        intervals = []
        prev_note = notes[0]
        for note in notes:
            semitone_interval = (note.as_steps()-prev_note.as_steps()) % 12
            intervals.append(semitone_interval)
            prev_note = note
        intervals.pop(0)
        return intervals

    @staticmethod
    def _check_array_len(method, array):
        if len(array) < 2:
            raise IndexError(
                f"{method}() requires an array of length greater or "
                f"equal to 2 but an array of length {len(array)} was "
                "given"
            )

    @staticmethod
    def get_letter_intervals(notes):
        """Get the letter intervals between an array of `Notes`.

        An array of length greater or equal to 2 is required. The
        interval for each `Note` is relative to the previous `Note`.

        Parameters
        ----------
        notes : array-like
            An array of `Notes`.

        Returns
        -------
        list of int
            The list of letter intervals between all adjacent `Notes`.

        Raises
        ------
        IndexError
            If the array has a length less than 2.

        Examples
        --------
        >>> c = Note("C")
        >>> f = Note("F")
        >>> a = Note("A")
        >>> NoteComparer.get_letter_intervals([c, f, a])
        [3, 2]

        """
        NoteComparer._check_array_len("get_letter_intervals", notes)
        intervals = []
        prev_note_idx = notes[0].letter.index()
        for note in notes:
            note_idx = note.letter.index()
            interval = (note_idx-prev_note_idx) % 7
            intervals.append(interval)
            prev_note_idx = note_idx
        intervals.pop(0)
        return intervals

    @staticmethod
    def get_semitone_displacements(notes):
        """Get the semitone displacements between `Notes`.

        An array of length greater or equal to 2 is required. The
        interval for each `Note` is relative to the previous `Note`. By
        displacement, we mean the shortest semitone distance between
        `Notes` that accounts for the direction of the interval, i.e.
        the displacement will be negative if the shortest distance is a
        downwards interval.

        Parameters
        ----------
        notes : Note
            An array of `Notes`.

        Returns
        -------
        list of int
            The list of the semitone displacements between all adjacent
            `Notes`.

        Raises
        ------
        IndexError
            If the array has a length less than 2.

        Examples
        --------
        >>> c = Note("C")
        >>> b = Note("B")
        >>> NoteComparer.get_semitone_intervals(c, b)
        [11]
        >>> NoteComparer.get_semitone_displacements(c, b)
        [-1]

        """
        NoteComparer._check_array_len(
            "get_semitone_displacements", notes
        )
        displacements = []
        intervals = NoteComparer.get_semitone_intervals(notes)
        for interval in intervals:
            displacement = interval if interval <= 6 else interval-12
            displacements.append(displacement)
        return displacements
