import pytest

from chordparser.music.quality import Quality


def test_check_major():
    with pytest.raises(ValueError):
        Quality("major", "seventh")


def test_check_diminished():
    with pytest.raises(ValueError):
        Quality("diminished", "seventh")


def test_check_diminished_2():
    with pytest.raises(ValueError):
        Quality("minor", "diminished seventh")


def test_check_flat_sevenths():
    with pytest.raises(ValueError):
        Quality("major", "major seventh", True)


@pytest.mark.parametrize(
    "quality, interval", [
        ("major", (4, 3)),
        ("sus2", (2, 5)),
    ]
)
def test_base_interval(quality, interval):
    q = Quality(quality)
    assert interval == q.base_intervals


@pytest.mark.parametrize(
    "quality, degree", [
        ("major", (1, 3, 5)),
        ("sus2", (1, 2, 5)),
    ]
)
def test_base_degree(quality, degree):
    q = Quality(quality)
    assert degree == q.base_degrees


@pytest.mark.parametrize(
    "quality, ext, interval", [
        ("dominant", "seventh", (4, 3, 3)),
        ("sus2", "major ninth", (2, 5, 4, 3)),
        ("diminished", "diminished seventh", (3, 3, 3)),
        ("half-diminished", "seventh", (3, 3, 4)),
    ]
)
def test_interval(quality, ext, interval):
    q = Quality(quality, ext)
    assert interval == q.intervals


@pytest.mark.parametrize(
    "quality, ext, degree", [
        ("major", "major ninth", (1, 3, 5, 7, 9)),
        ("sus2", "thirteenth", (1, 2, 5, 7, 9, 11, 13)),
    ]
)
def test_degree(quality, ext, degree):
    q = Quality(quality, ext)
    assert degree == q.degrees


@pytest.mark.parametrize(
    "quality, ext, sym", [
        ("dominant", "seventh", ("", "", "", "\u266d")),
        ("minor", "major ninth", ("", "\u266d", "", "", "")),
        ("diminished", "diminished seventh", ("", "\u266d", "\u266d", "\U0001D12B")),
        ("augmented", "seventh", ("", "", "\u266f", "\u266d")),
    ]
)
def test_sym(quality, ext, sym):
    q = Quality(quality, ext)
    assert sym == q.symbols


@pytest.mark.parametrize(
    "quality, ext, sym", [
        ("dominant", "seventh", ("", "", "")),
        ("power", None, ("", "")),
    ]
)
def test_sym_base(quality, ext, sym):
    q = Quality(quality, ext)
    assert sym == q.base_symbols


@pytest.mark.parametrize(
    "quality, name", [
        ("major", "major"),
        ("sus2", "sus2"),
    ]
)
def test_long_repr(quality, name):
    q = Quality(quality)
    assert name == str(q)


@pytest.mark.parametrize(
    "quality, ext, name", [
        ("dominant", "ninth", "dominant ninth"),
        ("major", "major seventh", "major seventh"),
        ("diminished", "diminished seventh", "diminished seventh"),
    ]
)
def test_long_repr_with_ext(quality, ext, name):
    q = Quality(quality, ext)
    assert name == str(q)


@pytest.mark.parametrize(
    "quality, ext, name", [
        ("dominant", "ninth", "dominant flat ninth"),
        ("major", "major eleventh", "major flat eleventh"),
    ]
)
def test_long_repr_with_flat_ext(quality, ext, name):
    q = Quality(quality, ext, True)
    assert name == str(q)


def test_short():
    q = Quality("diminished")
    assert "dim" == q.short()


def test_short_flat():
    q = Quality("minor", "ninth", True)
    assert "m\u266d9" == q.short()


def test_short_halfdim():
    q = Quality("half-diminished", "eleventh")
    assert "m11\u266d5" == q.short()


def test_short_sus():
    q = Quality("sus4", "seventh")
    assert "7sus" == q.short()


def test_equality_not_implemented():
    q = Quality("major")
    assert q != len


def test_equality():
    q1 = Quality("major", "major seventh")
    q2 = Quality("major", "major seventh")
    assert q1 == q2
