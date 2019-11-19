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
        ("D\u266Fmaj", "major"), ("D\u266DMa7", "major7"),
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
    "name, chord", [
        ("C", (Note('C'), Note('E'), Note('G'))),
        ("D\u266Fmaj", (
            Note('D\u266F'),
            Note('F\U0001D12A'),
            Note('A\u266F'),
            )),
        ("Em", (Note('E'), Note('G'), Note('B'))),
        ("Fdim", (
            Note('F'),
            Note('A\u266D'),
            Note('C\u266D'),
            Note('E\U0001D12B'),
            )),
        ("Faug", (Note('F'), Note('A'), Note('C\u266F'))),
        ("C\u00f8", (Note('C'), Note('E\u266D'), Note('G\u266D'), Note('B\u266D'))),
        ("G7", (Note('G'), Note('B'), Note('D'), Note('F'))),
        ("Amaj7", (Note('A'), Note('C\u266F'), Note('E'), Note('G\u266F'))),
        ])
def test_chord_base_chord(name, chord):
    new_chord = chords.Chord(name)
    assert new_chord.base_chord == chord


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
        ("C5", (
            Note('C'), Note('G'),
            )),
        ("Em5", (
            Note('E'), Note('B'),
            )),
        ])
def test_chord_power_chord(name, chord):
    new_chord = chords.Chord(name)
    assert new_chord.notes == chord


@pytest.mark.parametrize(
    "name, chord", [
        ("C13", (
            Note('C'), Note('E'), Note('G'), Note('Bb'),
            Note('D'), Note('F'), Note('A'),
            )),
        ("Em11", (
            Note('E'), Note('G'), Note('B'),
            Note('D'), Note('F#'), Note('A'),
            )),
        ("F9", (
            Note('F'), Note('A'), Note('C'),
            Note('E\u266D'), Note('G'),
            )),
        ])
def test_chord_ext_chord(name, chord):
    new_chord = chords.Chord(name)
    assert new_chord.notes == chord


@pytest.mark.parametrize(
    "name, chord", [
        ("CMb5", (
            Note('C'), Note('E'), Note('Gb'),
            )),
        ("Em#5", (
            Note('E'), Note('G'), Note('B#'),
            )),
        ("F7bb5", (
            Note('F'), Note('A'), Note('Cbb'),
            Note('E\u266D'),
            )),
        ("Gmaj7##5", (
            Note('G'), Note('B'), Note('D##'),
            Note('F\u266F'),
            )),
        ])
def test_chord_alt5_chord(name, chord):
    new_chord = chords.Chord(name)
    assert new_chord.notes == chord


@pytest.mark.parametrize(
    "name, chord", [
        ("Cadd13", (
            Note('C'), Note('E'), Note('G'), Note('A'),
            )),
        ("Emadd2add4add9", (
            Note('E'), Note('F#'), Note('G'), Note('A'), Note('B'), Note('F#'),
            )),
        ])
def test_chord_add_chord(name, chord):
    new_chord = chords.Chord(name)
    assert new_chord.notes == chord


@pytest.mark.parametrize(
    "name, chord", [
        ("CMsus2", (
            Note('C'), Note('D'), Note('G'),
            )),
        ("Emsus4", (
            Note('E'), Note('A'), Note('B'),
            )),
        ])
def test_chord_sus_chord(name, chord):
    new_chord = chords.Chord(name)
    assert new_chord.notes == chord


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
        ('Dm7add4/A', -5, 'A'),
        ('Gmaj', 12, 'G')])
def test_chord_root_transpose(key, value, new_key):
    new_chord = chords.Chord(key)
    new_chord.transpose(value)
    assert new_chord.root == new_key


@pytest.mark.parametrize(
    "key, value, new_key", [
        ('C/E', 3, 'F\U0001D12A'),
        ('Dm7add4/A', -5, 'E')])
def test_chord_bass_transpose(key, value, new_key):
    new_chord = chords.Chord(key)
    new_chord.transpose(value)
    assert new_chord.bass_note == new_key
