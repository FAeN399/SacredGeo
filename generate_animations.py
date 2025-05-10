"""
Script to generate sacred geometry animations.
This script creates and saves various animated patterns and shapes.
"""
import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# Import core 2D pattern generators
from sacred_geometry.core.core import (
    create_flower_of_life, create_fibonacci_spiral, create_metatrons_cube,
    create_regular_polygon
)

# Import fractal pattern generators
from sacred_geometry.fractals.fractals import (
    sacred_spiral, koch_snowflake
)

# Import 3D shape generators
from sacred_geometry.shapes.shapes import (
    create_merkaba, create_cuboctahedron, create_tetrahedron
)

# Import visualization tools
from sacred_geometry.visualization.visualization import animate_pattern

# Create output directory if it doesn't exist
output_dir = "outputs/animations"
os.makedirs(output_dir, exist_ok=True)

# ===== Generate Animations =====
print("\nGenerating animations...")

# 1. Growing Flower of Life Animation
print("Creating Flower of Life animation...")
num_frames = 60

fig, ax = plt.subplots(figsize=(10, 10))
ax.set_aspect('equal')

# Animation function
def update_flower(frame):
    ax.clear()
    ax.set_aspect('equal')
    ax.set_title("Growing Flower of Life")
    ax.set_xlim(-4, 4)
    ax.set_ylim(-4, 4)
    ax.grid(True, linestyle='--', alpha=0.7)

    # Calculate layer based on frame
    layer = 1 + int(frame / num_frames * 3)

    # Generate the flower of life with appropriate layer
    flower = create_flower_of_life(center=(0, 0), radius=1.0, layers=layer)

    # Plot each circle
    for i, circle in enumerate(flower):
        alpha = min(1.0, (frame / (num_frames / 3)) - i * 0.05)
        if alpha > 0:
            ax.plot(circle[:, 0], circle[:, 1], 'b-', alpha=alpha)

    return ax,

# Create the animation
anim = animation.FuncAnimation(
    fig, update_flower, frames=num_frames, interval=50, blit=False
)

# Save the animation
filename = os.path.join(output_dir, "flower_of_life_growing.gif")
anim.save(filename, writer='pillow', fps=15)
print(f"Saved: {filename}")
plt.close(fig)

# 2. Sacred Spiral Animation
print("Creating Sacred Spiral animation...")
num_frames = 60

fig, ax = plt.subplots(figsize=(10, 10))
ax.set_aspect('equal')

# Animation function
def update_spiral(frame):
    ax.clear()
    ax.set_aspect('equal')
    ax.set_title("Sacred Spiral (Golden Ratio)")
    ax.set_xlim(-6, 6)
    ax.set_ylim(-6, 6)
    ax.grid(True, linestyle='--', alpha=0.7)

    # Calculate turns based on frame
    turns = (frame + 1) / num_frames * 8

    # Generate the spiral
    spiral = sacred_spiral(
        center=(0, 0),
        start_radius=0.1,
        max_radius=5.5,
        turns=turns,
        points_per_turn=100
    )

    # Plot the spiral
    ax.plot(spiral[:, 0], spiral[:, 1], 'r-', linewidth=2)

    return ax,

# Create the animation
anim = animation.FuncAnimation(
    fig, update_spiral, frames=num_frames, interval=50, blit=False
)

# Save the animation
filename = os.path.join(output_dir, "sacred_spiral.gif")
anim.save(filename, writer='pillow', fps=15)
print(f"Saved: {filename}")
plt.close(fig)

# 3. Rotating Merkaba Animation
print("Creating Rotating Merkaba animation...")
num_frames = 60

fig = plt.figure(figsize=(10, 10))
ax = fig.add_subplot(111, projection='3d')

# Animation function
def update_merkaba(frame):
    ax.clear()
    ax.set_title("Rotating Merkaba")

    # Calculate rotation based on frame
    rotation = frame / num_frames * 2 * np.pi

    # Create merkaba with current rotation
    merkaba = create_merkaba(center=(0, 0, 0), radius=1.0, rotation=rotation)

    # Plot first tetrahedron
    tetra1 = merkaba['tetrahedron1']
    vertices1 = tetra1['vertices']
    faces1 = tetra1['faces']

    # Create face collections for both tetrahedra
    for i, (tetra_key, color) in enumerate([('tetrahedron1', 'blue'), ('tetrahedron2', 'red')]):
        tetra = merkaba[tetra_key]
        vertices = tetra['vertices']
        faces = tetra['faces']

        # Create the collection of polygons
        face_collection = []
        for face in faces:
            face_vertices = [vertices[i] for i in face]
            face_collection.append(face_vertices)

        # Add the collection to the plot using Poly3DCollection
        from mpl_toolkits.mplot3d.art3d import Poly3DCollection
        poly = Poly3DCollection(face_collection, alpha=0.4)
        poly.set_color(color)
        ax.add_collection3d(poly)

        # Plot edges
        for edge in tetra['edges']:
            v1, v2 = edge
            ax.plot([vertices[v1][0], vertices[v2][0]],
                   [vertices[v1][1], vertices[v2][1]],
                   [vertices[v1][2], vertices[v2][2]],
                   'k-', linewidth=1)

    # Set axis limits
    ax.set_xlim(-1.5, 1.5)
    ax.set_ylim(-1.5, 1.5)
    ax.set_zlim(-1.5, 1.5)

    # Set equal aspect ratio
    ax.set_box_aspect([1, 1, 1])

    return ax,

# Create the animation
anim = animation.FuncAnimation(
    fig, update_merkaba, frames=num_frames, interval=50, blit=False
)

# Save the animation
filename = os.path.join(output_dir, "rotating_merkaba.gif")
anim.save(filename, writer='pillow', fps=15)
print(f"Saved: {filename}")
plt.close(fig)

# 4. Metatron's Cube Animation
print("Creating Metatron's Cube animation...")
num_frames = 60

fig, ax = plt.subplots(figsize=(10, 10))
ax.set_aspect('equal')

# Animation function
def update_metatron(frame):
    ax.clear()
    ax.set_aspect('equal')
    ax.set_title("Metatron's Cube Formation")
    ax.set_xlim(-3, 3)
    ax.set_ylim(-3, 3)
    ax.grid(True, linestyle='--', alpha=0.7)

    # Create Metatron's Cube
    metatron = create_metatrons_cube(center=(0, 0), radius=1.0)

    # Draw circles with growing opacity
    for i, circle in enumerate(metatron['circles']):
        alpha = min(1.0, frame / (num_frames * 0.5) - i * 0.05)
        if alpha > 0:
            ax.plot(circle[:, 0], circle[:, 1], 'b-', alpha=alpha)

    # Draw lines with growing opacity
    if frame > num_frames * 0.5:
        line_alpha = min(1.0, (frame - num_frames * 0.5) / (num_frames * 0.5))
        for line in metatron['lines']:
            ax.plot([line[0][0], line[1][0]], [line[0][1], line[1][1]],
                  'r-', linewidth=1, alpha=line_alpha)

    return ax,

# Create the animation
anim = animation.FuncAnimation(
    fig, update_metatron, frames=num_frames, interval=50, blit=False
)

# Save the animation
filename = os.path.join(output_dir, "metatrons_cube.gif")
anim.save(filename, writer='pillow', fps=15)
print(f"Saved: {filename}")
plt.close(fig)

# 5. Koch Snowflake Evolution Animation
print("Creating Koch Snowflake animation...")
num_frames = 60

fig, ax = plt.subplots(figsize=(10, 10))
ax.set_aspect('equal')

# Animation function
def update_koch(frame):
    ax.clear()
    ax.set_aspect('equal')
    ax.set_title("Koch Snowflake Evolution")
    ax.set_xlim(-1.5, 1.5)
    ax.set_ylim(-1.5, 1.5)
    ax.grid(True, linestyle='--', alpha=0.7)

    # Calculate depth based on frame
    # We'll transition between depths 0, 1, 2, 3, 4
    depth = min(4, int(frame / (num_frames / 5)))

    # Create initial hexagon
    initial_hexagon = create_regular_polygon(center=(0, 0), radius=1.0, sides=6)

    # Generate Koch snowflake
    snowflake = koch_snowflake(initial_hexagon, depth)

    # Close the curve by repeating the first vertex
    snowflake_closed = np.vstack([snowflake, snowflake[0]])

    # Plot the snowflake
    ax.plot(snowflake_closed[:, 0], snowflake_closed[:, 1], 'b-', linewidth=1)

    return ax,

# Create the animation
anim = animation.FuncAnimation(
    fig, update_koch, frames=num_frames, interval=50, blit=False
)

# Save the animation
filename = os.path.join(output_dir, "koch_snowflake.gif")
anim.save(filename, writer='pillow', fps=15)
print(f"Saved: {filename}")
plt.close(fig)

print("\nAll animations generated successfully!")
