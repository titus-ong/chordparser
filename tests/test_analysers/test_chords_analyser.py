import pytest

from chordparser.analysers.chords_analyser import ChordAnalyser
from chordparser.editors.chords_editor import ChordEditor
from chordparser.editors.keys_editor import KeyEditor
from chordparser.editors.notes_editor import NoteEditor
from chordparser.editors.scales_editor import ScaleEditor


NE = NoteEditor()
KE = KeyEditor()
SE = ScaleEditor()
CE = ChordEditor()
CA = ChordAnalyser()


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


@pytest.mark.parametrize(
    "chord, mode, allow, result", [
        ("C5", "major", True, [('I', 'major', None)]),
        ("C5", "major", False, []),
        ("Csus", "major", True, [('I', 'major', None)]),
        ("Csus", "major", False, []),
        ]
    )
def test_diatonic_power_sus(chord, mode, allow, result):
    c = CE.create_chord(chord)
    s = SE.create_scale("C", mode)
    assert CA.analyse_diatonic(c, s, allow_power_sus=allow) == result


def test_diatonic_default_sus():
    c = CE.create_chord("C5")
    s = SE.create_scale("C", "minor")
    assert CA.analyse_diatonic(
        c, s, allow_power_sus=True,
        default_power_sus="m"
    ) == [('i', 'minor', 'natural')]


def test_all():
    c = CE.create_chord("Db")
    s = SE.create_scale("C", "locrian")
    assert CA.analyse_all(c, s) == [
        ('\u266dII', 'locrian', None),
        ('\u266dII', 'phrygian', None)
    ]


def test_secondary_not_maj_min_dom():
    c = CE.create_chord("Cdim")
    s = SE.create_scale("C")
    assert "" == CA.analyse_secondary(c, c, s)


def test_secondary_tonic():
    c = CE.create_chord("F")
    c2 = CE.create_chord("C")
    s = SE.create_scale("F")
    assert "" == CA.analyse_secondary(c2, c, s)


def test_secondary_dominant():
    c = CE.create_chord("C7")
    c2 = CE.create_chord("G")
    s = SE.create_scale("F")
    assert "V/V" == CA.analyse_secondary(c2, c, s)


def test_secondary_major():
    c = CE.create_chord("C")
    c2 = CE.create_chord("Bdim7")
    s = SE.create_scale("F")
    assert "vii\u00B07/V" == CA.analyse_secondary(c2, c, s)


def test_secondary_minor():
    c = CE.create_chord("Am")
    c2 = CE.create_chord("E")
    s = SE.create_scale("C")
    assert "V/vi" == CA.analyse_secondary(c2, c, s, incl_submodes=True)


def test_secondary_not_diatonic():
    c = CE.create_chord("C7")
    c2 = CE.create_chord("Gm")
    s = SE.create_scale("F")
    assert "" == CA.analyse_secondary(c2, c, s)
