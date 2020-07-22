from chordparser.quality_editor import QualityEditor
import pytest


QE = QualityEditor()


def test_power():
    q = QE.create_quality("5")
    assert "power" == q.value


def test_sus():
    q = QE.create_quality("sus")
    assert "sus4" == q.value


def test_sus_2():
    q = QE.create_quality("sus2")
    assert "sus2" == q.value


def test_triad():
    q = QE.create_quality("aug")
    assert "augmented" == q.value


def test_alt5():
    q = QE.create_quality("mb5")
    assert "diminished" == q.value


def test_alt5_2():
    q = QE.create_quality("7#5")
    assert "augmented" == q.value


@pytest.mark.parametrize(
    "quality, value", [
        ("7", "dominant"),
        ("m9", "minor"),
        ("augmaj7", "augmented"),
        ("maj7#5", "augmented"),
        ("m7b5", "half-diminished"),
    ]
)
def test_base_ext(quality, value):
    q = QE.create_quality(quality)
    assert value == q.value


@pytest.mark.parametrize(
    "quality, value", [
        ("7", "seventh"),
        ("m9", "ninth"),
        ("augmaj7", "major seventh"),
        ("dim7", "diminished seventh"),
        ("dim", None),
    ]
)
def test_base_ext(quality, value):
    q = QE.create_quality(quality)
    assert value == q.ext


def test_flat_ext():
    q = QE.create_quality("majb9")
    assert True is q.flat_ext


def test_capital():
    q = QE.create_quality("7", False)
    assert "minor" == q.value


def test_capital_2():
    q = QE.create_quality("", False)
    assert "minor" == q.value


def test_empty():
    q = QE.create_quality("+")
    assert "augmented" == q.value


def test_empty_2():
    q = QE.create_quality("")
    assert "major" == q.value


def test_none():
    q = QE.create_quality(None)
    assert "major" == q.value


def test_none_2():
    q = QE.create_quality(None, False)
    assert "minor" == q.value
