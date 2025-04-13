"""
Example script demonstrating 2D sacred geometry patterns.
"""
import os
import numpy as np
import matplotlib.pyplot as plt
from sacred_geometry.core.core import (
    create_circle, create_regular_polygon, create_flower_of_life,
    create_metatrons_cube, create_vesica_piscis, create_fibonacci_spiral
)
from sacred_geometry.fractals.fractals import (
    sierpinski_triangle, koch_snowflake, sacred_spiral, fractal_tree
)
from sacred_geometry.visualization.visualization import plot_2d_pattern

# Create output directory if it doesn't exist
output_dir = "examples/outputs/2d"
os.makedirs(output_dir, exist_ok=True)

def save_figure(fig, filename):
    """Save figure to the output directory."""
    filepath = os.path.join(output_dir, filename)
    fig.savefig(filepath, dpi=300, bbox_inches='tight')
    print(f"Saved: {filepath}")
    plt.close(fig)

# Example 1: Flower of Life
flower = create_flower_of_life(center=(0, 0), radius=1.0, layers=3)
fig = plot_2d_pattern(
    flower, 
    title="Flower of Life", 
    color_scheme="golden",
    figure_size=(10, 10)
)
save_figure(fig, "flower_of_life.png")

# Example 2: Metatron's Cube
metatron = create_metatrons_cube(center=(0, 0), radius=1.0)
fig = plot_2d_pattern(
    metatron, 
    title="Metatron's Cube", 
    show_points=True,
    color_scheme="rainbow",
    figure_size=(10, 10)
)
save_figure(fig, "metatrons_cube.png")

# Example 3: Vesica Piscis
vesica = create_vesica_piscis(center1=(-0.5, 0), center2=(0.5, 0), radius=1.0)
fig = plot_2d_pattern(
    vesica, 
    title="Vesica Piscis", 
    show_points=True,
    color_scheme="monochrome",
    figure_size=(10, 10)
)
save_figure(fig, "vesica_piscis.png")

# Example 4: Fibonacci Spiral
fibonacci = create_fibonacci_spiral(center=(0, 0), scale=0.1, n_iterations=10)
fig = plot_2d_pattern(
    fibonacci, 
    title="Fibonacci Spiral", 
    color_scheme="golden",
    figure_size=(10, 10)
)
save_figure(fig, "fibonacci_spiral.png")

# Example 5: Sierpinski Triangle
# Create an equilateral triangle
points = np.array([
    [0, np.sqrt(3)],
    [-1, 0],
    [1, 0]
])
sierpinski = sierpinski_triangle(points, depth=5)

fig, ax = plt.subplots(figsize=(10, 10))
ax.set_aspect('equal')
ax.set_title("Sierpinski Triangle")

for triangle in sierpinski:
    # Close the triangle by repeating the first point
    x = np.append(triangle[:, 0], triangle[0, 0])
    y = np.append(triangle[:, 1], triangle[0, 1])
    ax.plot(x, y, 'b-', linewidth=0.5)

ax.set_xlim(-1.5, 1.5)
ax.set_ylim(-0.5, 2)
plt.tight_layout()
save_figure(fig, "sierpinski_triangle.png")

# Example 6: Koch Snowflake
# Start with an equilateral triangle
side_length = 2.0
height = side_length * np.sqrt(3) / 2
koch_points = np.array([
    [0, height/2],
    [-side_length/2, -height/2],
    [side_length/2, -height/2]
])
koch = koch_snowflake(koch_points, depth=4)

fig, ax = plt.subplots(figsize=(10, 10))
ax.set_aspect('equal')
ax.set_title("Koch Snowflake")

# Plot the snowflake
x = np.append(koch[:, 0], koch[0, 0])
y = np.append(koch[:, 1], koch[0, 1])
ax.plot(x, y, 'b-', linewidth=1)

ax.set_xlim(-1.5, 1.5)
ax.set_ylim(-1.5, 1.5)
plt.tight_layout()
save_figure(fig, "koch_snowflake.png")

# Example 7: Sacred Spiral
spiral = sacred_spiral(center=(0, 0), start_radius=0.1, max_radius=5.0, turns=7)

fig, ax = plt.subplots(figsize=(10, 10))
ax.set_aspect('equal')
ax.set_title("Sacred Spiral (Golden Ratio)")

ax.plot(spiral[:, 0], spiral[:, 1], 'r-', linewidth=1.5)
ax.set_xlim(-5.5, 5.5)
ax.set_ylim(-5.5, 5.5)
plt.tight_layout()
save_figure(fig, "sacred_spiral.png")

# Example 8: Fractal Tree
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
save_figure(fig, "fractal_tree.png")

print("All 2D examples generated successfully.")