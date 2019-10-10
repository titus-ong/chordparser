"""
Parse chord notation and return key and mode.
"""
class Chord:
    pass


class ChordConverter:
    pass  # Convert chords to scales (keys) for roman numeral analysis

class ChordTransposer:
    pass  # parse chord to get position relative to base interval (if there's sharp/flat), then go to new key and add that position back to the sign
    # e.g. D# in G major --> +1 to D in G major
    # convert to Eb major --> Bb +1 ==> B in Eb major
