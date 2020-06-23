from chordparser import Parser
from chordparser.notes import Note
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
cp = Parser()


def test_notes():
    assert cp.create_note("C") == NE.create_note("C")


def test_keys():
    assert cp.create_key("C") == KE.create_key("C")


def test_scales():
    assert cp.create_scale("C") == SE.create_scale("C")


def test_chords():
    assert cp.create_chord("C") == CE.create_chord("C")


def test_CA():
    c = CE.create_chord("C")
    s = SE.create_scale("C")
    assert cp.roman(c, s) == "I"


def test_attribute_error():
    with pytest.raises(AttributeError):
        Note.num_value(cp)
