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


def test_all():
    c = CE.create_chord("Db")
    s = SE.create_scale("C", "locrian")
    assert CA.analyse_all(c, s) == [('\u266dII', 'locrian', None), ('\u266dII', 'phrygian', None)]
