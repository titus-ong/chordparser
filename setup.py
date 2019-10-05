from setuptools import setup, find_packages

def readme():
    with open('README.md') as f:
        return f.read()

setup(name='chordparser',
      version='1.2',
      description='Parse .cho (ChordPro) files',
      long_description=readme(),
      classifiers=[
          'Development Status :: 3 - Alpha',
          'License :: OSI Approved :: MIT License',
          'Programming Language :: Python :: 3.7',
          'Topic :: Text Processing :: Markup',
          ],
      keywords='chord sheet music parse',
      url='http://github.com/titus-ong/chordparser',
      author='Titus Ong',
      author_email='titusongyl@gmail.com',
      license='MIT',
      packages=find_packages(where='src'),
      package_dir={'': 'src'},
      setup_requires=['pytest-runner'],
      tests_require=['pytest'],
      install_requires=[
          'pytest',
          ],
      zip_safe=False)
