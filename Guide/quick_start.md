# Quick Start Guide - Advanced Sacred Geometry

Get started quickly with creating and visualizing sacred geometry patterns.

## Installation

1. **Create a virtual environment** (recommended):
```bash
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
.venv\Scripts\activate     # Windows
```

2. **Install the package**:
```bash
pip install sacred-geometry
```

## Basic Usage

### 1. Creating 2D Patterns

```python
from sacred_geometry.core.core import create_flower_of_life
from sacred_geometry.visualization.visualization import plot_2d_pattern

# Create a Flower of Life
flower = create_flower_of_life(center=(0, 0), radius=1.0, layers=3)

# Visualize it
plot_2d_pattern(flower, title="Flower of Life", color_scheme="golden")
```

### 2. Creating 3D Shapes

```python
from sacred_geometry.shapes.shapes import create_merkaba
from sacred_geometry.visualization.visualization import plot_3d_shape

# Create a Merkaba
merkaba = create_merkaba(center=(0, 0, 0), radius=1.0, rotation=np.pi/4)

# Visualize it
plot_3d_shape(merkaba, title="Merkaba", color_scheme="rainbow")
```

## Key Features Overview

### 2D Patterns
- Flower of Life
- Metatron's Cube
- Vesica Piscis
- Fibonacci Spiral
- Sacred Spirals
- Fractal Patterns

### 3D Shapes
- Merkaba
- Vector Equilibrium
- Platonic Solids
- 3D Flower of Life
- Torus

### Animations
- Pattern Growth
- Shape Rotations
- Energy Flows
- Fractal Evolution

## Example Scripts

Find complete examples in the `examples` directory:
- `example_2d.py`: 2D pattern examples
- `example_3d.py`: 3D shape examples
- `example_animations.py`: Animation examples
- `merkaba_animations.py`: Specialized Merkaba animations

## Jupyter Notebooks

Interactive exploration available in:
- `sacred_geometry_3d_shapes.ipynb`
- `merkaba_vector_equilibrium_exploration.ipynb`

## Output Directory Structure

```
outputs/
├── 2d/             # Static 2D patterns
├── 3d/             # Static 3D shapes
├── animations/     # GIF animations
└── custom/         # Your custom outputs
```

## Next Steps

1. Try the example scripts
2. Explore the Jupyter notebooks
3. Create custom patterns
4. Experiment with animations
5. Read the detailed guides in the Guide directory

## Common Commands

```python
# Create and save a pattern
pattern = create_flower_of_life(center=(0, 0), radius=1.0)
fig = plot_2d_pattern(pattern)
fig.savefig('my_pattern.png')

# Create and animate a Merkaba
from sacred_geometry.shapes.shapes import create_merkaba
merkaba = create_merkaba(radius=1.0, rotation=np.pi/4)
fig = plot_3d_shape(merkaba)
plt.show()
```

## Getting Help

- Check the documentation in the Guide directory
- Look at example scripts
- Read docstrings in the source code
- Explore Jupyter notebooks

## Tips for Success

1. Start with basic patterns
2. Use default parameters first
3. Make incremental changes
4. Save your work frequently
5. Monitor memory usage with large patterns