import chordparser as cp
import pytest


def test_create():
    sheet = cp.create("tests/sample_sheet.cho")
    assert isinstance(sheet, cp.Sheet), "Sheet not created from .cho file"


def test_create_contents():
    sheet = cp.create("tests/sample_sheet.cho")
    with open("tests/sample_sheet.cho", 'r') as f:
        contents = f.readlines()
    assert sheet.contents == contents, "Sheet contents are incorrect"


def test_create_invalid_format():
    with pytest.raises(cp.chordsheet.ParseError):
        sheet = cp.create("tests/")
