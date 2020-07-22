import pytest

from chordparser.editors.chords_editor import ChordEditor
from chordparser.editors.keys_editor import KeyEditor
from chordparser.editors.notes_editor import NoteEditor
from chordparser.editors.scales_editor import ScaleEditor
from chordparser.music.chords import Chord


NE = NoteEditor()
KE = KeyEditor()
SE = ScaleEditor()
CE = ChordEditor()


@pytest.mark.parametrize(
    "name, chord", [
        ("C", ('C', 'E', 'G')),
        ('Cdim', ('C', 'E\u266d', 'G\u266d')),
        ('Cmaj9', ('C', 'E', 'G', 'B', 'D')),
        ('C5', ('C', 'G')),
        ])
def test_base_notes(name, chord):
    c = CE.create_chord(name)
    assert c.base_notes == chord


@pytest.mark.parametrize(
    "name, notes, sym, deg, intervals", [
        ("Cmaj7add2addb11",
            ('C', 'D', 'E', 'G', 'B', 'F\u266D'),
            ('', '', '', '', '', '\u266D'),
            (1, 2, 3, 5, 7, 11),
            (2, 2, 3, 4, 5)),
        ("Cdimadd11",
            ('C', 'E\u266D', 'G\u266D', 'F'),
            ('', '\u266D', '\u266D', ''),
            (1, 3, 5, 11),
            (3, 3, 11)),
        ])
def test_add_notes(name, notes, sym, deg, intervals):
    c = CE.create_chord(name)
    assert c.notes == notes
    assert c.symbols == sym
    assert c.degrees == deg
    assert c.intervals == intervals


@pytest.mark.parametrize(
    "name, notes, sym, deg, intervals, inversion", [
        ("Cmaj7/G",
            ('G', 'C', 'E', 'B'),
            ('', '', '', ''),
            (5, 1, 3, 7),
            (5, 4, 7),
            (5)),
        ("Cdim/G#",
            ('G\u266F', 'C', 'E\u266D', 'G\u266D'),
            ('\u266F', '', '\u266D', '\u266D'),
            (5, 1, 3, 5),
            (4, 3, 3),
            (None)),
        ])
def test_bass_notes(name, notes, sym, deg, intervals, inversion):
    c = CE.create_chord(name)
    assert c.notes == notes
    assert c.symbols == sym
    assert c.degrees == deg
    assert c.intervals == intervals
    assert c.inversion is inversion


@pytest.mark.parametrize(
    "string, notation", [
        ("Cmajsus2add9/G", "Csus2add9/G chord"),
        ("Cmaj9sus4add#9#13/G#", "Cmaj9sus\u266F9\u266F13/G\u266F chord"),
        ("Caugmaj11", "Cmaj11\u266F5 chord"),
        ("Cadd2", "Cadd2 chord"),
        ("Cadd2addb6", "Cadd2\u266d6 chord"),
        ]
    )
def test_notation(string, notation):
    c = CE.create_chord(string)
    assert repr(c) == notation


@pytest.mark.parametrize(
    "string, semitones, letter, notation", [
        ('C', 3, 1, 'D\u266f chord'),
        ('Dm7add4/A', -5, -3, 'Am7add4/E chord'),
        ('G/G#', 1, 0, 'G\u266f/G\U0001D12A chord')])
def test_transpose(string, semitones, letter, notation):
    new_chord = CE.create_chord(string)
    new_chord.transpose(semitones, letter)
    assert repr(new_chord) == notation


def test_transpose_simple():
    new_chord = CE.create_chord("C#/G")
    new_chord.transpose_simple(1)
    assert "D" == new_chord.root
    assert "A\u266d" == new_chord.bass


def test_transpose_simple_flats():
    c = CE.create_chord("C/Gb")
    c.transpose_simple(1, use_flats=True)
    assert "D\u266d" == c.root
    assert "A\U0001D12B" == c.bass


@pytest.mark.parametrize(
    "input, output", [
        ("hey", "hey"), (None, '')
        ]
    )
def test_xstr(input, output):
    c = CE.create_chord('C')
    assert c._xstr(input) == output


def test_chord_equality():
    c = CE.create_chord('C')
    assert c == CE.create_chord('C')


def test_chord_not_implemented():
    c = CE.create_chord('C')
    assert c != len
