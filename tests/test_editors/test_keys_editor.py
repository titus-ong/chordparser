import pytest

from chordparser.editors.keys_editor import KeyEditor, ModeError
from chordparser.editors.notes_editor import NoteEditor
from chordparser.music.notes import Note


KE = KeyEditor()
NE = NoteEditor()


def test_check_root():
    note = NE.create_note("C")
    assert isinstance(KE._check_root(note), Note)


def test_check_root_2():
    note = "C"
    assert isinstance(KE._check_root(note), Note)


@pytest.mark.parametrize(
    "mode", ["major", "MINOR", "dOrIaN"]
)
def test_check_mode(mode):
    assert KE._check_mode(mode) == mode.lower()


@pytest.mark.parametrize(
    "mode", ["ionia", "hello", "1rh9"])
def test_check_mode_error(mode):
    with pytest.raises(SyntaxError):
        KE._check_mode(mode)


@pytest.mark.parametrize(
    "mode, submode", [
        ("major", None), ("minor", "harmonic"), ("locrian", None)])
def test_check_submode(mode, submode):
    assert KE._check_submode(mode, submode) == submode


def test_check_submode_2():
    assert KE._check_submode("minor", None) == 'natural'


def test_check_submode_3():
    assert KE._check_submode("minor", "Harmonic") == "harmonic"


def test_check_submode_syntax_error():
    with pytest.raises(SyntaxError):
        KE._check_submode("minor", "nothing")


def test_check_submode_mode_error():
    with pytest.raises(ModeError):
        KE._check_submode("major", "harmonic")


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


def test_relative_minor_incorrect_mode():
    nkey = KE.create_key('C', 'dorian')
    with pytest.raises(ModeError):
        KE.relative_minor(nkey)


def test_relative_minor_incorrect_submode():
    nkey = KE.create_key('C', 'major')
    with pytest.raises(SyntaxError):
        KE.relative_minor(nkey, 'blah')


def test_change_key():
    okey = KE.create_key('C', 'major', None)
    nkey = KE.create_key('D', 'minor', 'harmonic')
    assert nkey == KE.change_key(okey, 'D', 'minor', 'harmonic')


def test_change_key_2():
    okey = KE.create_key('C', 'minor', 'melodic')
    nkey = KE.create_key('D\u266d', 'minor', 'melodic')
    assert nkey == KE.change_key(okey, 'D\u266d', 'minor', None)


def test_change_key_not_inplace():
    okey = KE.create_key("C")
    nkey = KE.change_key(okey, root="C", inplace=False)
    assert nkey is not okey
