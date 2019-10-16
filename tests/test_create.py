"""
Test the create function of chordparser and ensure only chordpro files can be imported.
"""
import chordparser as cp
import pytest


@pytest.fixture
def create_sheet():
    parser = cp.Parser()
    return parser.parse("tests/samples/sample_sheet.cho")


def test_create(create_sheet):
    sheet = create_sheet
    assert isinstance(sheet, cp.Sheet)


def test_create_contents(create_sheet):
    sheet = create_sheet
    with open("tests/samples/sample_sheet.cho", 'r') as f:
        contents = f.readlines()
    assert sheet.contents_raw == contents


def test_create_invalid_format():
    with pytest.raises(cp.FormatError):
        parser = cp.Parser()
        sheet = parser.parse("tests/")


@pytest.mark.parametrize("file", [
    'tests/samples/sheet_error_brackets.cho',
    'tests/samples/sheet_error_brackets_2.cho',
    'tests/samples/sheet_error_brackets_3.cho',
    'tests/samples/sheet_error_brackets_4.cho',
    ])
def test_create_invalid_format(file):
    with pytest.warns(SyntaxWarning):
        parser = cp.Parser()
        sheet = parser.parse(file)
