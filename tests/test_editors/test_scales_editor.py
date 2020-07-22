from chordparser import keys_editor
from chordparser import scales_editor
import pytest


KE = keys_editor.KeyEditor()
SE = scales_editor.ScaleEditor()


@pytest.mark.parametrize(
    "key", ["A", "C\u266f", "D\u266d", "B\U0001D12B", "F\U0001D12A"])
def test_scale_keys(key):
    nkey = KE.create_key(key)
    new_scale = SE.create_scale(nkey)
    assert new_scale.key == KE.create_key(key)


@pytest.mark.parametrize(
    "root, mode, submode", [('C', 'phrygian', None)]
)
def test_scale_key_args(root, mode, submode):
    new_scale = SE.create_scale(root, mode, submode)
    assert new_scale.key == KE.create_key(root, mode, submode)


def test_change_scale():
    o = SE.create_scale('C', 'major', None)
    n = SE.create_scale('D', 'minor', 'harmonic')
    assert n == SE.change_scale(o, 'D', 'minor', 'harmonic')


def test_change_scale_2():
    o = SE.create_scale('C', 'minor', 'melodic')
    n = SE.create_scale('D\u266d', 'minor', 'melodic')
    assert n == SE.change_scale(o, 'D\u266d', 'minor', None)


def test_change_scale_not_inplace():
    o = SE.create_scale("C")
    n = SE.change_scale(o, root="C", inplace=False)
    assert n is not o
