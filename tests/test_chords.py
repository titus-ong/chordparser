import chordparser.chords as chords
import pytest


@pytest.mark.parametrize(
    "name, chord", [
        ("C", "C"), ("DbM", "DbM"), ("Dmaj", "Dmaj"), ("D#Ma7", "D#Ma7"),
        ("Em", "Em"), ("f", "f"), ("F#-", "F#-"), ("G7", "G7"),
        ("Abmin7", "Abmin7"), ("Bbbaug", "Bbbaug"), ("A##5", "A##5"),
        ("Bdim", "Bdim"), ("Cmin7dim5", "Cmin7dim5")])
def test_chord_name(name, chord):
    new_chord = chords.Chord(name)
    assert new_chord.name == chord


@pytest.mark.parametrize(
    "name, note", [
        ("C", "C"), ("DbM", "D\u266d"), ("Dmaj", "D"), ("D#Ma7", "D\u266f"),
        ("Em", "E"), ("f", "F"), ("F#-", "F\u266f"), ("G7", "G"),
        ("Abmin7", "A\u266d"), ("Bbbaug", "B\U0001D12B"),
        ("A##5", "A\U0001D12A"), ("Bdim", "B"), ("Cmin7dim5", "C")])
def test_chord_note(name, note):
    new_chord = chords.Chord(name)
    assert new_chord.note.value == note


# Only major and minor supported (not diminished/augmented)
@pytest.mark.parametrize(
    "name, quality", [
        ("C", "major"), ("DbM", "major"), ("Dmaj", "major"), ("D#Ma7", "major"),
        ("Em", "minor"), ("f", "minor"), ("F#-", "minor"), ("G7", "major"),
        ("Abmin7", "minor"), ("Bbbaug", "major"), ("A##5", "major"),
        ("Bdim", "major"), ("Cmin7dim5", "minor")])
def test_chord_quality(name, quality):
    new_chord = chords.Chord(name)
    assert new_chord.quality == quality
