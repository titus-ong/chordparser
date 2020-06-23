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


@pytest.mark.parametrize(
    "attribute, inputs, output", [
        (NoteEditor.create_note, ("C",), NE.create_note("C")),
        (KeyEditor.create_key, ("C", "major"), KE.create_key("C", "major")),
        (ScaleEditor.create_scale, ("C", "major"), SE.create_scale("C", "major")),
        (ChordEditor.create_chord, ("C",), CE.create_chord("C")),
        (ChordAnalyser.roman, (CE.create_chord("C"), SE.create_scale("C")), "I"),
        ]
    )
def test_attributes(attribute, inputs, output):
    assert attribute(cp, *inputs) == output


def test_attribute_error():
    with pytest.raises(AttributeError):
        Note.num_value(cp)
