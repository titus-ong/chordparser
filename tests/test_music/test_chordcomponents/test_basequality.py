import pytest

from chordparser.music.chordcomponents.basequality import BaseQuality
from chordparser.music.scaledegree import ScaleDegree


class TestBaseQualityScaleDegrees:
    @pytest.mark.parametrize(
        "quality, sd", [
            (BaseQuality.MAJOR, (
                ScaleDegree("1"),
                ScaleDegree("3"),
                ScaleDegree("5"),
            )),
            (BaseQuality.SUS2, (
                ScaleDegree("1"),
                ScaleDegree("2"),
                ScaleDegree("5"),
            )),
        ]
    )
    def test_correct_scale_degrees_created(self, quality, sd):
        assert sd == quality.scale_degrees
