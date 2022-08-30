#!/usr/bin/env python
import os
from pathlib import Path
import sys
import shutil
import datetime

from setuptools import setup, find_packages
from setuptools.command.install import install

readme = Path('README.md').read_text()

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
