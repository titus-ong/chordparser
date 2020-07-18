===========
chordparser
===========

A Python 3 package that provides a musical framework to analyse chords.

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

chordparser aims to act as a framework for harmonic analysis of chords based on keys and scales. This helps in understanding how each chord functions, and allows for the conversion to roman numeral chord notation.

Musical classes have been grouped into Notes, Keys, Scales, Chords and Romans as the foundation for analysing chords. Chord notation can be parsed as string input and converted to Chords, which have been built on the other classes.

The Parser is a one-stop shop for creating, manipulating and analysing the musical classes. It can be used to analyse the following chords: diatonic chords, mode mixture/ borrowed chords (from other modes), secondary dominant chords (e.g. V/V), secondary leading tone chords.

chordparser can be incorporated into Songbooks easily with its ability to transpose chords correctly. Check out the `Colab notebook <https://colab.research.google.com/drive/1T5WcH2WMHqpqbJrzxDt_Mg03lw1aXho7?usp=sharing>`_ on how you can do that and perform more advanced manipulation with other functions available in chordparser.

-------
Install
-------

.. code-block:: python

    >>> pip -install chordparser

--------
Features
--------

* Create and manipulate notes, keys, scales and chords easily
* Accept complex chord notations
* Transpose musical classes for easy transposition
* Automatically-generate notes for scales and chords
* Parse and store chord information on its quality, chord tones, and other sus/add/bass notes
* Generate roman numeral notation
* Analyse chord-scale relationships

-----
Usage
-----
Check out the `Colab notebook <https://colab.research.google.com/drive/1T5WcH2WMHqpqbJrzxDt_Mg03lw1aXho7?usp=sharing>`_.
