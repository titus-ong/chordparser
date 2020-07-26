chordparser
===========

.. image:: https://travis-ci.com/titus-ong/chordparser.svg?branch=master
   :alt: build status
   :target: https://travis-ci.com/titus-ong/chordparser

.. image:: https://readthedocs.org/projects/chordparser/badge/?version=latest
    :target: https://chordparser.readthedocs.io/en/latest/?badge=latest
    :alt: Documentation Status

.. image:: https://coveralls.io/repos/github/titus-ong/chordparser/badge.svg?branch=master
   :alt: coverage
   :target: https://coveralls.io/github/titus-ong/chordparser

.. image:: https://img.shields.io/pypi/v/chordparser.svg
   :target: https://pypi.org/pypi/chordparser
   :alt: downloads

.. image:: https://img.shields.io/pypi/pyversions/chordparser.svg
   :target: https://pypi.org/pypi/chordparser
   :alt: downloads

chordparser is a Python 3 package that provides a musical framework to analyse chords. Chord notation can be parsed into Chords, which can then be analysed against other chords or the key of the song. This allows for harmonic analysis in chord sheets and helps musicians understand why and how chord progressions work.

Quick demo:

.. code-block:: python

    >>> import chordparser
    >>> cp = chordparser.Parser()

    >>> new_chord = cp.create_chord("C7add4/E")
    >>> new_chord.notes
    (E note, C note, F note, G note, B♭ note)

    >>> new_chord.transpose_simple(6)
    F♯7add4/A♯ chord
    >>> new_chord.notes
    (A♯ note, F♯ note, B note, C♯ note, E note)

    >>> e_scale = cp.create_scale("E", "major")
    >>> cp.to_roman(new_chord, e_scale)
    II65 roman chord

    >>> e_fifth = cp.create_diatonic(e_scale, 5)
    >>> e_fifth
    B chord
    >>> cp.analyse_secondary(new_chord, e_fifth, e_scale)
    "V65/V"


--------
Features
--------

* Create and manipulate notes, keys, scales and chords easily
* Parse complex chord notations
* Transpose musical classes easily and accurately
* Automatically generate notes for scales and chords from notation
* Generate roman numeral notation from chords
* Analyse chord-scale relationships

------------
Installation
------------

To install chordparser, run this command in your terminal:

.. code-block:: console

    $ pip install chordparser

-----
Usage
-----

Check out the `Colab notebook <https://colab.research.google.com/drive/1T5WcH2WMHqpqbJrzxDt_Mg03lw1aXho7?usp=sharing>`_ for a quick introduction and a working example.

The full documentation can be found `here <https://chordparser.readthedocs.io/en/latest/>`_.

----------
Contribute
----------

- Issue Tracker: `github.com/titus-ong/chordparser/issues <github.com/titus-ong/chordparser/issues>`_
- Source Code: `github.com/titus-ong/chordparser <github.com/titus-ong/chordparser>`_

-------
Support
-------

If you are having issues, please let me know at: titusongyl@gmail.com

-------
Authors
-------

Development Lead

* Titus Ong <titusongyl@gmail.com>

-------
License
-------

The project is licensed under the MIT license.
