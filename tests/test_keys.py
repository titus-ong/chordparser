from chordparser import keys_editor
import pytest


KE = keys_editor.KeyEditor()


@pytest.mark.parametrize(
    "key, semitone, letter, new_key", [
        ('C', 2, 1, 'D'), ('G\u266d', -5, -4, 'C\u266f'), ('A\U0001D12A', 1, 2, 'C')])
def test_note_transpose(key, semitone, letter, new_key):
    nkey = KE.create_key(key)
    nkey.transpose(semitone, letter)
    assert nkey.root == new_key


@pytest.mark.parametrize(
    "value", [
        "H#", "Z", len])
def test_root_transpose_error(value):
    nkey = KE.create_key('C')
    with pytest.raises(TypeError):
        nkey.transpose(value, 1)


@pytest.mark.parametrize(
    "value", [
        "H#", 10.0, "Z", len])
def test_root_transpose_error_2(value):
    nkey = KE.create_key('C')
    with pytest.raises(TypeError):
        nkey.transpose(1, value)


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
