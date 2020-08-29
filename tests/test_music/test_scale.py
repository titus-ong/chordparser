import pytest

from chordparser.music.key import Key
from chordparser.music.note import Note
from chordparser.music.scale import Scale
from chordparser.music.scaledegree import ScaleDegree


class TestScale:
    def test_scale_creation_success(self):
        key = Key("C major")
        scale = Scale(key)
        assert key == scale.key

    def test_scale_argument_not_key(self):
        with pytest.raises(TypeError):
            Scale(len)


class TestScaleGetNotes:
    @pytest.mark.parametrize(
        "key, notes", [
            (Key("C major"), [
                Note("C"), Note("D"), Note("E"), Note("F"), Note("G"),
                Note("A"), Note("B"), Note("C"), Note("D"), Note("E"),
                Note("F"), Note("G"), Note("A"), Note("B"), Note("C"),
            ]),
            (Key("D dorian"), [
                Note("D"), Note("E"), Note("F"), Note("G"), Note("A"),
                Note("B"), Note("C"), Note("D"), Note("E"), Note("F"),
                Note("G"), Note("A"), Note("B"), Note("C"), Note("D"),
            ])
        ]
    )
    def test_correct_notes(self, key, notes):
        scale = Scale(key)
        assert notes == scale.get_notes()


class TestScaleGetScaleDegrees:
    @pytest.mark.parametrize(
        "key, sd", [
            (Key("C minor"), [
                ScaleDegree("1"), ScaleDegree("2"), ScaleDegree("b3"),
                ScaleDegree("4"), ScaleDegree("5"), ScaleDegree("b6"),
                ScaleDegree("b7"), ScaleDegree("1"), ScaleDegree("2"),
                ScaleDegree("b3"), ScaleDegree("4"), ScaleDegree("5"),
                ScaleDegree("b6"), ScaleDegree("b7"), ScaleDegree("1"),
             ])
        ]
    )
    def test_correct_scale_degrees(self, key, sd):
        scale = Scale(key)
        assert sd == scale.get_scale_degrees()


class TestScaleTranspose:
    def test_correct_transpose(self):
        scale = Scale(Key("C major"))
        scale.transpose(6, 3)
        assert "F\u266f major scale" == str(scale)


class TestScaleTransposeSimple:
    def test_correct_transpose(self):
        scale = Scale(Key("C major"))
        scale.transpose_simple(6)
        assert "F\u266f major scale" == str(scale)

    def test_correct_transpose_with_flats(self):
        scale = Scale(Key("C major"))
        scale.transpose_simple(8, use_flats=True)
        assert "A\u266d major scale" == str(scale)


class TestScaleGetNoteFromScaleDegree:
    @pytest.mark.parametrize(
        "key, sd, note", [
            (Key("C minor"), ScaleDegree("#3"), Note("E#")),
            (Key("Eb major"), ScaleDegree("2"), Note("F"))
        ]
    )
    def test_correct_note(self, key, sd, note):
        scale = Scale(key)
        assert note == scale.get_note_from_scale_degree(sd)


class TestScaleGetScaleDegreeFromNote:
    @pytest.mark.parametrize(
        "key, sd, note", [
            (Key("C minor"), ScaleDegree("#3"), Note("E#")),
            (Key("Eb major"), ScaleDegree("2"), Note("F"))
        ]
    )
    def test_correct_sd(self, key, sd, note):
        scale = Scale(key)
        assert sd == scale.get_scale_degree_from_note(note)


class TestScaleEquality:
    def test_scale_equal(self):
        key = Key("C major")
        scale = Scale(key)
        scale2 = Scale(key)
        assert scale == scale2

    def test_scale_not_equal_with_other_scales(self):
        scale = Scale(Key("C major"))
        scale2 = Scale(Key("C minor"))
        assert scale != scale2

    def test_scale_not_equal_with_other_types(self):
        assert len != Scale(Key("C major"))
