-------
History
-------

0.3.5 (2020-07-20)
~~~~~~~~~~~~~~~~~~
* Included ``transpose_simple`` method to only use semitones for transposing
* Included initial Sphinx documentation

0.3.4 (2020-07-19)
~~~~~~~~~~~~~~~~~~
* Removed code with static typing
* Removed unused instance variables in classes
* Changed ``Note.symbolvalue()`` to ``Note.symbol_value()`` for namespace consistency
* Include ``Note.letter_value()`` method
* Fixed wrong errors being raised
* Refactored scale building code
* Abstracted chord quality to a separate Quality class
* Quality now includes sus chords, Chords no longer have a ``Chord.sus`` attribute
* Refactored chord notation regex parsing for methods to be reusable
* Abstracted roman numeral notation to a separate Roman class, and roman conversion to a separate ChordRomanConverter class

0.2.2 (2020-06-25)
~~~~~~~~~~~~~~~~~~
* Changed song in sample_sheet.cho
* Added ability to remove all added notes
* ``incl_submodes`` defaulted to False in analysing chords

0.2.1 (2020-06-24)
~~~~~~~~~~~~~~~~~~
* Bug fixes for sample_sheet.cho

0.2.0 (2020-06-24)
~~~~~~~~~~~~~~~~~~
* Separated parsing function into Editor classes - NoteEditor, KeyEditor, ScaleEditor, ChordEditor
* Refactored regex parsing for code to be more readable and for regex groups to be more distinct
* Added ChordAnalyser for analysing chords
* Added Parser class to collate all the Editors

0.1.1 (2019-10-21)
~~~~~~~~~~~~~~~~~~
* Added Chord class with full parsing function

0.1.0 (2019-10-11)
~~~~~~~~~~~~~~~~~~

* First release on PyPI.