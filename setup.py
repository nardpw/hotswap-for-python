#!/usr/bin/env python
import os
import sys
import shutil
import datetime

from setuptools import setup, find_packages
from setuptools.command.install import install

readme = open('README.md').read()

VERSION = '1.0.0'

VERSION += "_" + datetime.datetime.now().strftime('%Y%m%d%H%M')[2:]

setup(
    # Metadata
    name='hotswapper',
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
