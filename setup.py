#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Setup script for Advanced Sacred Geometry package.

This package provides tools for creating, manipulating, and visualizing
sacred geometry patterns and shapes in both 2D and 3D.
"""

import os
from setuptools import setup, find_packages

# Read requirements from requirements.txt
with open('requirements.txt') as f:
    requirements = f.read().splitlines()

# Read long description from README.md if it exists
here = os.path.abspath(os.path.dirname(__file__))
try:
    with open(os.path.join(here, 'README.md'), encoding='utf-8') as f:
        long_description = f.read()
except FileNotFoundError:
    long_description = "Advanced Sacred Geometry - A toolkit for creating, manipulating, and visualizing sacred geometry patterns"

# Optional packages
EXTRAS = {
    'dev': [
        'pytest>=6.0.0',
        'pytest-cov>=2.10.0',
        'flake8>=3.8.0',
        'black>=20.8b1',
        'sphinx>=3.2.0',
        'sphinx-rtd-theme>=0.5.0',
    ],
    '3d': [
        'trimesh>=3.9.0',
        'pyglet>=1.5.0',
        'pyvista>=0.32.0',
        'plotly>=5.0.0',
    ],
    'animation': [
        'manim>=0.15.0',
        'pydub>=0.25.0',
    ],
    'web': [
        'flask>=2.0.0',
        'dash>=2.0.0',
    ],
}

setup(
    name="sacred_geometry",
    version="0.1.0",
    description="Advanced Sacred Geometry - A toolkit for creating, manipulating, and visualizing sacred geometry patterns",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="PMPly",
    author_email="your.email@example.com",  # Replace with your email
    url="https://github.com/PMPly/sacred-geometry",  # Replace with your repository URL
    packages=find_packages(exclude=["tests", "*.tests", "*.tests.*", "tests.*"]),
    install_requires=requirements,
    extras_require=EXTRAS,
    python_requires=">=3.7",
    include_package_data=True,
    license="MIT",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Scientific/Engineering :: Mathematics",
        "Topic :: Scientific/Engineering :: Visualization",
        "Topic :: Multimedia :: Graphics",
        "Intended Audience :: Education",
        "Intended Audience :: Science/Research",
        "Intended Audience :: Developers",
    ],
    entry_points={
        'console_scripts': [
            'sacred-geometry=sacred_geometry.cli:main',
            'sacred-geometry-gui=sacred_geometry.gui:main',
        ],
    },
    keywords=[
        'sacred geometry',
        'geometry',
        'mathematics',
        'visualization',
        'art',
        'education',
        'spirituality',
        'platonic solids',
        'flower of life',
        'metatron cube',
        'golden ratio',
        'fibonacci',
        'fractals',
    ],
)