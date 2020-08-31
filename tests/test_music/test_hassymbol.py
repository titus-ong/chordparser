import pytest

from chordparser.music.hassymbol import HasSymbol
from chordparser.music.symbol import Symbol


class Symbolful(HasSymbol):
    def __init__(self, symbol):
        self._symbol = symbol

    @property
    def symbol(self):
        return self._symbol


class TestSymbolfulRaiseBy:
    def test_correct_shift(self):
        symbolful = Symbolful(Symbol.NATURAL)
        symbolful.raise_by()
        assert Symbol.SHARP == symbolful.symbol

    @pytest.mark.parametrize(
        "step, symbol", [
            (2, Symbol.SHARP),
            (1, Symbol.NATURAL),
        ]
    )
    def test_correct_shift_with_step(self, step, symbol):
        symbolful = Symbolful(Symbol.FLAT)
        symbolful.raise_by(step)
        assert symbol == symbolful.symbol

    def test_negative_shift_valueerrror(self):
        symbolful = Symbolful(Symbol.NATURAL)
        with pytest.raises(ValueError):
            symbolful.raise_by(-1)

    def test_symbol_not_in_range(self):
        symbolful = Symbolful(Symbol.NATURAL)
        with pytest.raises(IndexError):
            symbolful.raise_by(3)


class TestSymbolfulLowerBy:
    def test_correct_shift(self):
        symbolful = Symbolful(Symbol.NATURAL)
        symbolful.lower_by()
        assert Symbol.FLAT == symbolful.symbol

    @pytest.mark.parametrize(
        "step, symbol", [
            (2, Symbol.FLAT),
            (1, Symbol.NATURAL),
        ]
    )
    def test_correct_shift_with_step(self, step, symbol):
        symbolful = Symbolful(Symbol.SHARP)
        symbolful.lower_by(step)
        assert symbol == symbolful.symbol

    def test_negative_shift_valueerrror(self):
        symbolful = Symbolful(Symbol.NATURAL)
        with pytest.raises(ValueError):
            symbolful.lower_by(-1)

    def test_symbol_not_in_range(self):
        symbolful = Symbolful(Symbol.NATURAL)
        with pytest.raises(IndexError):
            symbolful.lower_by(3)


class TestSymbolfulShiftBy:
    @pytest.mark.parametrize(
        "step, symbol", [
            (2, Symbol.SHARP),
            (1, Symbol.NATURAL),
        ]
    )
    def test_correct_positive_shift(self, step, symbol):
        symbolful = Symbolful(Symbol.FLAT)
        symbolful.shift_by(step)
        assert symbol == symbolful.symbol

    @pytest.mark.parametrize(
        "step, symbol", [
            (-2, Symbol.FLAT),
            (-1, Symbol.NATURAL),
        ]
    )
    def test_correct_negative_shift(self, step, symbol):
        symbolful = Symbolful(Symbol.SHARP)
        symbolful.shift_by(step)
        assert symbol == symbolful.symbol

    def test_symbol_not_in_range(self):
        symbolful = Symbolful(Symbol.NATURAL)
        with pytest.raises(IndexError):
            symbolful.shift_by(3)
