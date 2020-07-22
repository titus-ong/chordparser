import pytest

from chordparser.editors.chord_roman_converter import ChordRomanConverter
from chordparser.editors.chords_editor import ChordEditor
from chordparser.editors.scales_editor import ScaleEditor


SE = ScaleEditor()
CE = ChordEditor()
CRC = ChordRomanConverter()


@pytest.mark.parametrize(
    "chord, roman", [
        ("C", "I"),
        ("Cm", "i"),
        ("Cb", '\u266dI'),
        ("C7", "I7"),
        ("C7/G", "I43"),
        ("C9/G", "I9"),
        ("Cdim7", "i\u00B07"),
        ]
    )
def test_roman(chord, roman):
    c = CE.create_chord(chord)
    s = SE.create_scale("C", "major")
    assert str(CRC.to_roman(c, s)) == roman


def test_power_error():
    c = CE.create_chord("C5")
    s = SE.create_scale("C", "major")
    with pytest.warns(UserWarning):
        CRC.to_roman(c, s)


def test_sus_warning():
    c = CE.create_chord("Csus")
    s = SE.create_scale("C", "major")
    with pytest.warns(UserWarning):
        CRC.to_roman(c, s)


