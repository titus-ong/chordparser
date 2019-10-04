from setuptools import setup

setup(name='chordparser',
      version='1.0',
      description='Parse .cho (ChordPro) files',
      url='http://github.com/titus-ong/chordparser',
      author='Titus Ong',
      author_email='titusongyl@gmail.com',
      license='MIT',
      packages=['chordparser'],
      install_requires=[
          're',
          ]
      zip_safe=False)
