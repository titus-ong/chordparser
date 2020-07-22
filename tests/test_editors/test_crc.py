import pytest

from chordparser.editors.chord_roman_converter import ChordRomanConverter
from chordparser.editors.chords_editor import ChordEditor
from chordparser.editors.keys_editor import KeyEditor
from chordparser.editors.scales_editor import ScaleEditor


SE = ScaleEditor()
CE = ChordEditor()
KE = KeyEditor()
CRC = ChordRomanConverter()


def test_roman_scale():
    c = CE.create_chord("C")
    s = SE.create_scale("C")
    assert "I" == str(CRC.to_roman(c, s))


def test_roman_key():
    c = CE.create_chord("C")
    k = KE.create_key("C", "major")
    assert "I" == str(CRC.to_roman(c, k))


@pytest.mark.parametrize(
    "chord, roman", [
        ("C", "I"),
        ("Cm", "i"),
        ("Cb", '\u266dI'),
        ]
    )
def test_roman_root(chord, roman):
    c = CE.create_chord(chord)
    s = SE.create_scale("C", "major")
    assert CRC._get_roman_root(c, s) == roman


@pytest.mark.parametrize(
    "chord, roman", [
        ("C7", (7,)),
        ("C7/G", (4, 3)),
        ("C9/G", (9,)),
        ("C/E", (6,)),
        ]
    )
def test_roman_inversion(chord, roman):
    c = CE.create_chord(chord)
    assert CRC._get_roman_inversion(c) == roman


@pytest.mark.parametrize(
    "chord, roman", [
        ("C7", ""),
        ("Cmaj7", "M"),
        ("Caugmaj7", "M+"),
    ]
)
def test_roman_quality(chord, roman):
    c = CE.create_chord(chord)
    assert CRC._get_roman_quality(c) == roman


def test_power_warning():
    c = CE.create_chord("C5")
    s = SE.create_scale("C", "major")
    with pytest.warns(UserWarning):
        CRC.to_roman(c, s)


def test_sus_warning():
    c = CE.create_chord("Csus")
    s = SE.create_scale("C", "major")
    with pytest.warns(UserWarning):
        CRC.to_roman(c, s)


