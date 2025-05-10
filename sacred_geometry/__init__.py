"""
Advanced Sacred Geometry Package

A comprehensive Python library for creating, manipulating, and visualizing
sacred geometry patterns and shapes in both 2D and 3D.
"""

__version__ = '0.1.0'
__author__ = 'PMPly'

# Import core modules for easy access
try:
    from sacred_geometry.core.core import (
        create_flower_of_life,
        create_seed_of_life,
        create_metatrons_cube,
        create_vesica_piscis,
        create_fibonacci_spiral,
        create_regular_polygon,
        create_golden_rectangle,
        get_golden_ratio
    )
except ImportError:
    # Core modules might not be available
    pass

# Import 3D shape modules
try:
    from sacred_geometry.shapes.shapes import (
        create_tetrahedron,
        create_cube,
        create_octahedron,
        create_icosahedron,
        create_dodecahedron,
        create_merkaba,
        create_cuboctahedron,
        create_flower_of_life_3d,
        create_torus
    )
except ImportError:
    # Shape modules might not be available
    pass

# Import visualization modules
try:
    from sacred_geometry.visualization.visualization import (
        plot_2d_pattern,
        plot_3d_shape
    )
except ImportError:
    # Visualization modules might not be available
    pass

# Define package structure
__all__ = [
    # Core 2D patterns
    'create_flower_of_life',
    'create_seed_of_life',
    'create_metatrons_cube',
    'create_vesica_piscis',
    'create_fibonacci_spiral',
    'create_regular_polygon',
    'create_golden_rectangle',
    'get_golden_ratio',

    # 3D shapes
    'create_tetrahedron',
    'create_cube',
    'create_octahedron',
    'create_icosahedron',
    'create_dodecahedron',
    'create_merkaba',
    'create_cuboctahedron',
    'create_flower_of_life_3d',
    'create_torus',

    # Visualization
    'plot_2d_pattern',
    'plot_3d_shape',
]