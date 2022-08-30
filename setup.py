#!/usr/bin/env python
import os
import sys
import shutil
import datetime

from setuptools import setup, find_packages
from setuptools.command.install import install

try:
    readme = open('README.md').read()
except:
    readme = '''# Hotswap for Python

# Install

`pip install hotswap`

# Usage

Decorate the main function with @hotswap.main

# Example
```python
import hotswap
from time import sleep

def function():
    print('hoge')

class Calculater:

    def add(self, x, y):
        return x + y

@hotswap.main # add this to main function
def main():   # cannot be hot-swapped to the main function
    calc = Calculater()
    while True:
        function()
        print(calc.add(2, 3))
        sleep(1)

if __name__ == '__main__':
    main()

```
'''

VERSION = '1.0.0'

VERSION += "_" + datetime.datetime.now().strftime('%Y%m%d%H%M')[2:]

setup(
    # Metadata
    name='hotswap',
    version=VERSION,
    author='nardpw',
    author_email='',
    url='https://github.com/nardpw/hotswap-for-python',
    description='Hot-swapper for Python',
    long_description=readme,
    long_description_content_type='text/markdown',
    license='MIT',

    # Package info
    packages=find_packages(exclude=('*test*',)),

    #
    zip_safe=True,
    # nstall_requires=requirements,

    # Classifiers
    classifiers=[
        'Programming Language :: Python :: 3',
    ],
)
