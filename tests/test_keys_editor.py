from chordparser.keys_editor import KeyEditor, ModeError
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
        ("major", None), ("MINOR", "harmonic"),
        ("minor", "melodic"), ("minor", "natural"), ("ionian", None),
        ("dorian", None), ("phrygian", None), ("lydian", None),
        ("mixolydian", None), ("locrian", None)])
def test_key_mode_submode(mode, submode):
    nkey = KE.create_key('C', mode=mode, submode=submode)
    if not nkey.submode:
        assert str(nkey) == f'C {mode.lower()}'
    else:
        assert str(nkey) == f'C {submode.lower()} {mode.lower()}'


def test_key_mode_submode_2():
    nkey = KE.create_key('C', 'minor')
    assert nkey.submode == 'natural'


@pytest.mark.parametrize(
    "mode", [1, True, len])
def test_key_mode_typeerror(mode):
    with pytest.raises(TypeError):
        nkey = KE.create_key('C', mode)


@pytest.mark.parametrize(
    "mode", ["ionia", "hello", "1rh9"])
def test_key_mode_error(mode):
    with pytest.raises(ValueError):
        nkey = KE.create_key('C', mode)


@pytest.mark.parametrize(
    "mode, submode", [("minor", "nothing")])
def test_key_submode_key_error(mode, submode):
    with pytest.raises(ValueError):
        nkey = KE.create_key('C', mode, submode)


@pytest.mark.parametrize(
    "mode, submode", [("major", 1), ("minor", True)])
def test_key_submode_type_error(mode, submode):
    with pytest.raises(TypeError):
    "mode, submode", [("major", "harmonic")])
def test_key_submode_key_error_2(mode, submode):
    with pytest.raises(ModeError):
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
    with pytest.raises(ModeError):
        KE.relative_major(nkey)


def test_relative_minor_incorrect_mode():
    nkey = KE.create_key('C', 'dorian')
    with pytest.raises(ModeError):
        KE.relative_minor(nkey)


def test_relative_minor_incorrect_submode():
    nkey = KE.create_key('C', 'major')
    with pytest.raises(ValueError):
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


def test_change_key():
    okey = KE.create_key('C', 'major', None)
    nkey = KE.create_key('D', 'minor', 'harmonic')
    assert nkey == KE.change_key(okey, 'D', 'minor', 'harmonic')


def test_change_key_2():
    okey = KE.create_key('C', 'minor', 'melodic')
    nkey = KE.create_key('D\u266d', 'minor', 'melodic')
    assert nkey == KE.change_key(okey, 'D\u266d', 'minor', None)

def test_change_key_error():
    with pytest.raises(TypeError):
        KE.change_key(len)
