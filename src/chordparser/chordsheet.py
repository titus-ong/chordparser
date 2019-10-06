class Error(Exception):
    pass


class ParseError(Error):
    pass


class Sheet:
    def __init__(self, contents):
        self.contents = contents
