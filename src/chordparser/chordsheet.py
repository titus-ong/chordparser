from general import Error


class ParseError(Error):
    pass


class Sheet:
    def __init__(self, contents):
        self.contents_raw = contents
