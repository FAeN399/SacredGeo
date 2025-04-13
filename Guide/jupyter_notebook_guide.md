# Working with Sacred Geometry Jupyter Notebooks

This guide will help you get started with the interactive Jupyter notebooks in this project.

## Prerequisites

1. Install Python 3.7+ and Jupyter:
```bash
pip install jupyter notebook
```

2. Install the sacred-geometry package:
```bash
pip install sacred-geometry
```

## Available Notebooks

### 1. sacred_geometry_3d_shapes.ipynb
This notebook demonstrates 3D sacred geometry shapes including:
- Merkaba (Star Tetrahedron)
- Vector Equilibrium (Cuboctahedron)
- Platonic Solids
- Torus
- Metatron's Cube

### 2. merkaba_vector_equilibrium_exploration.ipynb
An in-depth exploration of:
- Merkaba's geometric properties and symmetries
- Vector Equilibrium's unique characteristics
- The relationship between these forms
- Interactive visualizations and animations

## Using the Notebooks

1. **Starting Jupyter**:
   ```bash
   jupyter notebook
   ```
   Navigate to the `examples` directory and open the desired notebook.

2. **Running Cells**:
   - Click a cell to select it
   - Press `Shift + Enter` to run the cell
   - Run cells in order from top to bottom
   - The first cell installs required packages

3. **Interactive Features**:
   - Use the sliders to adjust parameters
   - Change colors using dropdown menus
   - Toggle features with checkboxes
   - Click "Generate" buttons to create new visualizations

4. **3D Visualization Controls**:
   - Rotate: Click and drag
   - Zoom: Scroll wheel
   - Pan: Right-click and drag
   - Reset view: Home key

## Common Issues and Solutions

1. **ModuleNotFoundError**:
   ```python
   ModuleNotFoundError: No module named 'sacred_geometry'
   ```
   Solution: Run `pip install sacred-geometry` in a terminal

2. **Memory Issues**:
   If visualizations become slow or memory-intensive:
   - Reduce the number of particles in simulations
   - Lower the resolution of 3D shapes
   - Clear output of unused cells
   - Restart the kernel if needed

3. **Display Issues**:
   If 3D shapes don't display properly:
   - Ensure matplotlib backend is set correctly
   - Try restarting the kernel
   - Check that all required packages are installed

## Best Practices

1. **Memory Management**:
   - Clear outputs of cells you're not using
   - Restart kernel when switching between major sections
   - Save your work regularly

2. **Customization**:
   - Start with default parameters
   - Make incremental adjustments
   - Note combinations that work well
   - Save interesting configurations

3. **Exploration**:
   - Try different combinations of shapes
   - Experiment with color schemes
   - Adjust rotation angles
   - Save particularly meaningful or beautiful results

## Advanced Usage

1. **Creating Custom Patterns**:
   ```python
   # Example of combining shapes
   merkaba = create_merkaba(center=(0, 0, 0), radius=1.0)
   ve = create_cuboctahedron(center=(0, 0, 0), radius=1.2)
   ```

2. **Animation Tips**:
   - Adjust frame rates for smoother motion
   - Use higher DPI for better quality exports
   - Consider using HTML5 output for web sharing

3. **Export Options**:
   - Save static images as PNG
   - Export animations as GIF
   - Use high DPI for publication quality

## Getting Help

- Check the documentation strings in the code
- Review the example scripts in the `examples` directory
- Look at the reference implementations
- Read about sacred geometry concepts in the included references

## Next Steps

1. Start with the basic 3D shapes notebook
2. Move on to the Merkaba exploration
3. Try creating your own combinations
4. Experiment with animations
5. Share your discoveries!