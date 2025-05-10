"""
Script to generate a variety of sacred geometry outputs.
This script creates and saves multiple 2D patterns, 3D shapes, and animations.
"""
import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# Import core 2D pattern generators
from sacred_geometry.core.core import (
    create_flower_of_life, create_metatrons_cube, create_vesica_piscis,
    create_fibonacci_spiral, create_regular_polygon, create_golden_rectangle
)

# Import fractal pattern generators
from sacred_geometry.fractals.fractals import (
    sierpinski_triangle, koch_snowflake, sacred_spiral, fractal_tree,
    recursive_flower_of_life, dragon_curve, hilbert_curve
)

# Import 3D shape generators
from sacred_geometry.shapes.shapes import (
    create_tetrahedron, create_cube, create_octahedron,
    create_icosahedron, create_dodecahedron, create_merkaba,
    create_cuboctahedron, create_flower_of_life_3d, create_torus
)

# Import visualization tools
from sacred_geometry.visualization.visualization import (
    plot_2d_pattern, plot_3d_shape, animate_pattern
)

# Create output directories if they don't exist
output_dirs = {
    '2d': 'outputs/2d',
    '3d': 'outputs/3d',
    'animations': 'outputs/animations',
    'fractals': 'outputs/fractals'
}

for dir_path in output_dirs.values():
    os.makedirs(dir_path, exist_ok=True)

def save_figure(fig, category, filename):
    """Save figure to the appropriate output directory."""
    filepath = os.path.join(output_dirs[category], filename)
    fig.savefig(filepath, dpi=300, bbox_inches='tight')
    print(f"Saved: {filepath}")
    plt.close(fig)

# ===== Generate 2D Patterns =====
print("\nGenerating 2D patterns...")

# Flower of Life with different layers
for layers in [2, 3, 4]:
    flower = create_flower_of_life(center=(0, 0), radius=1.0, layers=layers)
    fig = plot_2d_pattern(
        flower, 
        title=f"Flower of Life (Layers: {layers})", 
        color_scheme="golden",
        figure_size=(10, 10)
    )
    save_figure(fig, '2d', f"flower_of_life_layers_{layers}.png")

# Metatron's Cube
metatron = create_metatrons_cube(center=(0, 0), radius=1.0)
fig = plot_2d_pattern(
    metatron, 
    title="Metatron's Cube", 
    show_points=True,
    color_scheme="rainbow",
    figure_size=(10, 10)
)
save_figure(fig, '2d', "metatrons_cube.png")

# Vesica Piscis
vesica = create_vesica_piscis(center1=(-0.5, 0), center2=(0.5, 0), radius=1.0)
fig = plot_2d_pattern(
    vesica, 
    title="Vesica Piscis", 
    show_points=True,
    color_scheme="monochrome",
    figure_size=(10, 10)
)
save_figure(fig, '2d', "vesica_piscis.png")

# Fibonacci Spiral
fibonacci = create_fibonacci_spiral(center=(0, 0), scale=0.1, n_iterations=10)
fig = plot_2d_pattern(
    fibonacci, 
    title="Fibonacci Spiral", 
    color_scheme="golden",
    figure_size=(10, 10)
)
save_figure(fig, '2d', "fibonacci_spiral.png")

# Regular Polygons
for sides in [3, 5, 6, 7, 9, 12]:
    polygon = create_regular_polygon(center=(0, 0), radius=1.0, sides=sides)
    fig = plot_2d_pattern(
        polygon, 
        title=f"Regular Polygon ({sides} sides)", 
        color_scheme="rainbow",
        figure_size=(8, 8)
    )
    save_figure(fig, '2d', f"polygon_{sides}_sides.png")

# ===== Generate Fractal Patterns =====
print("\nGenerating fractal patterns...")

# Sierpinski Triangle
initial_triangle = np.array([
    [0, 0],
    [1, 0],
    [0.5, np.sqrt(3)/2]
])
for depth in [3, 5, 7]:
    triangles = sierpinski_triangle(initial_triangle, depth)
    
    fig, ax = plt.subplots(figsize=(10, 10))
    ax.set_aspect('equal')
    ax.set_title(f"Sierpinski Triangle (Depth: {depth})")
    
    for triangle in triangles:
        # Close the triangle by repeating the first vertex
        triangle_closed = np.vstack([triangle, triangle[0]])
        ax.plot(triangle_closed[:, 0], triangle_closed[:, 1], 'b-', linewidth=0.5)
    
    ax.set_xlim(-0.1, 1.1)
    ax.set_ylim(-0.1, 1.0)
    plt.tight_layout()
    save_figure(fig, 'fractals', f"sierpinski_depth_{depth}.png")

# Koch Snowflake
initial_hexagon = create_regular_polygon(center=(0, 0), radius=1.0, sides=6)
for depth in [1, 2, 3, 4]:
    snowflake = koch_snowflake(initial_hexagon, depth)
    
    fig, ax = plt.subplots(figsize=(10, 10))
    ax.set_aspect('equal')
    ax.set_title(f"Koch Snowflake (Depth: {depth})")
    
    # Close the curve by repeating the first vertex
    snowflake_closed = np.vstack([snowflake, snowflake[0]])
    ax.plot(snowflake_closed[:, 0], snowflake_closed[:, 1], 'b-', linewidth=1)
    
    ax.set_xlim(-1.5, 1.5)
    ax.set_ylim(-1.5, 1.5)
    plt.tight_layout()
    save_figure(fig, 'fractals', f"koch_snowflake_depth_{depth}.png")

# Sacred Spiral
spiral = sacred_spiral(
    center=(0, 0), 
    start_radius=0.1, 
    max_radius=5.0, 
    turns=8,
    points_per_turn=100
)

fig, ax = plt.subplots(figsize=(10, 10))
ax.set_aspect('equal')
ax.set_title("Sacred Spiral (Golden Ratio)")
ax.plot(spiral[:, 0], spiral[:, 1], 'r-', linewidth=2)
ax.set_xlim(-5.5, 5.5)
ax.set_ylim(-5.5, 5.5)
plt.tight_layout()
save_figure(fig, 'fractals', "sacred_spiral.png")

# Fractal Tree
tree_branches = fractal_tree(
    start=(0, -3), 
    angle=np.pi/2,  # Initial angle (pointing up)
    length=2.0,     # Initial branch length
    depth=7,        # Recursion depth
    length_factor=0.7,
    angle_delta=np.pi/7
)

fig, ax = plt.subplots(figsize=(10, 10))
ax.set_aspect('equal')
ax.set_title("Fractal Tree")

for branch in tree_branches:
    ax.plot(branch[:, 0], branch[:, 1], 'brown', linewidth=1)

ax.set_xlim(-5, 5)
ax.set_ylim(-3, 5)
plt.tight_layout()
save_figure(fig, 'fractals', "fractal_tree.png")

# ===== Generate 3D Shapes =====
print("\nGenerating 3D shapes...")

# Platonic Solids
platonic_solids = {
    'tetrahedron': create_tetrahedron,
    'cube': create_cube,
    'octahedron': create_octahedron,
    'icosahedron': create_icosahedron,
    'dodecahedron': create_dodecahedron
}

for name, creator_func in platonic_solids.items():
    shape = creator_func(center=(0, 0, 0), radius=1.0)
    fig = plot_3d_shape(
        shape,
        title=f"{name.capitalize()}",
        color_scheme="rainbow",
        alpha=0.7,
        show_edges=True,
        show_vertices=True,
        figure_size=(10, 10)
    )
    save_figure(fig, '3d', f"{name}.png")

# Merkaba with different rotations
for rotation, rot_name in [(0, "0"), (np.pi/6, "pi_6"), (np.pi/4, "pi_4")]:
    merkaba = create_merkaba(center=(0, 0, 0), radius=1.0, rotation=rotation)
    fig = plot_3d_shape(
        merkaba,
        title=f"Merkaba (Rotation: {rot_name})",
        color_scheme="rainbow",
        alpha=0.7,
        show_edges=True,
        show_vertices=True,
        figure_size=(10, 10)
    )
    save_figure(fig, '3d', f"merkaba_rotation_{rot_name}.png")

# Vector Equilibrium (Cuboctahedron)
cuboctahedron = create_cuboctahedron(center=(0, 0, 0), radius=1.0)
fig = plot_3d_shape(
    cuboctahedron,
    title="Vector Equilibrium (Cuboctahedron)",
    color_scheme="rainbow",
    alpha=0.7,
    show_edges=True,
    show_vertices=True,
    figure_size=(10, 10)
)
save_figure(fig, '3d', "vector_equilibrium.png")

# Torus
torus = create_torus(
    center=(0, 0, 0),
    major_radius=2.0,
    minor_radius=0.5,
    num_major_segments=48,
    num_minor_segments=24
)
fig = plot_3d_shape(
    torus,
    title="Torus",
    color_scheme="rainbow",
    alpha=0.7,
    show_edges=False,
    show_vertices=False,
    figure_size=(10, 10)
)
save_figure(fig, '3d', "torus.png")

print("\nAll outputs generated successfully!")
