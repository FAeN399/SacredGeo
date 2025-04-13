# Deep Guide to the Advanced Sacred Geometry Program

## Overview
A comprehensive Python library for exploring, visualizing, and animating sacred geometry patterns in both 2D and 3D. The library provides tools for generating classical sacred geometry forms, creating interactive visualizations, and exploring mathematical relationships between different geometric structures.

## Core Features
- 3D Sacred Geometry Shapes (Merkaba, Vector Equilibrium, Platonic Solids)
- 2D Sacred Patterns (Flower of Life, Metatron's Cube)
- Interactive Visualizations
- Sacred Geometry Animations
- Fractal Pattern Generation
- Layered Compositions

## Installation
```bash
pip install sacred-geometry
```

## Library Structure
```
sacred_geometry/
├── core/
│   ├── __init__.py
│   └── core.py         # Basic geometric primitives
├── shapes/
│   ├── __init__.py
│   └── shapes.py       # 3D sacred geometry shapes
├── visualization/
│   ├── __init__.py
│   └── visualization.py # Plotting and animation tools
├── fractals/
│   ├── __init__.py
│   └── fractals.py     # Fractal pattern generators
└── composition/
    ├── __init__.py
    └── composition.py  # Layered composition tools
```

## Core Modules

### 1. Sacred Geometry Shapes
The shapes module provides functions to generate various sacred geometry forms:

- **Platonic Solids**
  - Tetrahedron
  - Cube
  - Octahedron
  - Icosahedron
  - Dodecahedron

- **Advanced Forms**
  - Merkaba (Star Tetrahedron)
  - Vector Equilibrium (Cuboctahedron)
  - Torus
  - Flower of Life (3D)

### 2. 2D Patterns
Functions for generating 2D sacred geometry patterns:

- Flower of Life
- Metatron's Cube
- Vesica Piscis
- Fibonacci Spiral
- Sacred Spirals
- Fractal Patterns

### 3. Visualization Tools
Comprehensive visualization capabilities:

- 3D shape plotting
- 2D pattern rendering
- Interactive controls
- Animation support
- Custom color schemes
- Sacred ratio proportions

### 4. Composition System
Tools for creating complex geometric arrangements:

- Hierarchical scene graph
- Transform operations
- Sacred ratio scaling
- Symmetry groups
- Pattern layering

## Examples

### 1. Creating a Basic 3D Shape
```python
from sacred_geometry.shapes import create_merkaba
from sacred_geometry.visualization import plot_3d_shape

# Create a Merkaba
merkaba = create_merkaba(center=(0, 0, 0), radius=1.0, rotation=np.pi/4)

# Visualize it
plot_3d_shape(merkaba, color_scheme="rainbow")
```

### 2. Generating a 2D Pattern
```python
from sacred_geometry.core import create_flower_of_life
from sacred_geometry.visualization import plot_2d_pattern

# Create Flower of Life
flower = create_flower_of_life(center=(0, 0), radius=1.0, layers=6)

# Visualize pattern
plot_2d_pattern(flower, color_scheme="golden")
```

### 3. Creating an Animation
```python
from sacred_geometry.visualization import animate_pattern

# Create and save an animation
animate_pattern(
    pattern_type="merkaba",
    num_frames=60,
    rotation=True,
    save_path="merkaba_rotation.gif"
)
```

## Advanced Topics

### 1. Sacred Ratios
The library implements key sacred geometry ratios:
- Golden Ratio (φ ≈ 1.618033988749895)
- Square Root of 2 (√2 ≈ 1.4142135623730951)
- Square Root of 3 (√3 ≈ 1.7320508075688772)

### 2. Symmetry Groups
Support for various symmetry operations:
- Tetrahedral symmetry
- Octahedral symmetry
- Icosahedral symmetry
- Dihedral symmetry
- Mirror symmetry

### 3. Fractal Patterns
Implementation of sacred geometry fractals:
- Sierpinski Triangle
- Koch Snowflake
- Sacred Spirals
- Fractal Trees

## Interactive Features

The library provides extensive interactive capabilities through Jupyter notebooks:

1. **Shape Exploration**
   - Rotation controls
   - Transparency adjustment
   - Color customization
   - Scale manipulation

2. **Pattern Generation**
   - Layer control
   - Symmetry selection
   - Color scheme selection
   - Export options

3. **Animation Controls**
   - Frame rate adjustment
   - Rotation speed
   - Transform parameters
   - Export settings

## Mathematical Foundations

### 1. Geometric Principles
- Vector mathematics
- 3D transformations
- Sacred ratios
- Symmetry groups

### 2. Implementation Details
- Vertex computation
- Face generation
- Edge detection
- Normal calculation

## Usage Guidelines

### 1. Basic Usage
```python
from sacred_geometry import shapes, visualization

# Create and visualize shapes
shape = shapes.create_tetrahedron()
visualization.plot_3d_shape(shape)
```

### 2. Advanced Usage
```python
from sacred_geometry import composition

# Create complex compositions
scene = composition.GeometryScene()
scene.add_shape(shape1, position=(0, 0, 0))
scene.add_shape(shape2, position=(1, 0, 0))
scene.apply_sacred_ratio_scaling()
```

## Contributing

Contributions are welcome! Please read our contributing guidelines and code of conduct.

### Development Setup
1. Clone the repository
2. Install dependencies
3. Run tests
4. Submit pull requests

## References

### Books
- "Sacred Geometry: Philosophy & Practice" by Robert Lawlor
- "A Beginner's Guide to Constructing the Universe" by Michael S. Schneider

### Online Resources
- Sacred Geometry International
- Wolfram MathWorld - Geometric Shapes

### Research Papers
- Various papers on geometric modeling
- Studies on sacred geometry principles

## License

This project is licensed under the MIT License - see the LICENSE file for details.
