import pytest

from chordparser.editors.keys_editor import KeyEditor


KE = KeyEditor()


def test_key_note_attribute():
    nkey = KE.create_key('C')
    nkey.transpose(2, 1)
    assert nkey.root == 'D'


@pytest.mark.parametrize(
    "root, mode, submode", [
        ('C', 'dorian', None),
        ('C', 'aeolian', 'harmonic'),
    ]
)
def test_key_representation(root, mode, submode):
    nkey = KE.create_key(root, mode, submode)
    if submode:
        assert repr(nkey) == f'{root} {submode} {mode}'
    else:
        assert repr(nkey) == f'{root} {mode}'


def test_key_not_implemented():
    nkey = KE.create_key('C')
    assert nkey != len


def test_key_attribute_error():
    nkey = KE.create_key('C')
    with pytest.raises(AttributeError):
        nkey.testing()


@pytest.mark.parametrize(
    "root, mode, submode", [
        ('C', 'major', None),
        ('C', 'ionian', None),
    ]
)
def test_key_equality(root, mode, submode):
    nkey = KE.create_key('C')
    assert nkey == KE.create_key(root, mode, submode)


def test_key_equality_2():
    nkey = KE.create_key('C', 'dorian')
    assert nkey == KE.create_key('C', 'dorian')


@pytest.mark.parametrize(
    "root, mode, submode", [
        ('C', 'major', None),
        ('C', 'minor', 'harmonic'),
    ]
)
def test_key_inequality(root, mode, submode):
    nkey = KE.create_key('C', 'aeolian', 'natural')
    assert nkey != KE.create_key(root, mode, submode)
