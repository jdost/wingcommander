#!/usr/bin/env python

import os
import sys

sys.path.append(os.getcwd() + "/src/")

import wingcommander

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

f = open('README.md', 'r')
readme = f.read()
f.close()

tags = [
    "Development Status :: 3 - Alpha",
    "Intended Audience :: Developers",
    "Natural Language :: English",
    "License :: OSI Approved :: Apache Software License",
    "Operating System :: Unix",
    "Operating System :: MacOS",
    "Environment :: Console",
    "Programming Language :: Python",
    "Programming Language :: Python :: 2.7",
]

setup(
    name="wingcommander",
    version=wingcommander.__version__,
    description="Pythonic commandline applications",
    long_description=readme,
    license="Apache 2.0",

    author="Jeff Ostendorf",
    author_email="jostendorf@gmail.com",
    url="http://jdost.us/wingcommander/",

    packages=['wingcommander'],
    package_dir={'wingcommander': 'src/wingcommander'},
    package_data={'': ['LICENSE']},
    include_package_data=True,

    classifiers=tags
)
