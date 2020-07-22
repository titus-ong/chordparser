import pytest

from chordparser.editors.chords_editor import ChordEditor
from chordparser.editors.keys_editor import KeyEditor
from chordparser.editors.notes_editor import NoteEditor
from chordparser.editors.scales_editor import ScaleEditor


NE = NoteEditor()
KE = KeyEditor()
SE = ScaleEditor()
CE = ChordEditor()


@pytest.mark.parametrize(
    "value", ["1", "H", "\u266fG"])
def test_chord_valueerror(value):
    with pytest.raises(SyntaxError):
        CE.create_chord(value)


@pytest.mark.parametrize(
    "value, root", [
        ('C', NE.create_note('C')),
        ('E\u266f', NE.create_note('E\u266f')),
    ]
)
def test_chord_root(value, root):
    new_chord = CE.create_chord(value)
    assert new_chord.root == root


def test_quality():
    c = CE.create_chord("Cminmaj7")
    assert "minor major seventh" == str(c.quality)


@pytest.mark.parametrize(
    "string, add", [
        ('Cadd13', [('', 13)]),
        ('cadd2#6', [('', 2), ('\u266f', 6)]),
        ('cminmaj9b11', [('\u266d', 11)]),
        ('C', None),
    ]
)
def test_add(string, add):
    c = CE.create_chord(string)
    assert c.add == add


def test_add_2():
    c = CE.create_chord("C")
    assert c.add is None


def test_parse_error():
    with pytest.raises(SyntaxError):
        c = CE.create_chord('Cadd21')


@pytest.mark.parametrize(
    "string, bass", [
        ('C', None),
        ('C/G', NE.create_note('G')),
        ('C/G#', NE.create_note('G\u266f')),
    ]
)
def test_bass(string, bass):
    c = CE.create_chord(string)
    assert c.bass == bass


def test_bass_2():
    c = CE.create_chord("C")
    assert None is c.bass


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
    assert str(c.quality) == quality


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
    assert str(c.quality) == quality


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
