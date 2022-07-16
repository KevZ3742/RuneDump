"""
Creates RuneDump Standalone for MacOS

Usage:
    python setup.py py2app
"""

from setuptools import setup

APP = ['RuneDump.py']
DATA_FILES = ['SavedRunes.json']
OPTIONS = {}

setup(
    name='RuneDump',
    app=APP,
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app']
)
