import pytest

from chordparser.music.notationparser import NotationParser


class TestNNPGetRegexGroupsCount:
    def test_correct_number_of_groups(self):
        parser = NotationParser()
        parser._pattern = "(a)(b)"
        assert 2 == parser.get_num_groups()
