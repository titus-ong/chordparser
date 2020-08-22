import pytest

from chordparser.music.letter import Letter


class TestLetterAsInt:
    @pytest.mark.parametrize(
        "letter, value", [
            ("C", 0),
            ("E",  4),
            ("B", 11),
        ]
    )
    def test_correct_int(self, letter, value):
        this = Letter(letter)
        assert value == this.as_int()


class TestLetterShiftBy:
    @pytest.mark.parametrize(
        "shift, value", [
            (2, "E"),
            (-1, "B"),
            (15, "D"),
        ]
    )
    def test_correct_shift(self, shift, value):
        this = Letter("C")
        this.shift_by(shift)
        assert value == this
