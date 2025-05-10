"""
Script to generate complex sacred geometry compositions.
This script creates and saves various layered compositions and geometric arrangements.
"""
import os
import numpy as np
import matplotlib.pyplot as plt

# Import 3D shape generators
from sacred_geometry.shapes.shapes import (
    create_tetrahedron, create_cube, create_octahedron,
    create_icosahedron, create_dodecahedron, create_merkaba,
    create_cuboctahedron, create_torus
)

# Import visualization tools
from sacred_geometry.visualization.visualization import plot_3d_shape

# Import composition tools
from sacred_geometry.composition.composition import (
    GeometryNode, GeometryScene, 
    create_symmetry_group, create_fractal_shape, create_shape_mandala,
    create_geometric_progression, apply_golden_ratio_proportions,
    rotate_around_axis, mirror_across_plane, apply_radial_symmetry,
    PHI, SQRT2, SQRT3, PI
)

# Create output directory if it doesn't exist
output_dir = "outputs/compositions"
os.makedirs(output_dir, exist_ok=True)

def save_figure(fig, filename):
    """Save figure to the output directory."""
    filepath = os.path.join(output_dir, filename)
    fig.savefig(filepath, dpi=300, bbox_inches='tight')
    print(f"Saved: {filepath}")
    plt.close(fig)

def plot_geometry_node(node, title="Sacred Geometry Composition", 
                     figure_size=(12, 10), color_scheme="rainbow"):
    """Plot a GeometryNode or GeometryScene."""
    fig = plt.figure(figsize=figure_size)
    ax = fig.add_subplot(111, projection='3d')
    ax.set_title(title)
    
    # Recursively plot all shapes in the node
    _plot_node_recursive(node, ax, color_scheme)
    
    # Set equal aspect ratio
    ax.set_box_aspect([1, 1, 1])
    
    return fig

def _plot_node_recursive(node, ax, color_scheme):
    """Helper function to recursively plot a node and its children."""
    # Plot the current node if it has shape data
    if hasattr(node, 'shape_data') and node.shape_data is not None:
        # Use the node's color if specified
        custom_color = node.color if hasattr(node, 'color') and node.color else None
        alpha = node.alpha if hasattr(node, 'alpha') and node.alpha is not None else 0.7
        
        # Plot the shape
        plot_3d_shape(
            node.shape_data,
            color_scheme=color_scheme if custom_color is None else "custom",
            custom_color=custom_color,
            alpha=alpha,
            show_edges=True,
            show_vertices=False,
            ax=ax
        )
    
    # Recursively plot all children
    if hasattr(node, 'children'):
        for child in node.children:
            _plot_node_recursive(child, ax, color_scheme)

# ===== Generate Compositions =====
print("\nGenerating compositions...")

# 1. Fractal Tetrahedron
print("Creating Fractal Tetrahedron...")
scene = GeometryScene()
fractal_tetra = scene.create_fractal_tetrahedron(depth=3)
fig = plot_geometry_node(scene.root, title="Fractal Tetrahedron")
save_figure(fig, "fractal_tetrahedron.png")

# 2. Nested Platonic Solids
print("Creating Nested Platonic Solids...")
scene = GeometryScene()
root = scene.root

# Create nested platonic solids with golden ratio scaling
tetra = create_tetrahedron(radius=1.0)
tetra_node = GeometryNode("Tetrahedron", tetra, color='red', alpha=0.4)
root.add_child(tetra_node)

cube = create_cube(radius=1.0 * PHI)
cube_node = GeometryNode("Cube", cube, color='blue', alpha=0.3)
root.add_child(cube_node)

octa = create_octahedron(radius=1.0 * PHI * PHI)
octa_node = GeometryNode("Octahedron", octa, color='green', alpha=0.3)
root.add_child(octa_node)

icosa = create_icosahedron(radius=1.0 * PHI * PHI * PHI)
icosa_node = GeometryNode("Icosahedron", icosa, color='purple', alpha=0.2)
root.add_child(icosa_node)

fig = plot_geometry_node(root, title="Nested Platonic Solids (Golden Ratio Scaling)")
save_figure(fig, "nested_platonic_solids.png")

# 3. Merkaba Star Mandala
print("Creating Merkaba Star Mandala...")
scene = GeometryScene()
root = scene.root

# Create a central merkaba
merkaba = create_merkaba(radius=1.0)
merkaba_node = GeometryNode("Central Merkaba", merkaba, color='blue', alpha=0.5)
root.add_child(merkaba_node)

# Create a ring of smaller merkabas around it
num_satellites = 6
for i in range(num_satellites):
    angle = i * 2 * np.pi / num_satellites
    x = 3.0 * np.cos(angle)
    y = 3.0 * np.sin(angle)
    z = 0.0
    
    satellite_merkaba = create_merkaba(center=(x, y, z), radius=0.7, rotation=angle)
    satellite_node = GeometryNode(f"Satellite Merkaba {i}", satellite_merkaba, 
                                 color='purple', alpha=0.4)
    root.add_child(satellite_node)

fig = plot_geometry_node(root, title="Merkaba Star Mandala")
save_figure(fig, "merkaba_star_mandala.png")

# 4. Sacred Geometry Tree
print("Creating Sacred Geometry Tree...")
scene = GeometryScene()
root = scene.root

# Create the trunk (cylinder approximated by a stretched cube)
trunk_height = 5.0
trunk = create_cube(center=(0, 0, trunk_height/2), radius=0.5)
# Stretch the cube to make it a cylinder-like trunk
for i in range(len(trunk['vertices'])):
    trunk['vertices'][i][2] *= trunk_height

trunk_node = GeometryNode("Trunk", trunk, color='brown', alpha=0.8)
root.add_child(trunk_node)

# Create the canopy (nested tetrahedra)
canopy_center = (0, 0, trunk_height + 2)
for i in range(3):
    size = 3.0 - i * 0.5
    tetra = create_tetrahedron(center=canopy_center, radius=size)
    tetra_node = GeometryNode(f"Canopy Layer {i}", tetra, 
                             color='green', alpha=0.3 + i * 0.1)
    root.add_child(tetra_node)

# Add some "fruits" (small icosahedra)
for i in range(5):
    angle = i * 2 * np.pi / 5
    radius = 2.0
    x = radius * np.cos(angle)
    y = radius * np.sin(angle)
    z = trunk_height + 2 + np.sin(angle) * 0.5
    
    fruit = create_icosahedron(center=(x, y, z), radius=0.4)
    fruit_node = GeometryNode(f"Fruit {i}", fruit, color='red', alpha=0.7)
    root.add_child(fruit_node)

fig = plot_geometry_node(root, title="Sacred Geometry Tree")
save_figure(fig, "sacred_geometry_tree.png")

# 5. Vector Equilibrium Field
print("Creating Vector Equilibrium Field...")
scene = GeometryScene()
root = scene.root

# Create a 3x3x3 grid of cuboctahedra
grid_size = 3
spacing = 2.5

for x in range(grid_size):
    for y in range(grid_size):
        for z in range(grid_size):
            # Calculate position
            pos_x = (x - (grid_size-1)/2) * spacing
            pos_y = (y - (grid_size-1)/2) * spacing
            pos_z = (z - (grid_size-1)/2) * spacing
            
            # Create cuboctahedron
            cuboct = create_cuboctahedron(center=(pos_x, pos_y, pos_z), radius=0.8)
            
            # Create node with color based on position
            r = x / (grid_size-1)
            g = y / (grid_size-1)
            b = z / (grid_size-1)
            color = (r, g, b)
            
            cuboct_node = GeometryNode(f"Cuboctahedron {x},{y},{z}", 
                                      cuboct, color=color, alpha=0.6)
            root.add_child(cuboct_node)

fig = plot_geometry_node(root, title="Vector Equilibrium Field")
save_figure(fig, "vector_equilibrium_field.png")

# 6. Cosmic Torus Composition
print("Creating Cosmic Torus Composition...")
scene = GeometryScene()
root = scene.root

# Create main torus
torus = create_torus(center=(0, 0, 0), major_radius=3.0, minor_radius=0.5)
torus_node = GeometryNode("Main Torus", torus, color='blue', alpha=0.4)
root.add_child(torus_node)

# Create inner merkaba
merkaba = create_merkaba(center=(0, 0, 0), radius=2.0, rotation=np.pi/4)
merkaba_node = GeometryNode("Inner Merkaba", merkaba, color='purple', alpha=0.5)
root.add_child(merkaba_node)

# Create outer tetrahedron
tetra = create_tetrahedron(center=(0, 0, 0), radius=4.0)
tetra_node = GeometryNode("Outer Tetrahedron", tetra, color='red', alpha=0.2)
root.add_child(tetra_node)

# Create small dodecahedra along the torus
num_points = 12
for i in range(num_points):
    angle = i * 2 * np.pi / num_points
    x = 3.0 * np.cos(angle)
    y = 3.0 * np.sin(angle)
    z = 0.0
    
    dodeca = create_dodecahedron(center=(x, y, z), radius=0.4)
    dodeca_node = GeometryNode(f"Dodecahedron {i}", dodeca, 
                              color='green', alpha=0.6)
    root.add_child(dodeca_node)

fig = plot_geometry_node(root, title="Cosmic Torus Composition")
save_figure(fig, "cosmic_torus.png")

print("\nAll compositions generated successfully!")
