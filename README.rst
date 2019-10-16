===========
chordparser
===========

A simple Python 3 package to parse ChordPro files.

.. image:: https://travis-ci.com/titus-ong/chordparser.svg
   :alt: build status
   :target: https://travis-ci.org/titus-ong/chordparser

.. image:: https://coveralls.io/repos/github/titus-ong/chordparser/badge.svg
   :alt: coverage
   :target: https://coveralls.io/github/titus-ong/chordparser

.. image:: https://img.shields.io/pypi/v/chordparser.svg
   :target: https://pypi.org/pypi/chordparser
   :alt: downloads

.. image:: https://img.shields.io/pypi/pyversions/chordparser.svg
   :target: https://pypi.org/pypi/chordparser
   :alt: downloads

This package is not as full-featured as the `official ChordPro program <https://github.com/ChordPro/chordpro>`_. It serves as a proof-of-concept for analysing chords within the chord progression of songs.
..
    Currently, the package only supports the following directives:

    - Title
    - Subtitle

    Installation
    ============

    .. code-block:: bash

        $ pip install chordparser

    Use
    ===

    .. code-block:: python

        >>> import chordparser as cp

        >>> new_parser = cp.Parser()
        >>> chordsheet = new_parser.parse('/path/to/chordpro/file.cho')
        >>> chordsheet.view()  # View .html file

        >>> # Useful functions
        >>> chordsheet.transpose(-2)  # Transpose down a tone
        >>> chordsheet.2roman()  # Change to Roman numeral analysis
        >>> chordsheet.analyse()  # Analyse chords based on surrounding chords (can only be done in Roman numerals)


