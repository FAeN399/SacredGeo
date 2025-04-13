"""
Example script demonstrating animations of sacred geometry patterns.
"""
import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from sacred_geometry.core.core import (
    create_flower_of_life, create_fibonacci_spiral, create_metatrons_cube
)
from sacred_geometry.fractals.fractals import (
    sacred_spiral, koch_snowflake
)
from sacred_geometry.visualization.visualization import animate_pattern

# Create output directory if it doesn't exist
output_dir = "examples/outputs/animations"
os.makedirs(output_dir, exist_ok=True)

# Example 1: Animated Flower of Life (growing layers)
def animate_flower_growth(num_frames=60):
    """Animate the growth of a Flower of Life pattern."""
    fig, ax = plt.subplots(figsize=(10, 10))
    ax.set_aspect('equal')
    ax.set_title("Growing Flower of Life")
    ax.set_xlim(-4, 4)
    ax.set_ylim(-4, 4)
    ax.grid(True, linestyle='--', alpha=0.7)
    
    # Animation function
    def update(frame):
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
        fig, update, frames=num_frames, interval=50, blit=False
    )
    
    # Save the animation
    filename = os.path.join(output_dir, "flower_of_life_growth.gif")
    anim.save(filename, writer='pillow', fps=15)
    print(f"Saved: {filename}")
    plt.close(fig)

# Example 2: Animated Sacred Spiral (unwinding)
def animate_sacred_spiral(num_frames=60):
    """Animate the unwinding of a sacred spiral based on golden ratio."""
    fig, ax = plt.subplots(figsize=(10, 10))
    ax.set_aspect('equal')
    ax.set_title("Sacred Spiral (Golden Ratio)")
    ax.set_xlim(-6, 6)
    ax.set_ylim(-6, 6)
    ax.grid(True, linestyle='--', alpha=0.7)
    
    # Animation function
    def update(frame):
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
        fig, update, frames=num_frames, interval=50, blit=False
    )
    
    # Save the animation
    filename = os.path.join(output_dir, "sacred_spiral.gif")
    anim.save(filename, writer='pillow', fps=15)
    print(f"Saved: {filename}")
    plt.close(fig)

# Example 3: Animated Metatron's Cube with rotation
def animate_metatrons_cube(num_frames=90):
    """Animate Metatron's Cube with rotation."""
    fig, ax = plt.subplots(figsize=(10, 10))
    ax.set_aspect('equal')
    ax.set_title("Rotating Metatron's Cube")
    ax.set_xlim(-4, 4)
    ax.set_ylim(-4, 4)
    ax.grid(True, linestyle='--', alpha=0.7)
    
    # Animation function
    def update(frame):
        ax.clear()
        ax.set_aspect('equal')
        ax.set_title("Rotating Metatron's Cube")
        ax.set_xlim(-4, 4)
        ax.set_ylim(-4, 4)
        ax.grid(True, linestyle='--', alpha=0.7)
        
        # Calculate rotation angle based on frame
        angle = frame / num_frames * 2 * np.pi
        
        # Generate the base Metatron's Cube
        cube = create_metatrons_cube(center=(0, 0), radius=1.0)
        
        # Apply rotation to all vertices and lines
        rotated_vertices = []
        for vertex in cube['vertices']:
            x, y = vertex
            # Apply rotation
            new_x = x * np.cos(angle) - y * np.sin(angle)
            new_y = x * np.sin(angle) + y * np.cos(angle)
            rotated_vertices.append((new_x, new_y))
        
        rotated_lines = []
        for line in cube['lines']:
            v1_idx = cube['vertices'].index(line[0])
            v2_idx = cube['vertices'].index(line[1])
            rotated_lines.append((rotated_vertices[v1_idx], rotated_vertices[v2_idx]))
        
        # Plot the circles and lines
        for circle in cube['circles']:
            # Rotate each point in the circle
            rotated_circle = np.zeros_like(circle)
            for i, point in enumerate(circle):
                rotated_circle[i, 0] = point[0] * np.cos(angle) - point[1] * np.sin(angle)
                rotated_circle[i, 1] = point[0] * np.sin(angle) + point[1] * np.cos(angle)
            ax.plot(rotated_circle[:, 0], rotated_circle[:, 1], 'b-', alpha=0.2)
        
        # Plot the lines
        for line in rotated_lines:
            ax.plot([line[0][0], line[1][0]], [line[0][1], line[1][1]], 
                   'r-', linewidth=0.8, alpha=0.7)
        
        # Plot the vertices
        vertices_array = np.array(rotated_vertices)
        ax.scatter(vertices_array[:, 0], vertices_array[:, 1], 
                 color='blue', s=30, alpha=0.8)
        
        return ax,
    
    # Create the animation
    anim = animation.FuncAnimation(
        fig, update, frames=num_frames, interval=50, blit=False
    )
    
    # Save the animation
    filename = os.path.join(output_dir, "metatrons_cube_rotation.gif")
    anim.save(filename, writer='pillow', fps=20)
    print(f"Saved: {filename}")
    plt.close(fig)

# Example 4: Koch Snowflake Evolution
def animate_koch_snowflake(num_frames=6, frame_duration=1000):
    """Animate the evolution of a Koch Snowflake."""
    fig, ax = plt.subplots(figsize=(10, 10))
    ax.set_aspect('equal')
    ax.set_title("Koch Snowflake Evolution")
    ax.set_xlim(-1.5, 1.5)
    ax.set_ylim(-1.5, 1.5)
    ax.grid(True, linestyle='--', alpha=0.7)
    
    # Create initial triangle
    side_length = 2.0
    height = side_length * np.sqrt(3) / 2
    initial_points = np.array([
        [0, height/2],
        [-side_length/2, -height/2],
        [side_length/2, -height/2]
    ])
    
    # Animation function
    def update(frame):
        ax.clear()
        ax.set_aspect('equal')
        ax.set_title(f"Koch Snowflake - Iteration {frame}")
        ax.set_xlim(-1.5, 1.5)
        ax.set_ylim(-1.5, 1.5)
        ax.grid(True, linestyle='--', alpha=0.7)
        
        # Generate Koch snowflake at current iteration
        snowflake = koch_snowflake(initial_points, depth=frame)
        
        # Plot the snowflake
        x = np.append(snowflake[:, 0], snowflake[0, 0])
        y = np.append(snowflake[:, 1], snowflake[0, 1])
        ax.plot(x, y, 'b-', linewidth=1)
        
        return ax,
    
    # Create the animation
    anim = animation.FuncAnimation(
        fig, update, frames=num_frames, interval=frame_duration, blit=False
    )
    
    # Save the animation
    filename = os.path.join(output_dir, "koch_snowflake_evolution.gif")
    anim.save(filename, writer='pillow', fps=1)
    print(f"Saved: {filename}")
    plt.close(fig)

# Run the animations
if __name__ == "__main__":
    print("Generating sacred geometry animations...")
    animate_flower_growth()
    animate_sacred_spiral()
    animate_metatrons_cube()
    animate_koch_snowflake()
    print("All animations generated successfully.")