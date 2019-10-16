"""
Contains client classes to manipulate other classes.
"""
from .chords import Chord
from .scales import Scale
from .general import Error
from .directives import *
import re


class Directiver:
    _pattern = (
        "^(new_song|title|subtitle|artist"
        "|composer|lyricist|copyright|album"
        "|year|key|time|tempo|duration|capo"
        "|meta|comment|comment_italic"
        "|comment_box|image|start_of_chorus"
        "|end_of_chorus|chorus|start_of_verse"
        "|end_of_verse|start_of_tab|end_of_tab"
        "|start_of_grid|end_of_grid|define"
        "|chord|textfont|textsize|textcolour"
        "|chordfont|chordsize|chordcolour"
        "|tabfont|tabsize|tabcolour|new_page"
        "|new_physical_page|column_break"
        "|soc|eoc|sot|eot|npp|col|np|ng"
        "|ns|st|ci|cb|g|c|t)(:\\s{0,1}(.*)){0,1}$")

    def __init__(self):
        self.instructions = dict()

    def initialise(self, line: str, linenumber: int):
        rgx = re.match(Directiver._pattern, line)
        directive = self._classifier(rgx.group(1))
        return directive(rgx.group(3), linenumber)

    def _classifier(self, txt: str) -> Directive:
        if txt == 'title' or txt == 't':
            return TitleDirective
        elif txt == 'subtitle' or txt == 'st':
            return SubtitleDirective
        else:
            return UnknownDirective

    def add(self, directive: Directive):
        self.instructions.update(directive.instruction())


class Converter:
    def chord2scale(chord: Chord):
        return Scale(chord.key, chord.quality)


class Transposer:
    def transpose(value: int = 0):
        pass
        # parse chord to get position relative to base interval (if there's sharp/flat), then go to new key and add that position back to the sign
        # e.g. D# in G major --> +1 to D in G major
        # convert to Eb major --> Bb +1 ==> B in Eb major
