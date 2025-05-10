"""
Sacred Geometry Custom Compositions Module

This module provides functions for creating complex sacred geometry compositions
by combining different patterns and shapes. It includes layered patterns,
mandalas, and 3D constellations.
"""
import numpy as np
from typing import Dict, List, Tuple, Any, Optional, Union
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from mpl_toolkits.mplot3d import Axes3D

# Import core patterns
from sacred_geometry.core.core import (
    create_flower_of_life, create_seed_of_life, create_metatrons_cube,
    create_vesica_piscis, create_fibonacci_spiral, create_regular_polygon,
    create_golden_rectangle, get_golden_ratio
)

# Import 3D shapes
from sacred_geometry.shapes.shapes import (
    create_tetrahedron, create_cube, create_octahedron,
    create_icosahedron, create_dodecahedron, create_merkaba,
    create_cuboctahedron, create_flower_of_life_3d, create_torus
)

# Import fractals
from sacred_geometry.fractals.fractals import (
    sierpinski_triangle, koch_snowflake, sacred_spiral, fractal_tree
)

# Type aliases
Point2D = Tuple[float, float]
Point3D = Tuple[float, float, float]
Pattern2D = List[np.ndarray]
Shape3D = Dict[str, Any]


def create_flower_of_life_with_fibonacci(
    center: Point2D = (0, 0),
    radius: float = 1.0,
    layers: int = 3,
    spiral_scale: float = 0.1,
    spiral_turns: int = 5
) -> Dict[str, Any]:
    """
    Create a composition with Flower of Life and Fibonacci Spiral.
    
    Args:
        center: Center point of the composition
        radius: Radius of the Flower of Life circles
        layers: Number of layers in the Flower of Life
        spiral_scale: Scale factor for the Fibonacci spiral
        spiral_turns: Number of turns in the Fibonacci spiral
        
    Returns:
        Dictionary containing the composition elements
    """
    # Create Flower of Life
    flower = create_flower_of_life(center=center, radius=radius, layers=layers)
    
    # Create Fibonacci Spiral
    # Scale the spiral to fit nicely within the Flower of Life
    spiral_center = center
    spiral = create_fibonacci_spiral(
        center=spiral_center,
        scale=radius * spiral_scale,
        n_iterations=spiral_turns * 4
    )
    
    # Return the composition
    return {
        "flower_of_life": flower,
        "fibonacci_spiral": spiral,
        "center": center,
        "radius": radius,
        "type": "2D"
    }


def create_sacred_geometry_mandala(
    center: Point2D = (0, 0),
    radius: float = 1.0,
    complexity: int = 3,
    rotation: float = 0.0
) -> Dict[str, Any]:
    """
    Create a sacred geometry mandala with multiple layers of patterns.
    
    Args:
        center: Center point of the mandala
        radius: Base radius of the mandala
        complexity: Level of detail (1-5)
        rotation: Rotation angle in radians
        
    Returns:
        Dictionary containing the mandala elements
    """
    mandala = {
        "center": center,
        "radius": radius,
        "complexity": complexity,
        "type": "2D",
        "layers": []
    }
    
    # Layer 1: Central seed of life
    seed = create_seed_of_life(center=center, radius=radius * 0.3)
    mandala["layers"].append({"type": "seed_of_life", "pattern": seed})
    
    # Layer 2: Surrounding regular polygons
    if complexity >= 2:
        # Create polygons with increasing number of sides
        for i in range(3, 3 + complexity):
            polygon_radius = radius * (0.4 + i * 0.1)
            polygon = create_regular_polygon(
                center=center,
                radius=polygon_radius,
                sides=i + 3,  # Start with hexagon (6 sides)
                rotation=rotation + (i * np.pi / 12)
            )
            mandala["layers"].append({"type": f"polygon_{i+3}", "pattern": polygon})
    
    # Layer 3: Vesica Piscis elements
    if complexity >= 3:
        vesica_elements = []
        for i in range(6):  # Create 6 vesica piscis arranged in a circle
            angle = i * np.pi / 3 + rotation
            center1 = (
                center[0] + radius * 0.6 * np.cos(angle),
                center[1] + radius * 0.6 * np.sin(angle)
            )
            center2 = (
                center[0] + radius * 0.6 * np.cos(angle + np.pi / 6),
                center[1] + radius * 0.6 * np.sin(angle + np.pi / 6)
            )
            vesica = create_vesica_piscis(
                center1=center1,
                center2=center2,
                radius=radius * 0.2
            )
            vesica_elements.append(vesica)
        mandala["layers"].append({"type": "vesica_piscis", "pattern": vesica_elements})
    
    # Layer 4: Fibonacci spiral elements
    if complexity >= 4:
        spiral_elements = []
        for i in range(complexity):
            angle = i * 2 * np.pi / complexity + rotation
            spiral_center = (
                center[0] + radius * 0.5 * np.cos(angle),
                center[1] + radius * 0.5 * np.sin(angle)
            )
            spiral = create_fibonacci_spiral(
                center=spiral_center,
                scale=radius * 0.05,
                n_iterations=5
            )
            spiral_elements.append(spiral)
        mandala["layers"].append({"type": "fibonacci_spiral", "pattern": spiral_elements})
    
    # Layer 5: Outer flower of life
    if complexity >= 5:
        outer_flower = create_flower_of_life(center=center, radius=radius * 0.15, layers=2)
        mandala["layers"].append({"type": "flower_of_life", "pattern": outer_flower})
    
    return mandala


def create_metatrons_cube_with_platonic_projections(
    center: Point3D = (0, 0, 0),
    radius: float = 1.0,
    show_all_solids: bool = True
) -> Dict[str, Any]:
    """
    Create Metatron's Cube with projections of Platonic solids.
    
    Args:
        center: Center point of the composition
        radius: Base radius for the shapes
        show_all_solids: Whether to include all five Platonic solids
        
    Returns:
        Dictionary containing the composition elements
    """
    # Create Metatron's Cube (2D)
    metatrons_cube_2d = create_metatrons_cube(center=center[:2], radius=radius)
    
    # Create the Platonic solids
    platonic_solids = {}
    
    # Always include tetrahedron
    platonic_solids["tetrahedron"] = create_tetrahedron(
        center=center,
        radius=radius * 0.6
    )
    
    if show_all_solids:
        # Add other Platonic solids
        platonic_solids["cube"] = create_cube(
            center=center,
            radius=radius * 0.7
        )
        
        platonic_solids["octahedron"] = create_octahedron(
            center=center,
            radius=radius * 0.65
        )
        
        platonic_solids["dodecahedron"] = create_dodecahedron(
            center=center,
            radius=radius * 0.8
        )
        
        platonic_solids["icosahedron"] = create_icosahedron(
            center=center,
            radius=radius * 0.75
        )
    
    # Return the composition
    return {
        "metatrons_cube_2d": metatrons_cube_2d,
        "platonic_solids": platonic_solids,
        "center": center,
        "radius": radius,
        "type": "3D"
    }


def create_fractal_tree_with_golden_ratio(
    center: Point2D = (0, 0),
    size: float = 1.0,
    depth: int = 5,
    use_golden_ratio: bool = True
) -> Dict[str, Any]:
    """
    Create a fractal tree with proportions based on the golden ratio.
    
    Args:
        center: Base point of the tree
        size: Size of the tree
        depth: Recursion depth
        use_golden_ratio: Whether to use golden ratio for branching
        
    Returns:
        Dictionary containing the composition elements
    """
    # Calculate parameters based on golden ratio if requested
    if use_golden_ratio:
        phi = get_golden_ratio()
        length_factor = 1 / phi  # Approximately 0.618
        angle_delta = np.pi / phi  # Approximately 108 degrees
    else:
        length_factor = 0.7
        angle_delta = np.pi / 4  # 45 degrees
    
    # Create the fractal tree
    tree_branches = fractal_tree(
        start=(center[0], center[1] - size),
        angle=np.pi/2,  # Initial angle (pointing up)
        length=size,
        depth=depth,
        length_factor=length_factor,
        angle_delta=angle_delta
    )
    
    # Create a golden spiral to complement the tree
    spiral = create_fibonacci_spiral(
        center=(center[0] + size * 0.3, center[1]),
        scale=size * 0.1,
        n_iterations=10
    )
    
    # Return the composition
    return {
        "tree_branches": tree_branches,
        "golden_spiral": spiral,
        "center": center,
        "size": size,
        "depth": depth,
        "golden_ratio_used": use_golden_ratio,
        "type": "2D"
    }


def create_nested_platonic_solids(
    center: Point3D = (0, 0, 0),
    radius: float = 1.0,
    complexity: int = 3
) -> Dict[str, Any]:
    """
    Create nested Platonic solids with increasing complexity.
    
    Args:
        center: Center point of the composition
        radius: Base radius for the outermost solid
        complexity: Level of nesting (1-5)
        
    Returns:
        Dictionary containing the composition elements
    """
    nested_solids = {
        "center": center,
        "radius": radius,
        "complexity": complexity,
        "type": "3D",
        "solids": []
    }
    
    # Define the nesting order of Platonic solids
    nesting_order = [
        "icosahedron",
        "dodecahedron",
        "octahedron",
        "cube",
        "tetrahedron"
    ]
    
    # Create nested solids based on complexity
    for i in range(min(complexity, 5)):
        solid_type = nesting_order[i]
        solid_radius = radius * (1 - i * 0.15)  # Decrease radius for inner solids
        
        if solid_type == "tetrahedron":
            solid = create_tetrahedron(center=center, radius=solid_radius)
        elif solid_type == "cube":
            solid = create_cube(center=center, radius=solid_radius)
        elif solid_type == "octahedron":
            solid = create_octahedron(center=center, radius=solid_radius)
        elif solid_type == "dodecahedron":
            solid = create_dodecahedron(center=center, radius=solid_radius)
        elif solid_type == "icosahedron":
            solid = create_icosahedron(center=center, radius=solid_radius)
        
        nested_solids["solids"].append({
            "type": solid_type,
            "solid": solid,
            "radius": solid_radius
        })
    
    return nested_solids


def create_cosmic_torus_with_merkaba(
    center: Point3D = (0, 0, 0),
    major_radius: float = 2.0,
    minor_radius: float = 0.5,
    merkaba_radius: float = 1.0,
    merkaba_rotation: float = np.pi/4
) -> Dict[str, Any]:
    """
    Create a cosmic torus with a merkaba at the center.
    
    Args:
        center: Center point of the composition
        major_radius: Major radius of the torus
        minor_radius: Minor radius of the torus
        merkaba_radius: Radius of the merkaba
        merkaba_rotation: Rotation angle of the merkaba
        
    Returns:
        Dictionary containing the composition elements
    """
    # Create the torus
    torus = create_torus(
        center=center,
        major_radius=major_radius,
        minor_radius=minor_radius,
        num_major_segments=48,
        num_minor_segments=24
    )
    
    # Create the merkaba at the center
    merkaba = create_merkaba(
        center=center,
        radius=merkaba_radius,
        rotation=merkaba_rotation
    )
    
    # Return the composition
    return {
        "torus": torus,
        "merkaba": merkaba,
        "center": center,
        "major_radius": major_radius,
        "minor_radius": minor_radius,
        "merkaba_radius": merkaba_radius,
        "type": "3D"
    }


def create_tree_of_life_template(
    center: Point2D = (0, 0),
    size: float = 1.0,
    with_paths: bool = True
) -> Dict[str, Any]:
    """
    Create a Tree of Life (Kabbalah) template with sacred geometry elements.
    
    Args:
        center: Center point of the composition
        size: Size of the tree
        with_paths: Whether to include the 22 paths connecting the sephirot
        
    Returns:
        Dictionary containing the composition elements
    """
    # Define the positions of the 10 sephirot (normalized coordinates)
    # These follow the traditional Tree of Life arrangement
    sephirot_positions = [
        (0.0, 1.0),      # Keter (Crown)
        (-0.5, 0.8),     # Chokmah (Wisdom)
        (0.5, 0.8),      # Binah (Understanding)
        (0.0, 0.6),      # Daat (Knowledge) - sometimes not counted
        (-0.5, 0.4),     # Chesed (Kindness)
        (0.5, 0.4),      # Geburah (Severity)
        (0.0, 0.2),      # Tiferet (Beauty)
        (-0.5, 0.0),     # Netzach (Victory)
        (0.5, 0.0),      # Hod (Splendor)
        (0.0, -0.2),     # Yesod (Foundation)
        (0.0, -0.6)      # Malkuth (Kingdom)
    ]
    
    # Scale and translate the positions
    sephirot = []
    for pos in sephirot_positions:
        x = center[0] + pos[0] * size
        y = center[1] + pos[1] * size
        sephirot.append((x, y))
    
    # Define the paths connecting the sephirot
    paths = []
    if with_paths:
        # Define the 22 traditional paths
        path_indices = [
            (0, 1), (0, 2), (1, 2), (1, 3), (1, 4), (2, 3), (2, 5),
            (3, 4), (3, 5), (3, 6), (4, 5), (4, 6), (4, 7), (5, 6),
            (5, 8), (6, 7), (6, 8), (6, 9), (7, 8), (7, 9), (8, 9),
            (9, 10)
        ]
        
        for i, j in path_indices:
            paths.append((sephirot[i], sephirot[j]))
    
    # Create circles for each sephirot
    circles = []
    sephirot_radius = size * 0.08
    for pos in sephirot:
        # Create a circle with 100 points
        theta = np.linspace(0, 2*np.pi, 100)
        x = pos[0] + sephirot_radius * np.cos(theta)
        y = pos[1] + sephirot_radius * np.sin(theta)
        circles.append(np.column_stack((x, y)))
    
    # Return the composition
    return {
        "sephirot": sephirot,
        "circles": circles,
        "paths": paths,
        "center": center,
        "size": size,
        "type": "2D"
    }


def plot_composition(
    composition: Dict[str, Any],
    ax: Optional[plt.Axes] = None,
    color_scheme: str = "golden",
    show_labels: bool = False,
    alpha: float = 0.7
) -> plt.Axes:
    """
    Plot a sacred geometry composition.
    
    Args:
        composition: The composition to plot
        ax: Matplotlib axes to plot on (created if None)
        color_scheme: Color scheme to use
        show_labels: Whether to show labels for components
        alpha: Transparency value
        
    Returns:
        The matplotlib axes with the plotted composition
    """
    # Create axes if not provided
    if ax is None:
        if composition["type"] == "3D":
            fig = plt.figure(figsize=(10, 10))
            ax = fig.add_subplot(111, projection='3d')
        else:
            fig = plt.figure(figsize=(10, 10))
            ax = fig.add_subplot(111)
            ax.set_aspect('equal')
    
    # Set dark theme for the axes
    ax.set_facecolor('#1a1a2e')
    
    # Plot based on composition type
    if composition["type"] == "2D":
        # Plot 2D composition
        if "flower_of_life" in composition:
            for i, circle in enumerate(composition["flower_of_life"]):
                ax.plot(circle[:, 0], circle[:, 1], 'gold', alpha=alpha)
        
        if "fibonacci_spiral" in composition:
            ax.plot(
                composition["fibonacci_spiral"][:, 0],
                composition["fibonacci_spiral"][:, 1],
                'cyan', linewidth=2, alpha=alpha
            )
        
        if "layers" in composition:  # For mandala
            colors = ['gold', 'cyan', 'magenta', 'lime', 'orange', 'white']
            for i, layer in enumerate(composition["layers"]):
                color = colors[i % len(colors)]
                if isinstance(layer["pattern"], list):
                    for pattern in layer["pattern"]:
                        if isinstance(pattern, dict) and "circle1" in pattern:
                            # Handle vesica piscis
                            ax.plot(pattern["circle1"][:, 0], pattern["circle1"][:, 1], color, alpha=alpha)
                            ax.plot(pattern["circle2"][:, 0], pattern["circle2"][:, 1], color, alpha=alpha)
                        else:
                            ax.plot(pattern[:, 0], pattern[:, 1], color, alpha=alpha)
                else:
                    ax.plot(layer["pattern"][:, 0], layer["pattern"][:, 1], color, alpha=alpha)
        
        if "tree_branches" in composition:
            for branch in composition["tree_branches"]:
                ax.plot(branch[:, 0], branch[:, 1], 'brown', linewidth=1.5, alpha=alpha)
        
        if "circles" in composition:  # For Tree of Life
            for i, circle in enumerate(composition["circles"]):
                ax.plot(circle[:, 0], circle[:, 1], 'gold', alpha=alpha)
            
            # Plot paths
            if "paths" in composition:
                for path in composition["paths"]:
                    ax.plot([path[0][0], path[1][0]], [path[0][1], path[1][1]], 'white', alpha=alpha*0.7)
    
    elif composition["type"] == "3D":
        # Plot 3D composition
        from sacred_geometry.visualization.visualization import plot_3d_shape
        
        if "torus" in composition:
            plot_3d_shape(
                composition["torus"],
                color_scheme=color_scheme,
                alpha=alpha*0.5,
                show_edges=True,
                ax=ax
            )
        
        if "merkaba" in composition:
            plot_3d_shape(
                composition["merkaba"],
                color_scheme="golden",
                alpha=alpha,
                show_edges=True,
                ax=ax
            )
        
        if "platonic_solids" in composition:
            colors = ["cyan", "magenta", "gold", "lime", "orange"]
            for i, (name, solid) in enumerate(composition["platonic_solids"].items()):
                plot_3d_shape(
                    solid,
                    color_scheme=colors[i % len(colors)],
                    alpha=alpha*0.7,
                    show_edges=True,
                    ax=ax
                )
        
        if "solids" in composition:  # For nested Platonic solids
            colors = ["gold", "cyan", "magenta", "lime", "orange"]
            for i, solid_info in enumerate(composition["solids"]):
                plot_3d_shape(
                    solid_info["solid"],
                    color_scheme=colors[i % len(colors)],
                    alpha=alpha*(1 - i*0.1),  # Decrease alpha for inner solids
                    show_edges=True,
                    ax=ax
                )
    
    # Set labels and title
    if "type" in composition:
        if composition["type"] == "2D":
            ax.set_xlabel("X")
            ax.set_ylabel("Y")
        else:
            ax.set_xlabel("X")
            ax.set_ylabel("Y")
            ax.set_zlabel("Z")
    
    return ax
