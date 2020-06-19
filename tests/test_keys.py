from chordparser import keys
from chordparser import keys_editor
import pytest


KE = keys_editor.KeyEditor()


@pytest.mark.parametrize(
    "key, value, new_key", [
        ('C', 2, 'D'), ('G\u266d', -5, 'C\u266f'), ('A\U0001D12A', 1, 'C')])
def test_key_transpose_sharps(key, value, new_key):
    nkey = KE.create_key(key)
    nkey.transpose(value)
    assert nkey.root == new_key


@pytest.mark.parametrize(
    "key, value, new_key", [
        ('C', -2, 'B\u266d'), ('F\u266f', -5, 'D\u266d'), ('F', -2, 'E\u266d')])
def test_key_transpose_flat(key, value, new_key):
    nkey = KE.create_key(key)
    nkey.transpose(value, use_flats=True)
    assert nkey.root == new_key


@pytest.mark.parametrize(
    "value", [
        "H#", 10.0, "Z", len])
def test_key_transpose_error(value):
    nkey = KE.create_key('C')
    with pytest.raises(TypeError):
        nkey.transpose(value)


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
