import pytest

from chordparser.music.symbol import Symbol
from chordparser.utils.unicode_chars import flat, doublesharp


class TestSymbolAsInt:
    @pytest.mark.parametrize(
        "symbol, value", [
            ("", 0),
            ("#",  1),
            ("bb", -2),
        ]
    )
    def test_correct_int(self, symbol, value):
        this = Symbol(symbol)
        assert value == this.as_int()


class TestSymbolShiftBy:
    @pytest.mark.parametrize(
        "shift, value", [
            (2, doublesharp),
            (-1, flat),
        ]
    )
    def test_correct_shift(self, shift, value):
        this = Symbol("")
        this.shift_by(shift)
        assert value == this

    def test_symbol_out_of_range(self):
        this = Symbol("")
        with pytest.raises(ValueError):
            this.shift_by(3)
