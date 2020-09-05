from chordparser.music.hassymbol import HasSymbol
from chordparser.music.notationparser import NotationParserTemplate
from chordparser.music.notecomponents.symbol import Symbol
from chordparser.utils.regex_patterns import (symbol_pattern,
                                              degree_pattern,
                                              symbol_converter)


class ScaleDegreeNotationParser(NotationParserTemplate):
    """Parse scale degree notation into degree and symbol."""

    _pattern = f"({symbol_pattern})?({degree_pattern})"

    def _split_into_groups(self, regex):
        symbol = regex.group(1)
        degree = regex.group(2)
        return degree, symbol

class ScaleDegree(HasSymbol):
    """A class representing a scale degree.

    The `ScaleDegree` consists of an integer (the degree) and a
    Symbol. It is created from a string notation with an optional symbol
    and a degree. The degree has to be between 1 and 7, and the symbols
    allowed are b, bb, #, ## or their respective unicode characters
    \u266d, \u266f, \U0001D12B, or \U0001D12A.

    Parameters
    ----------
    notation: str
        The string notation of the `ScaleDegree`.

    Attributes
    ----------
    degree : int
        The degree of the `ScaleDegree`.
    symbol : Symbol
        The accidental of the `ScaleDegree`.

    Examples
    --------
    >>> sd = ScaleDegree("b1")
    >>> sd
    \u266d1 Scale Degree

    """

    _SDNP = ScaleDegreeNotationParser()

    def __init__(self, notation):
        degree, symbol = self._SDNP.parse_notation(notation)
        self._set(degree, symbol)

    def _set(self, degree, symbol):
        self._degree = int(degree)
        self._symbol = symbol_converter[symbol]

    @property
    def degree(self):
        return self._degree

    @classmethod
    def from_components(cls, degree, symbol=""):
        """Create a `ScaleDegree` from its degree and symbol components.

        Parameters
        ----------
        degree: int or str
            The scale degree's integer value.
        symbol: str, Optional
            The symbol's string notation. Default "" when optional.

        Examples
        --------
        >>> sd = ScaleDegree.from_components(3, "b")
        >>> sd
        \u266d3 Scale Degree

        >>> sd = ScaleDegree.from_components("1")
        >>> sd
        1 Scale Degree

        """
        return cls(f"{symbol}{degree}")

    def __str__(self):
        return f"{self._symbol}{self._degree}"

    def __repr__(self):
        return f"{self} Scale Degree"

    def __eq__(self, other):
        """Compare with other `ScaleDegrees` or strings.

        If the other object is a `ScaleDegree`, it must have the same
        degree and symbol as this `ScaleDegree` to be equal. If it is a
        string, they must have the same string representation.

        Parameters
        ----------
        other
            The object to be compared with.

        Returns
        -------
        boolean
            The outcome of the comparison.

        Examples
        --------
        >>> sd = ScaleDegree("b5")
        >>> sd2 = ScaleDegree("b5")
        >>> sd == sd2
        True
        >>> sd3 = ScaleDegree("5")
        >>> sd == sd3
        False
        >>> sd4 = ScaleDegree("b4")
        >>> sd == sd4
        False

        Note that Symbols only use unicode characters when comparing
        with other strings.

        >>> sd = ScaleDegree("#7")
        >>> sd == "#7"
        False
        >>> sd == "\u266f7"
        True

        """
        if isinstance(other, ScaleDegree):
            return (
                self._degree == other.degree and
                self._symbol == other.symbol
            )
        if isinstance(other, str):
            return str(self) == other
        return NotImplemented
