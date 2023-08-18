#!/usr/bin/env python
from pathlib import Path

from setuptools import setup, find_packages

readme = Path("README.md").read_text()

VERSION = "1.1.0"

setup(
    # Metadata
    name="hotcodeswap",
    version=VERSION,
    author="nardpw",
    author_email="",
    url="https://github.com/nardpw/hotswap-for-python",
    description="Hot-swapper for Python",
    long_description=readme,
    long_description_content_type="text/markdown",
    license="MIT",
    # Package info
    packages=find_packages(exclude=("*test*",)),
    #
    zip_safe=True,
    # nstall_requires=requirements,
    # Classifiers
    classifiers=[
        "Programming Language :: Python :: 3",
    ],
)
