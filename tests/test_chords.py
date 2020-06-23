from chordparser.chords import Chord
from chordparser import chords_editor
from chordparser import scales_editor
from chordparser import keys_editor
from chordparser import notes_editor
import pytest


NE = notes_editor.NoteEditor()
KE = keys_editor.KeyEditor()
SE = scales_editor.ScaleEditor()
CE = chords_editor.ChordEditor()


@pytest.mark.parametrize(
    "name, quality, chord", [
        ("C", 'major', (NE.create_note('C'), NE.create_note('E'), NE.create_note('G'))),
        ("C", 'diminished', (NE.create_note('C'), NE.create_note('Eb'), NE.create_note('Gb'))),
        ])
def test_base_triad(name, quality, chord):
    c = Chord(name, quality)
    assert c.base_triad == chord


@pytest.mark.parametrize(
    "name, quality, q", [
        ("C", 'major seventh', [NE.create_note('C'), NE.create_note('E'), NE.create_note('G'), NE.create_note('B')]),
        ("C", 'diminished ninth', [NE.create_note('C'), NE.create_note('Eb'), NE.create_note('Gb'), NE.create_note('Bbb'), NE.create_note('D')]),
        ("C", 'augmented-major minor eleventh', [NE.create_note('C'), NE.create_note('E'), NE.create_note('G#'), NE.create_note('B'), NE.create_note('D'), NE.create_note('Fb')]),
        ])
def test_base_notes(name, quality, q):
    c = Chord(name, quality)
    assert c.notes == q


@pytest.mark.parametrize(
    "name, quality, q", [
        ("C", 'major seventh', ([[None, 1], [None, 3], [None, 5], [None, 7]])),
        ("C", 'diminished ninth', ([[None, 1], [None, 3], [None, 5], [None, 7], [None, 9]])),
        ("C", 'augmented-major minor eleventh', ([[None, 1], [None, 3], [None, 5], [None, 7], [None, 9], ['\u266D', 11]])),
        ])
def test_base_tones(name, quality, q):
    c = Chord(name, quality)
    assert c.tones == q


@pytest.mark.parametrize(
    "name, quality, sus, q", [
        ("C", 'major seventh', 2, [NE.create_note('C'), NE.create_note('D'), NE.create_note('G'), NE.create_note('B')]),
        ("C", 'diminished ninth', 4, [NE.create_note('C'), NE.create_note('F'), NE.create_note('Gb'), NE.create_note('Bbb'), NE.create_note('D')]),
        ])
def test_sus_notes(name, quality, sus, q):
    c = Chord(name, quality, sus=sus)
    assert c.notes == q


@pytest.mark.parametrize(
    "name, quality, sus, q", [
        ("C", 'major seventh', 2, ([[None, 1], [None, 2], [None, 5], [None, 7]])),
        ("C", 'diminished ninth', 4, ([[None, 1], [None, 4], [None, 5], [None, 7], [None, 9]])),
        ])
def test_sus_tones(name, quality, sus, q):
    c = Chord(name, quality, sus=sus)
    assert c.tones == q


@pytest.mark.parametrize(
    "name, quality, add, q", [
        ("C", 'major seventh', ['2', '\u266D11'], [NE.create_note('C'), NE.create_note('D'), NE.create_note('E'), NE.create_note('G'), NE.create_note('B'), NE.create_note('F\u266D')]),
        ("C", 'diminished', ['11'], [NE.create_note('C'), NE.create_note('Eb'), NE.create_note('Gb'), NE.create_note('F')]),
        ])
def test_add_notes(name, quality, add, q):
    c = Chord(name, quality, add=add)
    assert c.notes == q


@pytest.mark.parametrize(
    "name, quality, add, q", [
        ("C", 'major seventh', ['2', '\u266D11'],  ([[None, 1], [None, 2], [None, 3], [None, 5], [None, 7], ['\u266D', 11]])),
        ("C", 'diminished', ['11'], ([[None, 1], [None, 3], [None, 5], [None, 11]])),
        ])
def test_add_tones(name, quality, add, q):
    c = Chord(name, quality, add=add)
    assert c.tones == q


@pytest.mark.parametrize(
    "name, quality, bass, q", [
        ("C", 'major seventh', NE.create_note('G'), [NE.create_note('G'), NE.create_note('C'), NE.create_note('E'), NE.create_note('B')]),
        ("C", 'diminished', NE.create_note('G#'), [NE.create_note('G#'), NE.create_note('C'), NE.create_note('Eb'), NE.create_note('Gb')]),
        ])
def test_bass_notes(name, quality, bass, q):
    c = Chord(name, quality, bass=bass)
    assert c.notes == q


@pytest.mark.parametrize(
    "name, quality, bass, q", [
        ("C", 'major seventh', NE.create_note('G'),  ([[None, 5], [None, 1], [None, 3], [None, 7]])),
        ("C", 'diminished', NE.create_note('G#'), ([['\u266F', 5], [None, 1], [None, 3], [None, 5]])),
        ])
def test_bass_tones(name, quality, bass, q):
    c = Chord(name, quality, bass=bass)
    assert c.tones == q


@pytest.mark.parametrize(
    "string, notation", [
        ("Cmajsus2add9/G", "Csus2add9/G chord"),
        ("Cminmaj9susadd#9#13/G#", "Cminmaj9sus4\u266F9\u266F13/G\u266F chord"),
        ("Caugmaj11", "Cmaj11\u266F5 chord"),
        ]
    )
def test_notation(string, notation):
    c = CE.create_chord(string)
    assert repr(c) == notation


@pytest.mark.parametrize(
    "string, value, notation", [
        ('C', 3, 'D\u266f chord'),
        ('Dm7add4/A', -5, 'Am7add4/E chord'),
        ('G/G#', 1, 'G\u266f/G\U0001D12A chord')])
def test_transpose(string, value, notation):
    new_chord = CE.create_chord(string)
    new_chord.transpose(value)
    assert repr(new_chord) == notation


def test_transpose_type_error():
    c = CE.create_chord('C')
    with pytest.raises(TypeError):
        c.transpose(1.5)


def test_transpose_type_error_2():
    c = CE.create_chord('C')
    with pytest.raises(TypeError):
        c.transpose(1, None)


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
