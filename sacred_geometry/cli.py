#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Command-line interface for the Sacred Geometry package.

This module provides a command-line interface for generating and exporting
sacred geometry patterns and shapes.
"""

import os
import sys
import argparse
import matplotlib.pyplot as plt
import numpy as np

# Import core modules
from sacred_geometry.core.core import (
    create_flower_of_life, create_seed_of_life, create_metatrons_cube,
    create_vesica_piscis, create_fibonacci_spiral, create_regular_polygon,
    create_golden_rectangle
)

# Import 3D shape modules
from sacred_geometry.shapes.shapes import (
    create_tetrahedron, create_cube, create_octahedron,
    create_icosahedron, create_dodecahedron, create_merkaba,
    create_cuboctahedron, create_flower_of_life_3d, create_torus
)

# Import fractal modules
from sacred_geometry.fractals.fractals import (
    sierpinski_triangle, koch_snowflake, sacred_spiral, fractal_tree
)

# Import visualization modules
from sacred_geometry.visualization.visualization import (
    plot_2d_pattern, plot_3d_shape
)

# Try to import advanced modules
try:
    from sacred_geometry.utils.exporters import (
        export_2d_image, export_svg, export_3d_obj, export_stl,
        export_high_resolution_image
    )
    EXPORTERS_AVAILABLE = True
except ImportError:
    EXPORTERS_AVAILABLE = False

# Create output directories if they don't exist
output_dirs = {
    '2d': 'outputs/2d',
    '3d': 'outputs/3d',
    'fractals': 'outputs/fractals',
    'animations': 'outputs/animations'
}

for directory in output_dirs.values():
    os.makedirs(directory, exist_ok=True)


def parse_arguments():
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description='Sacred Geometry Generator',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    
    # Main command options
    parser.add_argument('--type', '-t', choices=['2d', '3d', 'fractal'], default='2d',
                        help='Type of sacred geometry to generate')
    
    # 2D pattern options
    parser.add_argument('--pattern', '-p', 
                        choices=['flower-of-life', 'seed-of-life', 'metatrons-cube', 
                                'vesica-piscis', 'fibonacci-spiral', 'golden-rectangle',
                                'regular-polygon'],
                        default='flower-of-life',
                        help='Pattern to generate (for 2D type)')
    
    # 3D shape options
    parser.add_argument('--shape', '-s',
                        choices=['tetrahedron', 'cube', 'octahedron', 'icosahedron',
                                'dodecahedron', 'merkaba', 'cuboctahedron', 
                                'flower-of-life-3d', 'torus'],
                        default='merkaba',
                        help='Shape to generate (for 3D type)')
    
    # Fractal options
    parser.add_argument('--fractal', '-f',
                        choices=['sierpinski', 'koch', 'sacred-spiral', 'tree'],
                        default='sierpinski',
                        help='Fractal to generate (for fractal type)')
    
    # Common parameters
    parser.add_argument('--radius', '-r', type=float, default=1.0,
                        help='Radius for patterns and shapes')
    parser.add_argument('--layers', '-l', type=int, default=3,
                        help='Number of layers (for layered patterns)')
    parser.add_argument('--sides', type=int, default=6,
                        help='Number of sides (for regular polygon)')
    parser.add_argument('--depth', '-d', type=int, default=5,
                        help='Recursion depth (for fractals)')
    parser.add_argument('--rotation', type=float, default=0.0,
                        help='Rotation angle in degrees')
    
    # Output options
    parser.add_argument('--output', '-o', type=str, default=None,
                        help='Output filename (without extension)')
    parser.add_argument('--format', choices=['png', 'svg', 'pdf', 'obj', 'stl'], 
                        default='png', help='Output file format')
    parser.add_argument('--dpi', type=int, default=300,
                        help='DPI for raster outputs')
    parser.add_argument('--color-scheme', choices=['golden', 'rainbow', 'monochrome',
                                                  'fire', 'ice', 'earth', 'chakra'],
                        default='golden', help='Color scheme for visualization')
    parser.add_argument('--show', action='store_true',
                        help='Show the visualization (in addition to saving)')
    
    return parser.parse_args()


def generate_2d_pattern(args):
    """Generate a 2D sacred geometry pattern based on arguments."""
    center = (0, 0)
    radius = args.radius
    
    if args.pattern == 'flower-of-life':
        pattern = create_flower_of_life(center=center, radius=radius, layers=args.layers)
    elif args.pattern == 'seed-of-life':
        pattern = create_seed_of_life(center=center, radius=radius)
    elif args.pattern == 'metatrons-cube':
        pattern = create_metatrons_cube(center=center, radius=radius)
    elif args.pattern == 'vesica-piscis':
        pattern = create_vesica_piscis(
            center1=(-radius/2, 0), 
            center2=(radius/2, 0), 
            radius=radius
        )
    elif args.pattern == 'fibonacci-spiral':
        pattern = create_fibonacci_spiral(
            center=center, 
            scale=radius/10, 
            n_iterations=args.layers * 4
        )
    elif args.pattern == 'golden-rectangle':
        pattern = create_golden_rectangle(center=center, width=radius*2)
    elif args.pattern == 'regular-polygon':
        pattern = create_regular_polygon(
            center=center, 
            radius=radius, 
            sides=args.sides, 
            rotation=args.rotation * np.pi / 180
        )
    else:
        raise ValueError(f"Unknown 2D pattern: {args.pattern}")
    
    # Create figure and plot
    fig, ax = plt.subplots(figsize=(10, 10))
    plot_2d_pattern(pattern, ax=ax, color_scheme=args.color_scheme)
    
    # Save the output
    if args.output:
        output_filename = args.output
    else:
        output_filename = f"outputs/2d/{args.pattern}"
    
    if not output_filename.endswith(f".{args.format}"):
        output_filename = f"{output_filename}.{args.format}"
    
    if EXPORTERS_AVAILABLE and args.format == 'svg':
        export_svg(pattern, output_filename, color_scheme=args.color_scheme)
    else:
        fig.savefig(output_filename, dpi=args.dpi, bbox_inches='tight')
    
    print(f"Saved to {output_filename}")
    
    if args.show:
        plt.show()
    
    return fig, ax


def generate_3d_shape(args):
    """Generate a 3D sacred geometry shape based on arguments."""
    center = (0, 0, 0)
    radius = args.radius
    
    if args.shape == 'tetrahedron':
        shape = create_tetrahedron(center=center, radius=radius)
    elif args.shape == 'cube':
        shape = create_cube(center=center, radius=radius)
    elif args.shape == 'octahedron':
        shape = create_octahedron(center=center, radius=radius)
    elif args.shape == 'icosahedron':
        shape = create_icosahedron(center=center, radius=radius)
    elif args.shape == 'dodecahedron':
        shape = create_dodecahedron(center=center, radius=radius)
    elif args.shape == 'merkaba':
        shape = create_merkaba(
            center=center, 
            radius=radius, 
            rotation=args.rotation * np.pi / 180
        )
    elif args.shape == 'cuboctahedron':
        shape = create_cuboctahedron(center=center, radius=radius)
    elif args.shape == 'flower-of-life-3d':
        shape = create_flower_of_life_3d(
            center=center, 
            radius=radius, 
            layers=args.layers
        )
    elif args.shape == 'torus':
        shape = create_torus(
            center=center,
            major_radius=radius,
            minor_radius=radius/4,
            num_major_segments=48,
            num_minor_segments=24
        )
    else:
        raise ValueError(f"Unknown 3D shape: {args.shape}")
    
    # Create figure and plot
    fig = plt.figure(figsize=(10, 10))
    ax = fig.add_subplot(111, projection='3d')
    plot_3d_shape(
        shape, 
        ax=ax, 
        color_scheme=args.color_scheme,
        show_edges=True,
        show_vertices=True
    )
    
    # Save the output
    if args.output:
        output_filename = args.output
    else:
        output_filename = f"outputs/3d/{args.shape}"
    
    if args.format in ['obj', 'stl']:
        if not output_filename.endswith(f".{args.format}"):
            output_filename = f"{output_filename}.{args.format}"
        
        if EXPORTERS_AVAILABLE:
            if args.format == 'obj':
                export_3d_obj(shape, output_filename)
            elif args.format == 'stl':
                export_stl(shape, output_filename)
        else:
            print(f"Warning: 3D export requires the exporters module. Saving as PNG instead.")
            output_filename = output_filename.replace(f".{args.format}", ".png")
            fig.savefig(output_filename, dpi=args.dpi, bbox_inches='tight')
    else:
        if not output_filename.endswith(f".{args.format}"):
            output_filename = f"{output_filename}.{args.format}"
        fig.savefig(output_filename, dpi=args.dpi, bbox_inches='tight')
    
    print(f"Saved to {output_filename}")
    
    if args.show:
        plt.show()
    
    return fig, ax


def generate_fractal(args):
    """Generate a fractal pattern based on arguments."""
    if args.fractal == 'sierpinski':
        pattern = sierpinski_triangle(
            center=(0, 0),
            size=args.radius * 2,
            depth=args.depth
        )
    elif args.fractal == 'koch':
        pattern = koch_snowflake(
            center=(0, 0),
            size=args.radius * 2,
            depth=args.depth
        )
    elif args.fractal == 'sacred-spiral':
        pattern = sacred_spiral(
            center=(0, 0),
            initial_radius=args.radius / 10,
            growth_factor=1.1,
            n_points=100 * args.depth
        )
    elif args.fractal == 'tree':
        pattern = fractal_tree(
            start=(0, -args.radius),
            angle=np.pi/2,
            length=args.radius,
            depth=args.depth
        )
    else:
        raise ValueError(f"Unknown fractal: {args.fractal}")
    
    # Create figure and plot
    fig, ax = plt.subplots(figsize=(10, 10))
    
    if isinstance(pattern, list):
        # For fractals that return a list of line segments
        for line in pattern:
            ax.plot(line[:, 0], line[:, 1], color='gold', alpha=0.8)
    else:
        # For fractals that return a single array
        ax.plot(pattern[:, 0], pattern[:, 1], color='gold', alpha=0.8)
    
    ax.set_aspect('equal')
    ax.axis('off')
    ax.set_facecolor('#1a1a2e')
    
    # Save the output
    if args.output:
        output_filename = args.output
    else:
        output_filename = f"outputs/fractals/{args.fractal}"
    
    if not output_filename.endswith(f".{args.format}"):
        output_filename = f"{output_filename}.{args.format}"
    
    fig.savefig(output_filename, dpi=args.dpi, bbox_inches='tight')
    print(f"Saved to {output_filename}")
    
    if args.show:
        plt.show()
    
    return fig, ax


def main():
    """Main entry point for the CLI."""
    args = parse_arguments()
    
    try:
        if args.type == '2d':
            generate_2d_pattern(args)
        elif args.type == '3d':
            generate_3d_shape(args)
        elif args.type == 'fractal':
            generate_fractal(args)
        else:
            print(f"Unknown type: {args.type}")
            return 1
        
        return 0
    except Exception as e:
        print(f"Error: {str(e)}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
