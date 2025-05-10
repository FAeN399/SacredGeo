#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Basic usage examples for the Sacred Geometry package.

This script demonstrates how to create and visualize various sacred geometry
patterns and shapes using the package.
"""

import os
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# Import sacred geometry modules
from sacred_geometry.core.core import (
    create_flower_of_life,
    create_seed_of_life,
    create_metatrons_cube,
    create_vesica_piscis,
    create_fibonacci_spiral,
    create_regular_polygon,
    create_golden_rectangle,
    get_golden_ratio
)

from sacred_geometry.shapes.shapes import (
    create_tetrahedron,
    create_cube,
    create_octahedron,
    create_icosahedron,
    create_dodecahedron,
    create_merkaba,
    create_cuboctahedron,
    create_flower_of_life_3d,
    create_torus
)

from sacred_geometry.visualization.visualization import (
    plot_2d_pattern,
    plot_3d_shape
)

# Create output directory if it doesn't exist
os.makedirs('outputs/examples', exist_ok=True)

def example_2d_patterns():
    """Example of creating and visualizing 2D sacred geometry patterns."""
    # Create a figure with subplots
    fig, axs = plt.subplots(2, 3, figsize=(15, 10))
    axs = axs.flatten()
    
    # 1. Flower of Life
    flower = create_flower_of_life(center=(0, 0), radius=1.0, layers=3)
    plot_2d_pattern(flower, ax=axs[0], color_scheme='golden')
    axs[0].set_title('Flower of Life')
    
    # 2. Seed of Life
    seed = create_seed_of_life(center=(0, 0), radius=1.0)
    plot_2d_pattern(seed, ax=axs[1], color_scheme='rainbow')
    axs[1].set_title('Seed of Life')
    
    # 3. Metatron's Cube
    metatron = create_metatrons_cube(center=(0, 0), radius=1.0)
    plot_2d_pattern(metatron, ax=axs[2], color_scheme='fire')
    axs[2].set_title("Metatron's Cube")
    
    # 4. Vesica Piscis
    vesica = create_vesica_piscis(center1=(-0.5, 0), center2=(0.5, 0), radius=1.0)
    plot_2d_pattern(vesica, ax=axs[3], color_scheme='ice')
    axs[3].set_title('Vesica Piscis')
    
    # 5. Fibonacci Spiral
    spiral = create_fibonacci_spiral(center=(0, 0), scale=0.1, n_iterations=10)
    axs[4].plot(spiral[:, 0], spiral[:, 1], 'gold', linewidth=2)
    axs[4].set_aspect('equal')
    axs[4].set_title('Fibonacci Spiral')
    axs[4].set_facecolor('#1a1a2e')
    
    # 6. Golden Rectangle
    rectangle = create_golden_rectangle(center=(0, 0), width=2.0)
    axs[5].plot(rectangle[:, 0], rectangle[:, 1], 'cyan', linewidth=2)
    axs[5].set_aspect('equal')
    axs[5].set_title('Golden Rectangle')
    axs[5].set_facecolor('#1a1a2e')
    
    # Adjust layout and save
    plt.tight_layout()
    plt.savefig('outputs/examples/2d_patterns.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    print("2D patterns example saved to 'outputs/examples/2d_patterns.png'")

def example_3d_shapes():
    """Example of creating and visualizing 3D sacred geometry shapes."""
    # Create a figure with subplots
    fig = plt.figure(figsize=(15, 10))
    
    # 1. Tetrahedron
    ax1 = fig.add_subplot(231, projection='3d')
    tetrahedron = create_tetrahedron(center=(0, 0, 0), radius=1.0)
    plot_3d_shape(tetrahedron, ax=ax1, color_scheme='fire', show_edges=True)
    ax1.set_title('Tetrahedron')
    
    # 2. Cube
    ax2 = fig.add_subplot(232, projection='3d')
    cube = create_cube(center=(0, 0, 0), radius=1.0)
    plot_3d_shape(cube, ax=ax2, color_scheme='earth', show_edges=True)
    ax2.set_title('Cube')
    
    # 3. Octahedron
    ax3 = fig.add_subplot(233, projection='3d')
    octahedron = create_octahedron(center=(0, 0, 0), radius=1.0)
    plot_3d_shape(octahedron, ax=ax3, color_scheme='ice', show_edges=True)
    ax3.set_title('Octahedron')
    
    # 4. Icosahedron
    ax4 = fig.add_subplot(234, projection='3d')
    icosahedron = create_icosahedron(center=(0, 0, 0), radius=1.0)
    plot_3d_shape(icosahedron, ax=ax4, color_scheme='golden', show_edges=True)
    ax4.set_title('Icosahedron')
    
    # 5. Dodecahedron
    ax5 = fig.add_subplot(235, projection='3d')
    dodecahedron = create_dodecahedron(center=(0, 0, 0), radius=1.0)
    plot_3d_shape(dodecahedron, ax=ax5, color_scheme='rainbow', show_edges=True)
    ax5.set_title('Dodecahedron')
    
    # 6. Merkaba
    ax6 = fig.add_subplot(236, projection='3d')
    merkaba = create_merkaba(center=(0, 0, 0), radius=1.0, rotation=0.0)
    plot_3d_shape(merkaba, ax=ax6, color_scheme='cosmic', show_edges=True)
    ax6.set_title('Merkaba')
    
    # Adjust layout and save
    plt.tight_layout()
    plt.savefig('outputs/examples/3d_shapes.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    print("3D shapes example saved to 'outputs/examples/3d_shapes.png'")

def example_combined():
    """Example of combining multiple sacred geometry patterns."""
    # Create a figure
    fig, ax = plt.subplots(figsize=(10, 10))
    
    # Create a Flower of Life as the base
    flower = create_flower_of_life(center=(0, 0), radius=1.0, layers=3)
    
    # Create Metatron's Cube overlaid on the Flower of Life
    metatron = create_metatrons_cube(center=(0, 0), radius=1.0)
    
    # Create a Fibonacci Spiral
    spiral = create_fibonacci_spiral(center=(0, 0), scale=0.1, n_iterations=10)
    
    # Plot all patterns
    for circle in flower:
        ax.plot(circle[:, 0], circle[:, 1], 'gold', alpha=0.5)
    
    for line in metatron:
        if isinstance(line, np.ndarray):
            ax.plot(line[:, 0], line[:, 1], 'cyan', alpha=0.7)
    
    ax.plot(spiral[:, 0], spiral[:, 1], 'magenta', linewidth=2)
    
    # Set properties
    ax.set_aspect('equal')
    ax.set_title('Combined Sacred Geometry Patterns', fontsize=16)
    ax.set_facecolor('#1a1a2e')
    ax.axis('off')
    
    # Save the figure
    plt.savefig('outputs/examples/combined_patterns.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    print("Combined patterns example saved to 'outputs/examples/combined_patterns.png'")

def example_golden_ratio():
    """Example demonstrating the golden ratio in sacred geometry."""
    # Create a figure
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # Get the golden ratio
    phi = get_golden_ratio()
    
    # Create a golden rectangle
    rectangle = create_golden_rectangle(center=(0, 0), width=phi)
    
    # Create a Fibonacci spiral within the golden rectangle
    spiral = create_fibonacci_spiral(center=(0, 0), scale=phi/20, n_iterations=8)
    
    # Plot the rectangle
    ax.plot(rectangle[:, 0], rectangle[:, 1], 'white', linewidth=2)
    
    # Plot the spiral
    ax.plot(spiral[:, 0], spiral[:, 1], 'gold', linewidth=2)
    
    # Add text explaining the golden ratio
    ax.text(0, -phi/2 - 0.5, f"Golden Ratio (φ) = {phi:.10f}", 
            ha='center', va='center', color='white', fontsize=12)
    ax.text(0, -phi/2 - 0.7, "The ratio of a to b is the same as the ratio of a+b to a", 
            ha='center', va='center', color='white', fontsize=10)
    
    # Draw the golden ratio illustration
    a = phi
    b = 1
    ax.plot([-a/2, a/2], [-phi/2 - 0.2, -phi/2 - 0.2], 'cyan', linewidth=2)
    ax.plot([-a/2, -a/2 + b], [-phi/2 - 0.3, -phi/2 - 0.3], 'magenta', linewidth=2)
    ax.text(0, -phi/2 - 0.2, "a", ha='center', va='bottom', color='cyan', fontsize=10)
    ax.text(-a/2 + b/2, -phi/2 - 0.3, "b", ha='center', va='bottom', color='magenta', fontsize=10)
    
    # Set properties
    ax.set_aspect('equal')
    ax.set_title('The Golden Ratio in Sacred Geometry', fontsize=16)
    ax.set_facecolor('#1a1a2e')
    ax.axis('off')
    
    # Save the figure
    plt.savefig('outputs/examples/golden_ratio.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    print("Golden ratio example saved to 'outputs/examples/golden_ratio.png'")

if __name__ == "__main__":
    print("Running Sacred Geometry examples...")
    
    # Run examples
    example_2d_patterns()
    example_3d_shapes()
    example_combined()
    example_golden_ratio()
    
    print("All examples completed successfully!")
