from chordparser.notes_editor import NoteEditor
from chordparser.keys_editor import KeyEditor
from chordparser.scales_editor import ScaleEditor
from chordparser.chords_editor import ChordEditor
from chordparser.chords_analyser import ChordAnalyser
import pytest


NE = NoteEditor()
KE = KeyEditor()
SE = ScaleEditor()
CE = ChordEditor()
CA = ChordAnalyser()


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
    assert CA.roman(c, s) == roman


def test_power_error():
    c = CE.create_chord("C5")
    s = SE.create_scale("C", "major")
    with pytest.raises(ValueError):
        CA.roman(c, s)


def test_sus_warning():
    c = CE.create_chord("Csus")
    s = SE.create_scale("C", "major")
    with pytest.warns(UserWarning):
        CA.roman(c, s)


@pytest.mark.parametrize(
    "chord, mode, incl_submodes, result", [
        ("C", "major", True, [('I', 'major', None)]),
        ("C7", "major", False, [('I7', 'major', None)]),
        ("Cm", "minor", False, [('i', 'minor', 'natural')]),
        ("Cm", "minor", True, [('i', 'minor', 'natural'), ('i', 'minor', 'harmonic'), ('i', 'minor', 'melodic')]),
        ]
    )
def test_diatonic(chord, mode, incl_submodes, result):
    c = CE.create_chord(chord)
    s = SE.create_scale("C", mode)
    assert CA.analyse_diatonic(c, s, incl_submodes) == result


def test_all():
    c = CE.create_chord("Db")
    s = SE.create_scale("C", "locrian")
    assert CA.analyse_all(c, s) == [('\u266dII', 'locrian', None), ('\u266dII', 'phrygian', None)]
