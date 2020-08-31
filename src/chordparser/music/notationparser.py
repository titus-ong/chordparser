from abc import ABCMeta, abstractmethod
import re


class NotationParserTemplate(metaclass=ABCMeta):
    """Abstract class for parsing notation."""

    _pattern: str  # To be defined in concrete class

    @property
    def pattern(self):
        return self._pattern

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

    @abstractmethod
    def _split_into_groups(self, regex):
        pass

    def get_num_groups(self):
        regex = re.compile(self._pattern)
        return regex.groups
