"""
A package to parse ChordPro files.
"""
from .chordsheet import Sheet
from .general import Error
from os.path import splitext
import re


class ParseError(Error):
    pass


def create(file_path):
    file_name, extension = splitext(file_path)
    print(extension)
    if not re.match(
                    "^.(cho|crd|chopro|chord|pro)$", extension
                    ):
        raise ParseError("File format cannot be read")
    with open(file_path, 'r') as f:
        contents = f.readlines()
    return Sheet(contents)
