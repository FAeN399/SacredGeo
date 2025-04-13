# Advanced Sacred Geometry

A comprehensive Python toolkit for creating, manipulating, and visualizing sacred geometry patterns in both 2D and 3D.

## Features

### 3D Sacred Geometry
- **Platonic Solids**: All five regular polyhedra (Tetrahedron, Cube, Octahedron, Icosahedron, Dodecahedron)
- **Merkaba (Star Tetrahedron)**: Interactive creation with customizable rotation and colors
- **Vector Equilibrium (Cuboctahedron)**: Perfect equilibrium geometric form
- **3D Flower of Life**: Multi-layered spherical arrangement
- **Torus**: Customizable major and minor radii

### 2D Sacred Patterns
- **Flower of Life**: Multi-layered circular pattern
- **Metatron's Cube**: Complex geometric pattern with Platonic solid projections
- **Vesica Piscis**: Fundamental sacred geometry form
- **Fibonacci Spiral**: Golden ratio-based spiral pattern

### Fractal Patterns
- **Sierpinski Triangle**: Self-similar triangular fractal
- **Koch Snowflake**: Recursive fractal pattern
- **Sacred Spiral**: Golden ratio-based spiral
- **Fractal Tree**: Nature-inspired branching pattern

### Visualization Features
- Interactive 3D viewing with rotation and zoom
- Customizable colors and transparency
- Support for both 2D and 3D plotting
- Animation capabilities for pattern evolution
- High-quality figure export

## Installation

```bash
pip install sacred-geometry
```

### Requirements
- Python >= 3.7
- NumPy >= 1.20.0
- Matplotlib >= 3.4.0
- SymPy >= 1.8.0
- SciPy >= 1.7.0
- Additional visualization packages (see requirements.txt)

## Quick Start

```python
import numpy as np
from sacred_geometry.shapes.shapes import create_merkaba
from sacred_geometry.visualization.visualization import plot_3d_shape

# Create a Merkaba
merkaba = create_merkaba(center=(0, 0, 0), radius=1.0, rotation=np.pi/4)

# Visualize it
fig = plot_3d_shape(
    merkaba,
    title="Merkaba (Star Tetrahedron)",
    color_scheme="rainbow",
    alpha=0.7,
    show_edges=True,
    show_vertices=True
)
```

## Interactive Features

### Interactive Shape Explorer
The `sacred_geometry_interactive.ipynb` notebook provides an intuitive interface for exploring sacred geometry shapes with real-time controls:

- Shape selection (Merkaba, Vector Equilibrium, Platonic Solids, Torus)
- Size and rotation adjustments
- Color customization for each component
- Transparency controls
- Edge and vertex visibility toggles
- View angle adjustments

### Animation Controls
Create dynamic visualizations with customizable animation parameters:

- Rotation animation
- Scale pulsing
- Energy flow effects
- Color transitions
- Frame rate control
- Multiple animation types per shape

### Example Usage
```python
# Interactive shape visualization
from sacred_geometry.visualization.visualization import plot_3d_shape

shape = create_merkaba(center=(0, 0, 0), radius=1.0)
fig = plot_3d_shape(
    shape,
    color_scheme="custom",
    custom_color="blue",
    alpha=0.7,
    show_edges=True
)

# Interactive animation
from sacred_geometry.visualization.visualization import animate_pattern

anim = animate_pattern(
    create_flower_of_life,
    frames=60,
    interval=50,
    center=(0, 0),
    radius=1.0
)
```

## Examples

Check out the `examples` directory for detailed examples:
- `example_2d.py`: 2D sacred geometry patterns
- `example_3d.py`: 3D sacred geometry shapes
- `example_animations.py`: Animated patterns
- `merkaba_animations.py`: Special Merkaba animations
- Jupyter notebooks with interactive visualizations

## Documentation

For an in-depth overview of the library and its capabilities, see the [Deep Guide](documentation/Deep_Guide.md).

Each module includes comprehensive docstrings. Key modules:

- `sacred_geometry.shapes`: 3D geometric shapes
- `sacred_geometry.core`: Core geometric operations
- `sacred_geometry.fractals`: Fractal pattern generation
- `sacred_geometry.visualization`: Plotting utilities

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## References

### Books
- "Sacred Geometry: Philosophy & Practice" by Robert Lawlor
- "How the World Is Made: The Story of Creation According to Sacred Geometry" by John Michell
- "A Beginner's Guide to Constructing the Universe" by Michael S. Schneider

### Mathematical References
- "Polyhedra: Platonic, Archimedean, Stellations & More" by Jonathan Bowers
- "Regular Polytopes" by H.S.M. Coxeter

## License

This project is licensed under the MIT License - see the LICENSE file for details.