import pytest

from chordparser.music.roman import Roman


def test_notation():
    r = Roman("I", "M+", (6, 4))
    assert "IM+64" == str(r)


def test_notation_2():
    r = Roman("v", "\u00B0", ())
    assert "v\u00B0" == str(r)


def test_notation_3():
    r = Roman("IV", "+", (6,))
    assert "IV+6" == str(r)


def test_equality():
    r = Roman("I", "+", (6,))
    o = Roman("I", "+", (6,))
    assert r == o


def test_equality_2():
    r = Roman("IV", "+", (6,))
    assert "IV+6" == r
