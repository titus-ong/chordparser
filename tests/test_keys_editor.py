from chordparser import keys_editor
import pytest


KE = keys_editor.KeyEditor()


@pytest.mark.parametrize(
    "key", [1, True, len, [], ()])
def test_keys_typeerror(key):
    with pytest.raises(TypeError):
        nkey = KE.create_key(key)


@pytest.mark.parametrize(
    "key", ["ABC", "G\u266f\u266f", "H"])
def test_keys_valueerror(key):
    with pytest.raises(ValueError):
        nkey = KE.create_key(key)


@pytest.mark.parametrize(
    "mode, submode", [
        ("major", None), ("mInoR", None), ("MINOR", "harmonic"),
        ("minor", "melodic"), ("minor", "natural"), ("ionian", None),
        ("dorian", None), ("phrygian", None), ("lydian", None),
        ("mixolydian", None), ("aeolian", None), ("locrian", None)])
def test_key_mode_submode(mode, submode):
    nkey = KE.create_key('C', mode=mode, submode=submode)
    if not submode:
        assert str(nkey) == f'C {mode.lower()}'
    else:
        assert str(nkey) == f'C {submode.lower()} {mode.lower()}'


@pytest.mark.parametrize(
    "mode", [1, True, len])
def test_key_mode_typeerror(mode):
    with pytest.raises(TypeError):
        nkey = KE.create_key('C', mode)


@pytest.mark.parametrize(
    "mode", ["ionia", "hello", "1rh9"])
def test_key_mode_error(mode):
    with pytest.raises(KeyError):
        nkey = KE.create_key('C', mode)


@pytest.mark.parametrize(
    "mode, submode", [("major", "harmonic"), ("minor", "nothing")])
def test_key_submode_key_error(mode, submode):
    with pytest.raises(KeyError):
        nkey = KE.create_key('C', mode, submode)


@pytest.mark.parametrize(
    "mode, submode", [("major", 1), ("minor", True)])
def test_key_submode_type_error(mode, submode):
    with pytest.raises(TypeError):
        nkey = KE.create_key('C', mode, submode)


@pytest.mark.parametrize(
    "root, mode, newroot, newmode", [
        ('C', 'minor', 'E\u266d', 'major'),
        ('F', 'aeolian', 'A\u266d', 'major'),
        ]
    )
def test_relative_major(root, mode, newroot, newmode):
    nkey = KE.create_key(root, mode)
    rel_key = KE.relative_major(nkey)
    assert rel_key == KE.create_key(newroot, newmode)


def test_relative_major_incorrect_mode():
    nkey = KE.create_key('C', 'dorian')
    with pytest.raises(KeyError):
        KE.relative_major(nkey)


def test_relative_minor_incorrect_mode():
    nkey = KE.create_key('C', 'dorian')
    with pytest.raises(KeyError):
        KE.relative_minor(nkey)


def test_relative_minor_incorrect_submode():
    nkey = KE.create_key('C', 'major')
    with pytest.raises(KeyError):
        KE.relative_minor(nkey, 'blah')


@pytest.mark.parametrize(
    "root, mode, submode, newroot, newmode, newsub", [
        ('A', 'major', 'harmonic', 'F\u266f', 'minor', 'harmonic'),
        ('F\u266d', 'ionian', 'natural', 'D\u266d', 'minor', 'natural'),
        ]
    )
def test_relative_minor(root, mode, submode, newroot, newmode, newsub):
    nkey = KE.create_key(root, mode)
    rel_key = KE.relative_minor(nkey, submode)
    assert rel_key == KE.create_key(newroot, newmode, newsub)
