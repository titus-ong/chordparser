from setuptools import setup, find_packages
import codecs
import os.path
import re


def readme():
    with open('README.rst') as f:
        return f.read()


def fpath(name):
    return os.path.join(os.path.dirname(__file__), name)


def read(fname):
    return codecs.open(fpath(fname), encoding='utf-8').read()


def grep(attrname):
    pattern = r"{0}\W*=\W*'([^']+)'".format(attrname)
    strval, = re.findall(pattern, file_text)
    return strval


file_text = read(fpath('src/chordparser/__init__.py'))


setup(name='chordparser',
      version=grep('__version__'),
      description='Parse and analyse chords',
      long_description=readme(),
      classifiers=[
          "Development Status :: 4 - Beta",
          'License :: OSI Approved :: MIT License',
          'Operating System :: OS Independent',
          "Natural Language :: English",
          'Programming Language :: Python :: 3.6',
          'Programming Language :: Python :: 3.7',
          'Programming Language :: Python :: 3.8',
          'Topic :: Text Processing',
          'Topic :: Software Development :: Libraries :: Python Modules',
          ],
      keywords=(
          'chords music parse notation analysis '
          'sheet notes scales keys transpose'
          ),
      url='http://github.com/titus-ong/chordparser',
      author=grep('__author__'),
      author_email=grep('__email__'),
      license='MIT',
      packages=find_packages(where='src'),
      package_dir={'': 'src'},
      setup_requires=['pytest-runner'],
      tests_require=['pytest'],
      install_requires=[],
      zip_safe=False)
