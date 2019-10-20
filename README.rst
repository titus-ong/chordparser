===========
chordparser
===========

A simple Python 3 package to analyse chords.

.. image:: https://travis-ci.org/titus-ong/chordparser.svg?branch=master
   :alt: build status
   :target: https://travis-ci.org/titus-ong/chordparser

.. image:: https://coveralls.io/repos/github/titus-ong/chordparser/badge.svg?branch=master
   :alt: coverage
   :target: https://coveralls.io/github/titus-ong/chordparser

.. image:: https://img.shields.io/pypi/v/chordparser.svg
   :target: https://pypi.org/pypi/chordparser
   :alt: downloads

.. image:: https://img.shields.io/pypi/pyversions/chordparser.svg
   :target: https://pypi.org/pypi/chordparser
   :alt: downloads

chordparser aims to parse chord notation (e.g. in ChordPro file formats), and provide harmonic analysis of chords based on the key and nearby chords. This helps in understanding how each chord functions, and allows for conversion to roman numeral chord notation.

The chord functions that can be analysed are: diatonic chords, mode mixture/ borrowed chords (from other modes), secondary dominant chords (e.g. V/V), secondary leading tone chords.

chordparser will provide a simple ChordPro parser for demonstration of its chord analysis functions. It is not as full-featured as the `official ChordPro program <https://github.com/ChordPro/chordpro>`_, and does not aim to be. Rather, it serves as a proof-of-concept for analysing chords within the chord progression of songs.

-------
Install
-------

.. code-block:: python

    >>> pip -install chordparser

----------------
Current Features
----------------

* Parse notes
* Parse keys with different modes and submodes (e.g. harmonic/natural/melodic for minor)
* Scale with automatically-generated notes and diatonic chords
* Ability to transpose notes, keys and scales
* Parse chords

  - Root note, quality, triad, bass note
