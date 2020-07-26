from unittest import mock

import pytest

from chordparser.analysers.chords_analyser import ChordAnalyser
from chordparser.editors.chords_editor import ChordEditor
from chordparser.editors.keys_editor import KeyEditor
from chordparser.editors.notes_editor import NoteEditor
from chordparser.editors.scales_editor import ScaleEditor
from chordparser.music.notes import Note
from chordparser.parser import Parser


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
    assert cp.to_roman(c, s) == "I"


def test_attribute_error():
    with pytest.raises(AttributeError):
        Note.num_value(cp)


@mock.patch("chordparser.parser.Parser")
def test_IO_error(mock_parser):
    mock_parser._path = ""
    p = Parser()
    assert "" == p.sample
