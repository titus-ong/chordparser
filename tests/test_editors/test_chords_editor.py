import pytest

from chordparser.editors.chords_editor import ChordEditor
from chordparser.editors.keys_editor import KeyEditor
from chordparser.editors.notes_editor import NoteEditor
from chordparser.editors.scales_editor import ScaleEditor
from chordparser.music.notes import Note


NE = NoteEditor()
KE = KeyEditor()
SE = ScaleEditor()
CE = ChordEditor()


@pytest.mark.parametrize(
    "value", ["1", "H", "\u266fG"])
def test_chord_value_error(value):
    with pytest.raises(SyntaxError):
        CE.create_chord(value)


@pytest.mark.parametrize(
    "value", ['C', 'E\u266f']
)
def test_chord_root(value):
    new_chord = CE._parse_root(value)
    assert new_chord == value
    assert isinstance(new_chord, Note)


def test_quality():
    c = CE._parse_quality("minmaj7")
    assert "minor major seventh" == repr(c)


def test_quality_capital():
    c = CE.create_chord("c7")
    assert "minor seventh" == repr(c.quality)


@pytest.mark.parametrize(
    "string, add", [
        ('add13', [('', 13)]),
        ('add2#6', [('', 2), ('\u266f', 6)]),
        ('b11', [('\u266d', 11)]),
        (None, None),
    ]
)
def test_add(string, add):
    c = CE._parse_add(string)
    assert c == add


def test_add_parse_error():
    with pytest.raises(SyntaxError):
        c = CE._parse_add('add21')


@pytest.mark.parametrize(
    "string, bass", [
        ('G', 'G'),
        ('G#', 'G\u266f'),
    ]
)
def test_bass(string, bass):
    c = CE._parse_bass(string)
    assert c == bass
    assert isinstance(c, Note)


def test_bass_2():
    c = CE._parse_bass(None)
    assert None is c


def test_create_chord_everything():
    c = CE.create_chord("C#dim7addb4/E")
    assert "C\u266f" == c.root
    assert "diminished seventh" == repr(c.quality)
    assert [("\u266d", 4)] == c.add
    assert "E" == c.bass


@pytest.mark.parametrize(
    "degree, quality", [
        (7, 'diminished'),
        (4, 'major'),
        (6, 'minor'),
    ]
)
def test_diatonic(degree, quality):
    s = SE.create_scale('C', 'major')
    c = CE.create_diatonic(s, degree)
    assert repr(c.quality) == quality


@pytest.mark.parametrize(
    "degree, quality", [
        (7, 'diminished'),
        (4, 'major'),
        (6, 'minor'),
    ]
)
def test_diatonic_2(degree, quality):
    s = KE.create_key('C', 'major')
    c = CE.create_diatonic(s, degree)
    assert repr(c.quality) == quality


@pytest.mark.parametrize("degree", [0, len])
def test_diatonic_value_error(degree):
    s = SE.create_scale('C', 'major')
    with pytest.raises(ValueError):
        c = CE.create_diatonic(s, degree)


def test_change_chord_root():
    o = CE.create_chord('C')
    n = CE.create_chord('D')
    assert n == CE.change_chord(o, root='D')


def test_change_chord_q():
    o = CE.create_chord('C')
    n = CE.create_chord('Cminmajb9')
    assert n == CE.change_chord(o, quality="minmajb9")


def test_change_chord_add():
    o = CE.create_chord('Cadd9')
    n = CE.create_chord('Caddb2add9')
    assert n == CE.change_chord(o, add='b2')


def test_change_chord_rem():
    o = CE.create_chord('Caddb2')
    n = CE.create_chord('C')
    assert n == CE.change_chord(o, remove='b2')


def test_change_chord_rem_2():
    o = CE.create_chord('Caddb2add6add9')
    n = CE.create_chord('C')
    assert n == CE.change_chord(o, remove=True)
    assert None is o.add


def test_change_chord_rem_error():
    o = CE.create_chord('C')
    with pytest.raises(IndexError):
        CE.change_chord(o, remove='b2')


def test_change_chord_rem_error_2():
    o = CE.create_chord('Cb2')
    with pytest.raises(ValueError):
        CE.change_chord(o, remove='b22')


def test_change_chord_bass():
    o = CE.create_chord('Cadd9')
    n = CE.create_chord('Cadd9/G')
    assert n == CE.change_chord(o, bass='G')


def test_change_chord_bass_2():
    o = CE.create_chord('Cadd9/G')
    n = CE.create_chord('Cadd9')
    assert n == CE.change_chord(o, bass=False)
    assert None is o.bass


def test_change_chord_not_inplace():
    o = CE.create_chord("Csus4add9/G")
    n = CE.change_chord(o, bass='G', inplace=False)
    assert n == o
    assert n is not o
