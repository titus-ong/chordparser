"""
Test the create function of chordparser and ensure only chordpro files can be imported.
"""
import chordparser as cp
import pytest


def test_create():
    sheet = cp.create("tests/sample_sheet.cho")
    assert isinstance(sheet, cp.Sheet)


def test_create_contents():
    sheet = cp.create("tests/sample_sheet.cho")
    with open("tests/sample_sheet.cho", 'r') as f:
        contents = f.readlines()
    assert sheet.contents_raw == contents


def test_create_invalid_format():
    with pytest.raises(cp.ParseError):
        sheet = cp.create("tests/")
