"""
Module of all directives for chordpro files.
"""


class Directive:
    def __init__(self, statement, linenumber):
        self.statement = statement
        self.linenumber = linenumber


class TitleDirective(Directive):
    def instruction(self):
        return {'title': self.statement}


class SubtitleDirective(Directive):
    def instruction(self):
        return {'subtitle': self.statement}


class UnknownDirective(Directive):
    def instruction(self):
        return {}
