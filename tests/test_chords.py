import chordparser.chords as chords
from chordparser.notes import Note, Key
from chordparser.general import TransposeError
import pytest


@pytest.mark.parametrize(
    "name, chord", [
        (Note("C"), "C"), (Key("C#"), "C#"), ("DbM", "D\u266d"), ("Dmaj", "D"),
        ("D#Ma7", "D\u266fMa7"), ("Em", "Em"), ("f", "Fm"),
        ("F#-", "F\u266fm"), ("G7", "G7"),
        ("Abmin7", "A\u266dm7"), ("Bbbaug", "B\U0001D12Baug"),
        ("A##5", "A\U0001D12A5"), ("Bdim", "Bdim"), ("Cmin7dim5", "Cm7dim5")])
def test_chord_name(name, chord):
    new_chord = chords.Chord(name)
    assert new_chord.name == chord


@pytest.mark.parametrize(
    "name, note", [
        (Note("C"), "C"), (Key("C#"), "C\u266f"), ("DbM", "D\u266d"),
        ("Dmaj", "D"), ("D#Ma7", "D\u266f"), ("Em", "E"), ("f", "F"),
        ("F#-", "F\u266f"), ("G7", "G"),
        ("Abmin7", "A\u266d"), ("Bbbaug", "B\U0001D12B"),
        ("A##5", "A\U0001D12A"), ("Bdim", "B"), ("Cmin7dim5", "C")])
def test_chord_note(name, note):
    new_chord = chords.Chord(name)
    assert new_chord.key == note


# Only major and minor supported (not diminished/augmented)
@pytest.mark.parametrize(
    "name, quality", [
        (Note("C"), "major"), (Key("C#"), "major"), ("DbM", "major"),
        ("Dmaj", "major"), ("D#Ma7", "major"),
        ("Em", "minor"), ("f", "minor"), ("F#-", "minor"), ("G7", "major"),
        ("Abmin7", "minor"), ("Bbbaug", "major"), ("A##5", "major"),
        ("Bdim", "major"), ("Cmin7dim5", "minor")])
def test_chord_quality(name, quality):
    new_chord = chords.Chord(name)
    assert new_chord.quality == quality


@pytest.mark.parametrize(
    "name, other", [
        (Note("C"), ""), (Key("C#"), ""), ("DbM", ""), ("Dmaj", ""),
        ("D#Ma7", "7"), ("Em", ""), ("f", ""), ("F#-", ""), ("G7", "7"),
        ("Abmin7", "7"), ("Bbbaug", "aug"),
        ("A##5", "5"), ("Bdim", "dim"), ("Cmin7dim5", "7dim5")])
def test_chord_other(name, other):
    new_chord = chords.Chord(name)
    assert new_chord.other == other


@pytest.mark.parametrize(
    "name, major_minor", [
        (Note("C"), ""), (Key("C#"), ""), ("DbM", ""), ("Dmaj", ""),
        ("D#Ma7", "Ma"), ("Em", "m"), ("f", "m"), ("F#-", "m"), ("G7", ""),
        ("Abmin7", "m"), ("Bbbaug", ""),
        ("A##5", ""), ("Bdim", ""), ("Cmin7dim5", "m")])
def test_chord_major_minor(name, major_minor):
    new_chord = chords.Chord(name)
    assert new_chord.major_minor == major_minor


@pytest.mark.parametrize(
    "name, chord", [
        (Note("C"), "C chord"), (Key("C#"), "C\u266f chord"),
        ("DbM", "D\u266d chord"), ("Dmaj", "D chord"),
        ("D#Ma7", "D\u266fMa7 chord"), ("A##5", "A\U0001D12A5 chord"),
        ("Bdim", "Bdim chord"), ("Cmin7dim5", "Cm7dim5 chord")])
def test_chord_name(name, chord):
    new_chord = chords.Chord(name)
    assert repr(new_chord) == chord


@pytest.mark.parametrize(
    "name", [
        "H#", 10, "Z", len])
def test_chord_name(name):
    with pytest.raises(chords.ChordError):
        new_chord = chords.Chord(name)


@pytest.mark.parametrize(
    "value", [
        "H#", 10.0, "Z", len])
def test_chord_transpose_error(value):
    new_chord = chords.Chord('C')
    with pytest.raises(TransposeError):
        new_chord.transpose(value)


@pytest.mark.parametrize(
    "key, value, new_key", [
        ('C', 3, 'D\u266f'),
        ('Dm7add5', -5, 'Am7add5'),
        ('Gmaj', 12, 'G')])
def test_chord_transpose(key, value, new_key):
    new_chord = chords.Chord(key)
    new_chord.transpose(value)
    assert new_chord.name == new_key
