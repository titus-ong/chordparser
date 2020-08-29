import re


class NotationParserTemplate:
    """Abstract class for parsing notation."""
    _pattern = ""

    def parse_notation(self, notation):
        regex = self._to_regex_object(notation)
        if self._invalid_notation(regex):
            raise SyntaxError("invalid syntax")
        args = self._split_into_groups(regex)
        return args

    def _to_regex_object(self, notation):
        regex = re.match(
            f"{self._pattern}$",
            notation,
            flags=re.UNICODE | re.IGNORECASE,
        )
        return regex

    def _invalid_notation(self, regex):
        return not regex

    def _split_into_groups(self, regex):
        # To be implemented in concrete class
        raise NotImplementedError

    @property
    def pattern(self):
        return self._pattern

    def get_num_groups(self):
        return NotationParser.get_num_groups_from(self._pattern)

    @staticmethod
    def get_num_groups_from(pattern):
        regex = re.compile(pattern)
        return regex.groups
