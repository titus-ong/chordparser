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
