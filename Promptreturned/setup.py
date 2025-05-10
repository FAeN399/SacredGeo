#!/usr/bin/env python
"""
Setup script for Advanced Sacred Geometry package.
"""
from setuptools import setup, find_packages

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setup(
    name="sacred_geometry",
    version="0.1.0",
    description="Advanced Sacred Geometry - A toolkit for creating, manipulating, and visualizing sacred geometry patterns",
    author="PMPly",
    packages=find_packages(),
    install_requires=requirements,
    python_requires=">=3.7",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)