"""
Script to generate custom sacred geometry outputs.
This script creates unique combinations and variations of sacred geometry patterns.
"""
import os
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap

# Import core 2D pattern generators
from sacred_geometry.core.core import (
    create_flower_of_life, create_metatrons_cube, create_vesica_piscis,
    create_fibonacci_spiral, create_regular_polygon, get_golden_ratio
)

# Import fractal pattern generators
from sacred_geometry.fractals.fractals import (
    sierpinski_triangle, koch_snowflake, sacred_spiral, fractal_tree,
    recursive_flower_of_life, dragon_curve
)

# Import 3D shape generators
from sacred_geometry.shapes.shapes import (
    create_tetrahedron, create_cube, create_octahedron,
    create_icosahedron, create_dodecahedron, create_merkaba,
    create_cuboctahedron, create_flower_of_life_3d, create_torus
)

# Import visualization tools
from sacred_geometry.visualization.visualization import (
    plot_2d_pattern, plot_3d_shape
)

# Create output directory if it doesn't exist
output_dir = "outputs/custom"
os.makedirs(output_dir, exist_ok=True)

def save_figure(fig, filename):
    """Save figure to the output directory."""
    filepath = os.path.join(output_dir, filename)
    fig.savefig(filepath, dpi=300, bbox_inches='tight')
    print(f"Saved: {filepath}")
    plt.close(fig)

# ===== Generate Custom Outputs =====
print("\nGenerating custom outputs...")

# 1. Flower of Life with Fibonacci Spiral Overlay
print("Creating Flower of Life with Fibonacci Spiral...")

# Create figure and axis
fig, ax = plt.subplots(figsize=(12, 12))
ax.set_aspect('equal')
ax.set_title("Flower of Life with Fibonacci Spiral", fontsize=16)

# Create Flower of Life
flower = create_flower_of_life(center=(0, 0), radius=1.0, layers=3)
for circle in flower:
    ax.plot(circle[:, 0], circle[:, 1], 'b-', alpha=0.3, linewidth=1)

# Create Fibonacci Spiral
fibonacci = create_fibonacci_spiral(center=(0, 0), scale=0.1, n_iterations=10)
ax.plot(fibonacci['spiral'][:, 0], fibonacci['spiral'][:, 1], 'r-', linewidth=2)

# Set limits and grid
ax.set_xlim(-4, 4)
ax.set_ylim(-4, 4)
ax.grid(True, linestyle='--', alpha=0.3)

# Save the figure
save_figure(fig, "flower_of_life_with_fibonacci.png")

# 2. Sacred Geometry Mandala
print("Creating Sacred Geometry Mandala...")

# Create figure and axis
fig, ax = plt.subplots(figsize=(12, 12))
ax.set_aspect('equal')
ax.set_title("Sacred Geometry Mandala", fontsize=16)

# Create multiple layers of polygons with different rotations
phi = get_golden_ratio()
colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b']

# Layer 1: Hexagon
hexagon = create_regular_polygon(center=(0, 0), radius=3.0, sides=6)
ax.plot(np.append(hexagon[:, 0], hexagon[0, 0]), 
       np.append(hexagon[:, 1], hexagon[0, 1]), 
       '-', color=colors[0], linewidth=2)

# Layer 2: Pentagon
pentagon = create_regular_polygon(center=(0, 0), radius=2.5, sides=5, rotation=np.pi/5)
ax.plot(np.append(pentagon[:, 0], pentagon[0, 0]), 
       np.append(pentagon[:, 1], pentagon[0, 1]), 
       '-', color=colors[1], linewidth=2)

# Layer 3: Heptagon (7 sides)
heptagon = create_regular_polygon(center=(0, 0), radius=2.0, sides=7, rotation=np.pi/7)
ax.plot(np.append(heptagon[:, 0], heptagon[0, 0]), 
       np.append(heptagon[:, 1], heptagon[0, 1]), 
       '-', color=colors[2], linewidth=2)

# Layer 4: Triangle
triangle = create_regular_polygon(center=(0, 0), radius=1.5, sides=3, rotation=np.pi/6)
ax.plot(np.append(triangle[:, 0], triangle[0, 0]), 
       np.append(triangle[:, 1], triangle[0, 1]), 
       '-', color=colors[3], linewidth=2)

# Layer 5: Square
square = create_regular_polygon(center=(0, 0), radius=1.0, sides=4, rotation=np.pi/4)
ax.plot(np.append(square[:, 0], square[0, 0]), 
       np.append(square[:, 1], square[0, 1]), 
       '-', color=colors[4], linewidth=2)

# Layer 6: Center circle
circle = create_regular_polygon(center=(0, 0), radius=0.5, sides=36)
ax.plot(np.append(circle[:, 0], circle[0, 0]), 
       np.append(circle[:, 1], circle[0, 1]), 
       '-', color=colors[5], linewidth=2)

# Add connecting lines
for i in range(6):
    angle = i * np.pi / 3
    x = 3.0 * np.cos(angle)
    y = 3.0 * np.sin(angle)
    ax.plot([0, x], [0, y], 'k-', alpha=0.5, linewidth=1)

# Set limits and remove axes
ax.set_xlim(-3.5, 3.5)
ax.set_ylim(-3.5, 3.5)
ax.axis('off')

# Save the figure
save_figure(fig, "sacred_geometry_mandala.png")

# 3. Metatron's Cube with Platonic Solids Projection
print("Creating Metatron's Cube with Platonic Solids Projection...")

# Create figure and axis
fig, ax = plt.subplots(figsize=(12, 12))
ax.set_aspect('equal')
ax.set_title("Metatron's Cube with Platonic Solids Projection", fontsize=16)

# Create Metatron's Cube
metatron = create_metatrons_cube(center=(0, 0), radius=1.0)

# Draw circles
for circle in metatron['circles']:
    ax.plot(circle[:, 0], circle[:, 1], 'b-', alpha=0.3, linewidth=1)

# Draw lines
for line in metatron['lines']:
    ax.plot([line[0][0], line[1][0]], [line[0][1], line[1][1]], 
          'k-', linewidth=0.5, alpha=0.7)

# Draw vertices
vertices = np.array(metatron['vertices'])
ax.scatter(vertices[:, 0], vertices[:, 1], color='red', s=30)

# Project platonic solids onto the 2D plane
# Tetrahedron projection (simplified)
tetra_edges = [(0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3)]
for edge in tetra_edges:
    if edge[0] < len(vertices) and edge[1] < len(vertices):
        ax.plot([vertices[edge[0], 0], vertices[edge[1], 0]],
               [vertices[edge[0], 1], vertices[edge[1], 1]],
               'r-', linewidth=1.5, alpha=0.7)

# Cube projection (simplified)
cube_edges = [(1, 2), (1, 3), (2, 4), (3, 4), (5, 6), (5, 7), (6, 8), (7, 8)]
for edge in cube_edges:
    if edge[0] < len(vertices) and edge[1] < len(vertices):
        ax.plot([vertices[edge[0], 0], vertices[edge[1], 0]],
               [vertices[edge[0], 1], vertices[edge[1], 1]],
               'g-', linewidth=1.5, alpha=0.7)

# Set limits and grid
ax.set_xlim(-3, 3)
ax.set_ylim(-3, 3)
ax.grid(True, linestyle='--', alpha=0.3)

# Save the figure
save_figure(fig, "metatrons_cube_with_platonic_projections.png")

# 4. Fractal Tree with Golden Ratio Proportions
print("Creating Fractal Tree with Golden Ratio Proportions...")

# Create figure and axis
fig, ax = plt.subplots(figsize=(12, 12))
ax.set_aspect('equal')
ax.set_title("Fractal Tree with Golden Ratio Proportions", fontsize=16)

# Golden ratio
phi = get_golden_ratio()

# Create a fractal tree with golden ratio proportions
tree_branches = fractal_tree(
    start=(0, -3), 
    angle=np.pi/2,  # Initial angle (pointing up)
    length=3.0,     # Initial branch length
    depth=8,        # Recursion depth
    length_factor=1/phi,  # Golden ratio reduction
    angle_delta=np.pi/phi  # Golden angle
)

# Create a custom colormap for the branches
colors = [(0.6, 0.3, 0.1), (0.2, 0.8, 0.2)]  # Brown to green
cmap = LinearSegmentedColormap.from_list("BrownToGreen", colors, N=len(tree_branches))

# Plot each branch with a color based on its depth
for i, branch in enumerate(tree_branches):
    color = cmap(i / len(tree_branches))
    ax.plot(branch[:, 0], branch[:, 1], color=color, linewidth=max(0.5, 3 * (1 - i/len(tree_branches))))

# Set limits and remove axes
ax.set_xlim(-5, 5)
ax.set_ylim(-3, 7)
ax.axis('off')

# Save the figure
save_figure(fig, "golden_ratio_fractal_tree.png")

print("\nAll custom outputs generated successfully!")
