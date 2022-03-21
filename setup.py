"""
Setup file for building binaries
"""
from setuptools import setup, find_packages

setup(name='BorkumWebsite',
    version='1.0',
    packages=find_packages(include=['borkum', 'borkum.*']),
    classifiers=[
    "Programming Language :: Python :: 3",
    "Operating System :: OS Independent",
    ]
    )
