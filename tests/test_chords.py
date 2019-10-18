import chordparser.chords as chords
from chordparser.notes import Note
import pytest


@pytest.mark.parametrize(
    "value", [1, len, True, [], ()])
def test_chord_typeerror(value):
    with pytest.raises(TypeError):
        chords.Chord(value)


@pytest.mark.parametrize(
    "value", ["1", "H", "\u266fG"])
def test_chord_valueerror(value):
    with pytest.raises(ValueError):
        chords.Chord(value)


@pytest.mark.parametrize(
    "name, root", [
        ("C", "C"), ("C#Maj", "C\u266F"), ("DbM", "D\u266D"),
        ("D\u266Fmaj", "D\u266F"), ("D\u266DMa7", "D\u266D"),
        ("F##m", "F\U0001D12A"), ("Dbb", "D\U0001D12B"), ("F-", "F"),
        ("F\U0001D12Adim", "F\U0001D12A"), ("Do7", "D"),
        ("G\u00B011", "G"),
        ("B\U0001D12Baug", "B\U0001D12B"), ("G+11", "G"),
        ("C\u00f8", "C"), ("A\u00d8", "A"),
        ("G7", "G"), ("Edom7", "E"), ("Bdom", "B")])
def test_chord_root(name, root):
    new_chord = chords.Chord(name)
    assert new_chord.root == root


@pytest.mark.parametrize(
    "name, quality", [
        ("C", "major"), ("C#Maj", "major"), ("DbM", "major"),
        ("D\u266Fmaj", "major"), ("D\u266DMa7", "major"),
        ("F##m", "minor"), ("Dbb", "major"), ("F-", "minor"),
        ("F\U0001D12Adim", "diminished"), ("Do7", "diminished"),
        ("G\u00B011", "diminished"),
        ("B\U0001D12Baug", "augmented"), ("G+11", "augmented"),
        ("C\u00f8", "half-diminished"), ("A\u00d8", "half-diminished"),
        ("G7", "dominant"), ("Edom7", "dominant"), ("Bdom", "dominant")])
def test_chord_quality(name, quality):
    new_chord = chords.Chord(name)
    assert new_chord.quality == quality


@pytest.mark.parametrize(
    "name, triad", [
        ("C", (Note('C'), Note('E'), Note('G'))),
        ("D\u266Fmaj", (
            Note('D\u266F'),
            Note('F\U0001D12A'),
            Note('A\u266F'),
            )),
        ("Em", (Note('E'), Note('G'), Note('B'))),
        ("F\U0001D12Adim", (
            Note('F\U0001D12A'),
            Note('A\u266F'),
            Note('C\u266F'),
            )),
        ("Faug", (Note('F'), Note('A'), Note('C\u266F'))),
        ("C\u00f8", (Note('C'), Note('E\u266D'), Note('G\u266D'))),
        ("G7", (Note('G'), Note('B'), Note('D'))),
        ])
def test_chord_base_triad(name, triad):
    new_chord = chords.Chord(name)
    assert new_chord.base_triad == triad


@pytest.mark.parametrize(
    "name, quality", [
        ("C", ""),
        ("D\u266Fmaj7", "maj"),
        ("Em", "m"),
        ("F\U0001D12Adim", "dim"),
        ("Faug", "aug"),
        ("C\u00f8", "\u00d8"),
        ("G7", "dom"),
        ])
def test_chord_quality_short(name, quality):
    new_chord = chords.Chord(name)
    assert new_chord.quality_short == quality


@pytest.mark.parametrize(
    "name, chord", [
        ("C", "C chord"), ("C#7", "C\u266fdom7 chord"),
        ("DbM7", "D\u266dmaj7 chord"), ("D-add9", "Dmadd9 chord"),
        ("c#6/E", "C\u266fm6/E chord"),
        ])
def test_chord_name(name, chord):
    new_chord = chords.Chord(name)
    assert repr(new_chord) == chord


@pytest.mark.parametrize(
    "value", [
        "H#", 10.0, "Z", len])
def test_chord_transpose_error(value):
    new_chord = chords.Chord('C')
    with pytest.raises(TypeError):
        new_chord.transpose(value)


@pytest.mark.parametrize(
    "key, value, new_key", [
        ('C', 3, 'D\u266f'),
        ('Dm7add5/A', -5, 'A'),
        ('Gmaj', 12, 'G')])
def test_chord_root_transpose(key, value, new_key):
    new_chord = chords.Chord(key)
    new_chord.transpose(value)
    assert new_chord.root == new_key


@pytest.mark.parametrize(
    "key, value, new_key", [
        ('C/E', 3, 'G'),  # Fix this to be F##
        ('Dm7add5/A', -5, 'E')])
def test_chord_bass_transpose(key, value, new_key):
    new_chord = chords.Chord(key)
    new_chord.transpose(value)
    assert new_chord.bass_note == new_key