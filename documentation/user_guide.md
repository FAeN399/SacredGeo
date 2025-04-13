# Advanced Sacred Geometry: Step-by-Step User Guide

This guide will walk you through using the Advanced Sacred Geometry program, with special focus on the interactive notebooks that provide the richest exploration experience.

## Table of Contents

1. [Getting Started](#getting-started)
2. [Understanding the Notebooks](#understanding-the-notebooks)
3. [Exploring 3D Sacred Shapes](#exploring-3d-sacred-shapes)
4. [Interactive Merkaba & Vector Equilibrium Exploration](#interactive-merkaba--vector-equilibrium-exploration)
5. [Creating Layered Compositions](#creating-layered-compositions)
6. [Generating Animations](#generating-animations)
7. [Creating Your Own Sacred Geometry Patterns](#creating-your-own-sacred-geometry-patterns)
8. [Troubleshooting](#troubleshooting)

## Getting Started

### Installation

1. Ensure you have Python 3.7+ installed on your system
2. Clone the repository or download the source code
3. Install the required dependencies:

```bash
pip install -r requirements.txt
```

### Running Jupyter Notebooks

1. Navigate to the project directory in your terminal
2. Launch Jupyter Notebook:

```bash
jupyter notebook
```

3. In your browser, navigate to the `examples` folder to find the interactive notebooks

![Image: Screenshot showing Jupyter home page with examples folder highlighted]

## Understanding the Notebooks

The project includes several notebook files, each focusing on different aspects of sacred geometry:

| Notebook | Description |
|----------|-------------|
| `sacred_geometry_3d_shapes.ipynb` | Explores the Platonic solids, Merkaba, and other 3D sacred forms |
| `merkaba_vector_equilibrium_exploration.ipynb` | Deep dive into the relationship between Merkaba and Vector Equilibrium |
| `layered_compositions.ipynb` | Advanced techniques for creating hierarchical arrangements of sacred geometry forms |
| `sacred_geometry_interactive.ipynb` | Interactive widgets for real-time exploration of sacred geometry |

## Exploring 3D Sacred Shapes

Open `sacred_geometry_3d_shapes.ipynb` to begin exploring 3D sacred geometry forms.

1. **Run the first few cells** to import libraries and setup the environment
   
   ![Image: Screenshot showing code cell with imports and setup]

2. **Explore the Merkaba (Star Tetrahedron)**
   - Run the Merkaba visualization cells to see this sacred form from different rotation angles
   - Notice how two tetrahedra interpenetrate to create a balanced form

   ![Image: Screenshot showing Merkaba visualization with different rotation values]

3. **Discover the Vector Equilibrium**
   - Run the Vector Equilibrium cells to visualize this perfectly balanced form
   - Observe how all vectors from center to vertices are of equal length
   
   ![Image: Screenshot showing Vector Equilibrium visualization]

4. **Explore all five Platonic Solids**
   - Run the Platonic Solids cell to generate all five forms
   - Each shape represents a different element in ancient traditions
   
   ![Image: Screenshot showing all five Platonic solids]

5. **Analyze geometric relationships**
   - The notebook includes cells that analyze mathematical properties
   - Run these cells to see golden ratio relationships and symmetry properties
   
   ![Image: Screenshot showing analysis of geometric relationships]

## Interactive Merkaba & Vector Equilibrium Exploration

The `merkaba_vector_equilibrium_exploration.ipynb` notebook provides interactive tools for deeper understanding.

1. **Open the notebook** and run the setup cells

2. **Use the interactive Merkaba visualization**
   - Adjust the rotation slider to see how the two tetrahedra relate at different angles
   - Experiment with colors and transparency to highlight different aspects
   
   ![Image: Screenshot showing interactive Merkaba sliders and visualization]

3. **Explore the Vector Equilibrium interactively**
   - Use sliders to adjust the properties of triangular and square faces
   - Toggle visibility of vertices and edges
   
   ![Image: Screenshot showing Vector Equilibrium interactive controls]

4. **Discover the relationship between forms**
   - The "Relationship" section reveals how Merkaba and Vector Equilibrium connect
   - Notice optimal alignment occurs at π/4 (45°) rotation
   
   ![Image: Screenshot showing relationship between Merkaba and Vector Equilibrium]

5. **Run the animation cell**
   - Watch the transformation between forms
   - Notice when the gold outline appears showing alignment points
   
   ![Image: Screenshot showing animation of Merkaba rotation]

6. **Explore energy field simulations**
   - Run the energy field cells to visualize simulated energy distribution
   - Compare different shapes and particle densities
   
   ![Image: Screenshot showing energy field simulation]

7. **Create custom sacred geometry patterns**
   - Use the custom generator at the end of the notebook
   - Mix and match different forms with various parameters
   
   ![Image: Screenshot showing custom geometry generator]

## Creating Layered Compositions

The `layered_compositions.ipynb` notebook demonstrates how to create complex hierarchical arrangements.

1. **Run the setup cells** to import necessary modules

2. **Explore basic parent-child relationships**
   - Run the cell creating a parent tetrahedron with child tetrahedra
   - Notice how children are positioned at the vertices of the parent
   
   ![Image: Screenshot showing parent-child tetrahedron composition]

3. **Try sacred ratio progressions**
   - Run the golden ratio progression cell
   - Observe how shapes scale according to sacred proportions
   
   ![Image: Screenshot showing golden ratio progression]

4. **Explore symmetry groups**
   - Run the cells creating different symmetry patterns
   - Note how shapes are arranged according to specific symmetry rules
   
   ![Image: Screenshot showing symmetry group compositions]

5. **Create mandalas**
   - Generate sacred geometry mandalas with different parameters
   - Experiment with spiral arrangements and varying rings
   
   ![Image: Screenshot showing sacred geometry mandala]

6. **Build fractal geometry**
   - Run the fractal composition cells
   - Observe self-similarity at different scales
   
   ![Image: Screenshot showing fractal tetrahedron composition]

7. **Use the interactive composition explorer**
   - Select different compositions from the dropdown
   - Observe how different techniques create unique forms
   
   ![Image: Screenshot showing interactive composition explorer]

## Generating Animations

You can create animations of sacred geometry patterns using either the notebooks or Python scripts.

### Using the Animation Script

1. Run the `example_animations.py` script:

```bash
python examples/example_animations.py
```

2. Check the `examples/outputs/animations` folder for generated GIF files

![Image: Screenshot showing animation output files]

### Creating Custom Animations

1. Open a notebook that supports animations (like the Merkaba exploration)
2. Run the animation cells
3. Modify parameters to create custom animations
4. Use the HTML output to view animations in the notebook

![Image: Screenshot showing animation code and output]

## Creating Your Own Sacred Geometry Patterns

Ready to create your own sacred geometry patterns? Here's how:

1. **Start with the interactive notebooks**
   - Use existing interactive cells as templates
   - Experiment with different parameters

2. **Combine different shapes**
   - Create compositions using multiple sacred forms
   - Apply sacred ratios for proper proportions

3. **Apply mathematical transformations**
   - Use rotation, scaling, and positioning
   - Try different symmetry operations

4. **Export your creations**
   - Use the save buttons in interactive tools
   - Or add code to save figures programmatically:
   
```python
plt.savefig("my_sacred_geometry.png", dpi=300)
```

## Troubleshooting

### Common Issues

1. **Missing Dependencies**
   - Ensure all requirements are installed: `pip install -r requirements.txt`
   - For 3D visualization issues: `pip install matplotlib numpy ipywidgets`

2. **Jupyter Widget Issues**
   - If widgets don't display, run: `jupyter nbextension enable --py widgetsnbextension`
   - For JupyterLab, run: `jupyter labextension install @jupyter-widgets/jupyterlab-manager`

3. **Visualization Problems**
   - Try restarting the kernel: Kernel → Restart
   - For 3D display issues, ensure you have a compatible backend: `matplotlib.use('Agg')` may help

4. **Getting Help**
   - Consult the comprehensive documentation in the `documentation` folder
   - Check the `Deep_Guide.md` for detailed explanations of concepts
   - Explore the source code for implementation details

---

We hope this guide helps you explore the fascinating world of sacred geometry through this software. The interactive notebooks provide just a starting point - feel free to experiment and discover your own sacred geometry insights!

[Back to Top](#advanced-sacred-geometry-step-by-step-user-guide)
