"""
Example script demonstrating 3D sacred geometry shapes.
"""
import os
import numpy as np
import matplotlib.pyplot as plt
from sacred_geometry.shapes.shapes import (
    create_tetrahedron, create_cube, create_octahedron,
    create_icosahedron, create_dodecahedron, create_merkaba,
    create_cuboctahedron, create_flower_of_life_3d, create_torus
)
from sacred_geometry.visualization.visualization import plot_3d_shape

# Create output directory if it doesn't exist
output_dir = "examples/outputs/3d"
os.makedirs(output_dir, exist_ok=True)

def save_figure(fig, filename):
    """Save figure to the output directory."""
    filepath = os.path.join(output_dir, filename)
    fig.savefig(filepath, dpi=300, bbox_inches='tight')
    print(f"Saved: {filepath}")
    plt.close(fig)

# Example 1: Platonic Solids
shapes = {
    "tetrahedron": create_tetrahedron(center=(0, 0, 0), radius=1.0),
    "cube": create_cube(center=(0, 0, 0), radius=1.0),
    "octahedron": create_octahedron(center=(0, 0, 0), radius=1.0),
    "icosahedron": create_icosahedron(center=(0, 0, 0), radius=1.0),
    "dodecahedron": create_dodecahedron(center=(0, 0, 0), radius=1.0)
}

for name, shape in shapes.items():
    fig = plot_3d_shape(
        shape,
        title=f"Platonic Solid: {name.capitalize()}",
        color_scheme="rainbow",
        alpha=0.7,
        show_edges=True,
        show_vertices=True,
        figure_size=(10, 10)
    )
    save_figure(fig, f"platonic_{name}.png")

# Example 2: Merkaba (Star Tetrahedron)
merkaba = create_merkaba(center=(0, 0, 0), radius=1.0, rotation=np.pi/5)
fig = plot_3d_shape(
    merkaba,
    title="Merkaba (Star Tetrahedron)",
    color_scheme="rainbow",
    alpha=0.6,
    show_edges=True,
    show_vertices=True,
    figure_size=(10, 10)
)
save_figure(fig, "merkaba.png")

# Example 3: Vector Equilibrium (Cuboctahedron)
cuboctahedron = create_cuboctahedron(center=(0, 0, 0), radius=1.0)
fig = plot_3d_shape(
    cuboctahedron,
    title="Vector Equilibrium (Cuboctahedron)",
    color_scheme="golden",
    alpha=0.7,
    show_edges=True,
    show_vertices=True,
    figure_size=(10, 10)
)
save_figure(fig, "vector_equilibrium.png")

# Example 4: 3D Flower of Life
flower_3d = create_flower_of_life_3d(center=(0, 0, 0), radius=0.5, layers=2)
fig = plot_3d_shape(
    flower_3d,
    title="3D Flower of Life",
    color_scheme="rainbow",
    alpha=0.3,
    show_edges=False,
    show_vertices=False,
    figure_size=(10, 10)
)
save_figure(fig, "flower_of_life_3d.png")

# Example 5: Torus
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
save_figure(fig, "torus.png")

print("All 3D examples generated successfully.")