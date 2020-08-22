from chordparser.utils.unicode_chars import (flat, doubleflat,
                                             sharp, doublesharp)


note_pattern = "[a-gA-G]"
flat_pattern = f"bb|b|{flat}|{doubleflat}"
sharp_pattern = f"##|#|{sharp}|{doublesharp}"
