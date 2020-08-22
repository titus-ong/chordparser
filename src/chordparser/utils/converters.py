from chordparser.utils.unicode_chars import (flat, doubleflat,
                                             sharp, doublesharp)


symbol_to_unicode = {
    "b": flat,
    flat: flat,
    "bb": doubleflat,
    doubleflat: doubleflat,
    "#": sharp,
    sharp: sharp,
    "##": doublesharp,
    doublesharp: doublesharp,
    "": "",
    None: "",
}

symbol_to_int = {
    flat: -1,
    doubleflat: -2,
    sharp: 1,
    doublesharp: 2,
    "": 0,
}

int_to_symbol = {
    -1: flat,
    -2: doubleflat,
    1: sharp,
    2: doublesharp,
    0: "",
}
