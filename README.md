# Advanced Sacred Geometry (SacredGeo)

A comprehensive Python library for creating, manipulating, and visualizing sacred geometry patterns and shapes in both 2D and 3D.

![Sacred Geometry Banner](docs/images/banner.png)

## Overview

Sacred Geometry is a term used to describe geometric patterns and shapes that are found throughout nature, art, architecture, and various spiritual traditions. This library provides tools to create, manipulate, and visualize these patterns programmatically.

## Features

- **2D Pattern Generation**: Create classic sacred geometry patterns like the Flower of Life, Seed of Life, Metatron's Cube, Vesica Piscis, and more.
- **3D Shape Generation**: Generate 3D sacred geometry shapes including Platonic solids, Merkaba, and other complex structures.
- **Fractal Patterns**: Create fractal patterns like the Sierpinski Triangle, Koch Snowflake, and custom sacred fractals.
- **Animations**: Generate animations of sacred geometry patterns forming and transforming.
- **Customization**: Adjust parameters like size, complexity, rotation, and color schemes.
- **Export Options**: Export your creations as images (PNG, SVG), 3D models (OBJ, STL), and animations (GIF, MP4).
- **Educational Information**: Access historical, cultural, and mathematical context for various patterns.
- **GUI Application**: User-friendly graphical interface for creating and exploring sacred geometry.

## Installation

### Basic Installation

```bash
pip install sacred-geometry
```

### Installation with Extra Features

For 3D visualization capabilities:
```bash
pip install sacred-geometry[3d]
```

For animation capabilities:
```bash
pip install sacred-geometry[animation]
```

For web interface:
```bash
pip install sacred-geometry[web]
```

For development:
```bash
pip install sacred-geometry[dev]
```

## Quick Start

### Creating 2D Patterns

```python
from sacred_geometry.core.core import create_flower_of_life
import matplotlib.pyplot as plt

# Create a Flower of Life pattern
flower = create_flower_of_life(center=(0, 0), radius=1.0, layers=3)

# Plot the pattern
fig, ax = plt.subplots(figsize=(10, 10))
for circle in flower:
    ax.plot(circle[:, 0], circle[:, 1], 'b-')
ax.set_aspect('equal')
plt.show()
```

### Creating 3D Shapes

```python
from sacred_geometry.shapes.shapes import create_merkaba
from sacred_geometry.visualization.visualization import plot_3d_shape
import matplotlib.pyplot as plt

# Create a Merkaba (Star Tetrahedron)
merkaba = create_merkaba(center=(0, 0, 0), radius=1.0, rotation=0.0)

# Plot the 3D shape
fig = plt.figure(figsize=(10, 10))
ax = fig.add_subplot(111, projection='3d')
plot_3d_shape(merkaba, ax=ax, color_scheme="golden")
plt.show()
```

### Using the GUI

```bash
# Launch the GUI application
sacred-geometry-gui
```

## Documentation

For detailed documentation, examples, and tutorials, visit our [documentation site](https://sacred-geometry.readthedocs.io).

## Gallery

![Flower of Life](docs/images/flower_of_life.png)
![Metatron's Cube](docs/images/metatrons_cube.png)
![Platonic Solids](docs/images/platonic_solids.png)
![Merkaba](docs/images/merkaba.png)

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Inspired by the mathematical beauty of sacred geometry across cultures and traditions
- Thanks to all contributors and the open-source community

## Contact

For questions, suggestions, or collaboration, please open an issue on GitHub or contact the maintainers directly.
