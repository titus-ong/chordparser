from .. import chordparser as cp
import pytest

def test_create():
    sheet = cp.create("sample_sheet.cho")
    assert isinstance(sheet, cp.Sheet), "Sheet not created from .cho file"

