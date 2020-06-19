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


@pytest.mark.parametrize(
    "key", [1, True, len])
def test_scale_keys_typeerror(key):
    with pytest.raises(TypeError):
        SE.create_scale(key)
