"""
Store ChordPro file as a chordparser.Sheet.
"""
from .modules import Directiver
import re
import warnings


class Sheet:
    def __init__(self, contents):
        self.contents_raw = contents
        self.directiver = Directiver()
        self.contents = self.process_contents()

    def process_contents(self):
        self._check_formatting()
        contents = self._parse_lines()
        return contents
        # Check file formatting - brackets and all that
        # Divide file up into different parts - lyrics and chords and {}?

    def _check_formatting(self):
        if not self._check_brackets():
            warnings.warn(
                "Brackets are not closed."
                "This may affect how the file is being displayed",
                SyntaxWarning)
        return

    def _check_brackets(self):
        _open = {'{': '}', '[': ']'}
        _close = ('}', ']')
        for line in self.contents_raw:
            _brackets = []
            for char in line:
                if char in _open.keys():
                    _brackets.append(_open[char])
                elif char in _close:
                    try:
                        last = _brackets.pop()
                        if last != char:
                            raise IndexError
                    except IndexError:  # Also occurs for empty bracket lists
                        return
                else:
                    pass
            if _brackets:
                return
        else:
            return True

    def _parse_lines(self):
        self.contents = []
        pattern = r'^\{(.*)\}$'
        for idx, line in enumerate(self.contents_raw):
            rgx = re.match(pattern, line)
            if rgx:
                self._parse_curly(rgx.group(1), idx)
            else:
                self._parse_normal(line)
        return

    def _parse_curly(self, line, linenumber):
        directive = self.directiver.initialise(line, linenumber)
        self.directiver.add(directive)
        return

    def _parse_normal(self, line):
        pass

    def __repr__(self):
        return 'Chordsheet'
