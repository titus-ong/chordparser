import pytest

from chordparser.music.key import (ModeError, Mode, Submode,
                                   ModeGroupNotationParser,
                                   KeyNotationParser, ModeGroup, Key)
from chordparser.music.note import Note
from chordparser.utils.unicode_chars import (sharp, doublesharp,
                                             flat, doubleflat)


class TestMNPParseNotation:
    @pytest.fixture
    def parser(self):
        return ModeGroupNotationParser()

    @pytest.mark.parametrize(
        "notation, expected_mode", [
            ("", "major"),
            ("m", "minor"),
            (" major", "major"),
            (" Dorian", "dorian"),
        ]
    )
    def test_correct_mode(self, parser, notation, expected_mode):
        mode, _ = parser.parse_notation(notation)
        assert expected_mode == mode

    @pytest.mark.parametrize(
        "notation, expected_submode", [
            (" minor", "natural"),
            ("harmonic minor", "harmonic"),
            (" major", "none"),
        ]
    )
    def test_correct_submode(self, parser, notation, expected_submode):
        _, submode = parser.parse_notation(notation)
        assert expected_submode == submode

    def test_mode_error(self, parser):
        with pytest.raises(ModeError):
            parser.parse_notation("natural major")


class TestModeStepPattern:
    @pytest.mark.parametrize(
        "mode, steps", [
            ("major", (
                2, 2, 1, 2, 2, 2, 1,
                2, 2, 1, 2, 2, 2, 1,
            )),
            ("harmonic minor", (
                2, 1, 2, 2, 1, 3, 1,
                2, 1, 2, 2, 1, 3, 1,
            )),
            ("melodic minor", (
                2, 1, 2, 2, 2, 2, 1,
                2, 1, 2, 2, 2, 2, 1,
            )),
        ]
    )
    def test_correct_step_pattern(self, mode, steps):
        m = ModeGroup(mode)
        assert steps == m.get_step_pattern()


class TestModeStr:
    def test_correct_str(self):
        m = ModeGroup("harmonic minor")
        assert "harmonic minor" == str(m)

    def test_correct_str_2(self):
        m = ModeGroup("major")
        assert "major" == str(m)


class TestModeEquality:
    def test_equal(self):
        m = ModeGroup("harmonic minor")
        m2 = ModeGroup("harmonic minor")
        assert m2 == m

    def test_major_equal(self):
        m = ModeGroup("major")
        m2 = ModeGroup("ionian")
        assert m2 == m

    def test_minor_equal(self):
        m = ModeGroup("minor")
        m2 = ModeGroup("aeolian")
        assert m2 == m

    @pytest.mark.parametrize(
        "other", [ModeGroup("minor"), "harmonic minor", len]
    )
    def test_inequality(self, other):
        c = ModeGroup("harmonic minor")
        assert other != c


class TestKNPParseNotation:
    @pytest.fixture
    def parser(self):
        return KeyNotationParser()

    @pytest.mark.parametrize(
        "notation, tonic, mode", [
            ("C", "C", ""),
            ("D# dorian", "D#", " dorian"),
            ("E melodic minor", "E", " melodic minor"),
            ("F aeolian", "F", " aeolian"),
        ]
    )
    def test_correct_groups(self, parser, notation, tonic, mode):
        t, m = parser.parse_notation(notation)
        assert tonic == t
        assert mode == m


class TestKey:
    @pytest.mark.parametrize(
        "notation, tonic, mode, submode", [
            ("B", "B", Mode.MAJOR, Submode.NONE),
            ("Db dorian", f"D{flat}", Mode.DORIAN, Submode.NONE),
            ("F# minor", f"F{sharp}", Mode.MINOR, Submode.NATURAL),
            ("G melodic minor", "G", Mode.MINOR, Submode.MELODIC),
        ]
    )
    def test_key_creation(self, notation, tonic, mode, submode):
        key = Key(notation)
        assert tonic == key.tonic
        assert mode == key.mode.mode
        assert submode == key.mode.submode


class TestKeyFromComps:
    def test_key_creation(self):
        key = Key.from_components("C", "major")
        assert "C" == key.tonic
        assert Mode.MAJOR == key.mode.mode
        assert Submode.NONE == key.mode.submode

    def test_key_creation_2(self):
        key = Key.from_components(Note("D"), "minor", "harmonic")
        assert "D" == key.tonic
        assert Mode.MINOR == key.mode.mode
        assert Submode.HARMONIC == key.mode.submode


class TestKeySetMode:
    def test_with_mode_and_submode(self):
        key = Key("C")
        key.set_mode("minor", "melodic")
        assert Mode.MINOR == key.mode.mode
        assert Submode.MELODIC == key.mode.submode

    def test_without_mode(self):
        key = Key("D minor")
        key.set_mode(submode="harmonic")
        assert Mode.MINOR == key.mode.mode
        assert Submode.HARMONIC == key.mode.submode

    def test_without_submode(self):
        key = Key("D melodic minor")
        key.set_mode(mode="dorian")
        assert Mode.DORIAN == key.mode.mode
        assert Submode.NONE == key.mode.submode


class TestKeyRelativeMajor:
    def test_correct_relative(self):
        key = Key("D minor")
        key.to_relative_major()
        assert "F major" == str(key)

    def test_wrong_mode(self):
        key = Key("D dorian")
        with pytest.raises(ModeError):
            key.to_relative_major()


class TestKeyRelativeMinor:
    def test_correct_relative(self):
        key = Key("D major")
        key.to_relative_minor()
        print(key.mode)
        assert "B natural minor" == str(key)

    def test_correct_relative_2(self):
        key = Key("D major")
        key.to_relative_minor("harmonic")
        assert "B harmonic minor" == str(key)

    def test_wrong_mode(self):
        key = Key("E phrygian")
        with pytest.raises(ModeError):
            key.to_relative_minor()


class TestKeyTranspose:
    def test_transpose(self):
        key = Key("E")
        key.transpose(6, 3)
        assert f"A{sharp}" == key.tonic

class TestKeyTransposeSimple:
    def test_transpose_sharps(self):
        key = Key("G")
        key.transpose_simple(-1)
        assert f"F{sharp}" == key.tonic

    def test_transpose_flats(self):
        key = Key("G")
        key.transpose_simple(1, use_flats=True)
        assert f"A{flat}" == key.tonic


class TestKeyEquality:
    def test_equality(self):
        c = Key("C")
        c2 = Key("C")
        assert c == c2

    @pytest.mark.parametrize(
        "other", [Key("D minor"), "D minor", len]
    )
    def test_inequality(self, other):
        d = Key("D harmonic minor")
        assert other != d
