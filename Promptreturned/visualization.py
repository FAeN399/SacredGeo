"""
Visualization utilities for sacred geometry patterns.
"""
import numpy as np
import matplotlib.pyplot as plt
# Import only what's needed
from matplotlib.patches import Polygon, Circle  # noqa: F401 - May be used in future extensions
from mpl_toolkits.mplot3d import Axes3D  # noqa: F401 - Required for 3D projection
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
# Other modules
import matplotlib  # noqa: F401 - Used for general matplotlib configuration
from typing import List, Tuple, Dict, Any, Optional, Union

def plot_2d_pattern(pattern: Any, title: str = "Sacred Geometry Pattern", 
                  show_points: bool = False, color_scheme: str = "rainbow",
                  figure_size: Tuple[int, int] = (10, 10)) -> plt.Figure:
    """
    Plot a 2D sacred geometry pattern.
    
    Args:
        pattern: The pattern to plot (various formats supported)
        title: Title for the plot
        show_points: Whether to show points/vertices
        color_scheme: Color scheme to use ('rainbow', 'golden', 'monochrome')
        figure_size: Size of the figure in inches
        
    Returns:
        The matplotlib figure
    """
    fig, ax = plt.subplots(figsize=figure_size)
    ax.set_aspect('equal')
    ax.set_title(title)
    ax.grid(True, linestyle='--', alpha=0.7)
    
    # Choose a color map based on the color scheme
    if color_scheme == "rainbow":
        cmap = plt.cm.hsv
    elif color_scheme == "golden":
        # Golden colors: golds, yellows, oranges, browns
        cmap = plt.cm.YlOrBr
    elif color_scheme == "monochrome":
        cmap = plt.cm.Blues
    else:
        cmap = plt.cm.viridis
    
    # If the pattern is a list of circles (like Flower of Life)
    if isinstance(pattern, list) and len(pattern) > 0 and isinstance(pattern[0], np.ndarray):
        for i, circle in enumerate(pattern):
            color = cmap(i / len(pattern))
            ax.plot(circle[:, 0], circle[:, 1], color=color, alpha=0.7)
            
            if show_points:
                ax.scatter(circle[0, 0], circle[0, 1], color=color, s=20)
    
    # If the pattern is a dictionary (like Metatron's Cube or Vesica Piscis)
    elif isinstance(pattern, dict):
        # Check for circles
        for key in ['circle', 'circle1', 'circle2', 'circles']:
            if key in pattern:
                circles = pattern[key] if key == 'circles' else [pattern[key]]
                if not isinstance(circles, list):
                    circles = [circles]
                
                for i, circle in enumerate(circles):
                    color = cmap(i / max(1, len(circles)))
                    ax.plot(circle[:, 0], circle[:, 1], color=color, alpha=0.7)
        
        # Check for lines
        if 'lines' in pattern:
            for i, line in enumerate(pattern['lines']):
                color = cmap(i / max(1, len(pattern['lines'])))
                ax.plot([line[0][0], line[1][0]], [line[0][1], line[1][1]], 
                       color=color, linewidth=1, alpha=0.7)
        
        # Check for points
        for key in ['vertices', 'intersection_points']:
            if key in pattern and show_points:
                points = pattern[key]
                if len(points) > 0:
                    points_array = np.array(points)
                    ax.scatter(points_array[:, 0], points_array[:, 1], color='red', s=30)
        
        # Check for spiral
        if 'spiral' in pattern:
            spiral = pattern['spiral']
            if len(spiral) > 0:
                ax.plot(spiral[:, 0], spiral[:, 1], color='red', linewidth=2)
    
    # If the pattern is a numpy array of points
    elif isinstance(pattern, np.ndarray):
        # Assuming it's a single shape like a polygon
        ax.plot(np.append(pattern[:, 0], pattern[0, 0]), 
               np.append(pattern[:, 1], pattern[0, 1]), 
               'b-', linewidth=2)
        
        if show_points:
            ax.scatter(pattern[:, 0], pattern[:, 1], color='red', s=30)
    
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    plt.tight_layout()
    
    return fig

def plot_3d_shape(shape: Dict[str, Any], title: str = "3D Sacred Geometry", 
                color_scheme: str = "rainbow", custom_color: str = None, alpha: float = 0.7, 
                show_edges: bool = True, show_vertices: bool = True,
                figure_size: Tuple[int, int] = (10, 10), ax: Optional[plt.Axes] = None) -> plt.Figure:
    """
    Plot a 3D sacred geometry shape.
    
    Args:
        shape: Dictionary containing shape data
        title: Title for the plot
        color_scheme: Color scheme to use ('rainbow', 'golden', 'monochrome', 'custom')
        custom_color: Custom color to use when color_scheme is 'custom'
        alpha: Transparency of faces
        show_edges: Whether to show edges
        show_vertices: Whether to show vertices
        figure_size: Size of the figure in inches
        ax: Optional external axes to plot on
        
    Returns:
        The matplotlib figure
    """
    # Create figure if no axes provided
    if ax is None:
        fig = plt.figure(figsize=figure_size)
        ax = fig.add_subplot(111, projection='3d')
        ax.set_title(title)
    else:
        fig = ax.figure
    
    # Choose a color map based on the color scheme
    if color_scheme == "rainbow":
        cmap = plt.cm.hsv
    elif color_scheme == "golden":
        cmap = plt.cm.YlOrBr
    elif color_scheme == "custom" and custom_color:
        cmap = lambda _: custom_color  # Use underscore for unused parameter
    # The following elif was duplicated, so it's been removed
    else:
        cmap = plt.cm.viridis
    
    # Check if the shape is a Merkaba (contains two tetrahedra)
    if 'tetrahedron1' in shape and 'tetrahedron2' in shape:
        # Plot first tetrahedron
        tetra1 = shape['tetrahedron1']
        vertices1 = tetra1['vertices']
        faces1 = tetra1['faces']
        
        # Create the collection of polygons for tetrahedron 1
        face_collection1 = []
        for face in faces1:
            face_vertices = [vertices1[i] for i in face]
            face_collection1.append(face_vertices)
        
        _plot_polyhedron(ax, vertices1, faces1, cmap(0.3), alpha, show_edges)
        
        # Plot second tetrahedron
        tetra2 = shape['tetrahedron2']
        vertices2 = tetra2['vertices']
        faces2 = tetra2['faces']
        _plot_polyhedron(ax, vertices2, faces2, cmap(0.7), alpha, show_edges)
        
        # Show vertices if requested
        if show_vertices:
            ax.scatter(vertices1[:, 0], vertices1[:, 1], vertices1[:, 2], 
                     color='red', s=30)
            ax.scatter(vertices2[:, 0], vertices2[:, 1], vertices2[:, 2], 
                     color='blue', s=30)
    
    # Check for 3D Flower of Life (spheres)
    elif 'spheres' in shape:
        spheres = shape['spheres']
        for i, sphere in enumerate(spheres):
            _plot_sphere(ax, sphere['center'], sphere['radius'], 
                       cmap(i / len(spheres)), alpha=alpha/2)
    
    # Regular polyhedron or shape
    elif 'vertices' in shape and ('faces' in shape or 'triangular_faces' in shape or 'square_faces' in shape):
        vertices = shape['vertices']
        
        # Handle different face types
        if 'faces' in shape:
            faces = shape['faces']
            _plot_polyhedron(ax, vertices, faces, cmap(0.5), alpha, show_edges)
        
        if 'triangular_faces' in shape:
            _plot_polyhedron(ax, vertices, shape['triangular_faces'], cmap(0.3), alpha, show_edges)
        
        if 'square_faces' in shape:
            _plot_polyhedron(ax, vertices, shape['square_faces'], cmap(0.7), alpha, show_edges)
        
        # Show vertices if requested
        if show_vertices:
            ax.scatter(vertices[:, 0], vertices[:, 1], vertices[:, 2], 
                     color='black', s=30)
    
    # Set equal aspect ratio
    _set_axes_equal(ax)
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    plt.tight_layout()
    
    return fig

def _plot_polyhedron(ax: plt.Axes, vertices: np.ndarray, faces: List[Tuple], 
                   color: Union[str, Tuple[float, float, float, float]], 
                   alpha: float = 0.7, show_edges: bool = True,
                   edge_color: str = 'black', linewidth: float = 1):
    """Helper function to plot a polyhedron with customizable edge properties."""
    # Create the collection of polygons
    face_collection = []
    for face in faces:
        face_vertices = [vertices[i] for i in face]
        face_collection.append(face_vertices)
    
    # Plot faces
    # Plot faces
    ax.add_collection3d(Poly3DCollection(
        face_collection, 
        color=color, 
        alpha=alpha, 
        linewidths=linewidth if show_edges else 0,
        edgecolors=edge_color if show_edges else color))

def get_color_maps() -> Dict[str, Any]:
    return {
        "rainbow": plt.cm.hsv,
        "golden": plt.cm.YlOrBr,
        "monochrome": plt.cm.Blues,
        "spiritual": plt.cm.RdPu,
        "earth": plt.cm.YlGnBr,
        "water": plt.cm.ocean,
        "fire": plt.cm.Reds,
        "air": plt.cm.cool
    }

def _plot_sphere(ax: plt.Axes, center: Tuple[float, float, float], 
               radius: float, color: Union[str, Tuple[float, float, float, float]], 
               resolution: int = 20, alpha: float = 0.5):
    """Helper function to plot a sphere."""
    u = np.linspace(0, 2 * np.pi, resolution)
    v = np.linspace(0, np.pi, resolution)
    
    x = center[0] + radius * np.outer(np.cos(u), np.sin(v))
    y = center[1] + radius * np.outer(np.sin(u), np.sin(v))
    z = center[2] + radius * np.outer(np.ones(np.size(u)), np.cos(v))
    
    ax.plot_surface(x, y, z, color=color, alpha=alpha)

def _plot_sphere(ax: plt.Axes, center: Tuple[float, float, float], 
               radius: float, color: Union[str, Tuple[float, float, float, float]], 
               resolution: int = 20, alpha: float = 0.5):
    """Helper function to plot a sphere."""
    u = np.linspace(0, 2 * np.pi, resolution)
    v = np.linspace(0, np.pi, resolution)
    
    x = center[0] + radius * np.outer(np.cos(u), np.sin(v))
    y = center[1] + radius * np.outer(np.sin(u), np.sin(v))
    z = center[2] + radius * np.outer(np.ones(np.size(u)), np.cos(v))
    
    ax.plot_surface(x, y, z, color=color, alpha=alpha)

def _set_axes_equal(ax: plt.Axes):
    """Set 3D axes to equal scale."""
    limits = np.array([
        ax.get_xlim3d(),
        ax.get_ylim3d(),
        ax.get_zlim3d(),
    ])
    
    origin = np.mean(limits, axis=1)
    radius = 0.5 * np.max(np.abs(limits[:, 1] - limits[:, 0]))
    
    ax.set_xlim3d([origin[0] - radius, origin[0] + radius])
    ax.set_ylim3d([origin[1] - radius, origin[1] + radius])
    ax.set_zlim3d([origin[2] - radius, origin[2] + radius])

def apply_shape_transform(shape: Dict[str, Any], rotation: float = 0.0, 
                        scale: float = 1.0) -> Dict[str, Any]:
    
    # Create a copy of the shape to avoid modifying the original
    transformed_shape = shape.copy()
    
    # Create rotation matrix
    cos_r = np.cos(rotation)
    sin_r = np.sin(rotation)
    rot_matrix = np.array([
        [cos_r, -sin_r, 0],
        [sin_r, cos_r, 0],
        [0, 0, 1]
    ])
    
    # Apply transformations to vertices
    if 'tetrahedron1' in shape and 'tetrahedron2' in shape:
        # Handle Merkaba case
        for tetra in ['tetrahedron1', 'tetrahedron2']:
            vertices = shape[tetra]['vertices']
            transformed_vertices = vertices * scale
            transformed_vertices = np.dot(transformed_vertices, rot_matrix.T)
            transformed_shape[tetra]['vertices'] = transformed_vertices
    elif 'vertices' in shape:
        # Handle regular polyhedra
        vertices = shape['vertices']
        transformed_vertices = vertices * scale
        transformed_vertices = np.dot(transformed_vertices, rot_matrix.T)
        transformed_shape['vertices'] = transformed_vertices
    
    return transformed_shape
    limits = np.array([
        ax.get_xlim3d(),
        ax.get_ylim3d(),
        ax.get_zlim3d(),
    ])
    
    origin = np.mean(limits, axis=1)
    radius = 0.5 * np.max(np.abs(limits[:, 1] - limits[:, 0]))
    
    ax.set_xlim3d([origin[0] - radius, origin[0] + radius])
    ax.set_ylim3d([origin[1] - radius, origin[1] + radius])
    ax.set_zlim3d([origin[2] - radius, origin[2] + radius])

def animate_pattern(pattern_func, frames: int = 60, interval: int = 50, 
                  save_path: Optional[str] = None, **pattern_kwargs):
    """
    Create an animation of a sacred geometry pattern evolving over time.
    
    Args:
        pattern_func: Function that generates a pattern given parameters
        frames: Number of frames in the animation
        interval: Interval between frames in milliseconds
        save_path: Path to save the animation (None to display only)
        **pattern_kwargs: Keyword arguments for the pattern function
        
    Returns:
        The animation object
    """
    import matplotlib.animation as animation
    
    # Create the figure and axes
    fig, ax = plt.subplots(figsize=(10, 10))
    ax.set_aspect('equal')
    ax.set_title(f"Animated {pattern_func.__name__.replace('create_', '')}")
    ax.grid(True, linestyle='--', alpha=0.7)
    
    # Define the update function for the animation
    def update(frame):
        ax.clear()
        ax.set_aspect('equal')
        ax.grid(True, linestyle='--', alpha=0.7)
        
        # Update pattern parameters based on the frame
        # This will depend on what parameters the specific pattern function accepts
        if 'rotation' in pattern_kwargs:
            pattern_kwargs['rotation'] = frame * 2 * np.pi / frames
        elif 'scale' in pattern_kwargs:
            pattern_kwargs['scale'] = 0.5 + frame / frames
        elif 'radius' in pattern_kwargs:
            pattern_kwargs['radius'] = pattern_kwargs.get('base_radius', 1.0) * (0.5 + 0.5 * frame / frames)
        elif 'layers' in pattern_kwargs:
            pattern_kwargs['layers'] = 1 + int(frame / frames * 4)
        
        # Generate the pattern
        pattern = pattern_func(**pattern_kwargs)
        
        # Plot the pattern
        if isinstance(pattern, list):
            # List of arrays (like Flower of Life circles)
            for circle in pattern:
                ax.plot(circle[:, 0], circle[:, 1], 'b-', alpha=0.5)
        elif isinstance(pattern, dict):
            # Dictionary with different components
            if 'circles' in pattern:
                for circle in pattern['circles']:
                    ax.plot(circle[:, 0], circle[:, 1], 'b-', alpha=0.5)
            if 'lines' in pattern:
                for line in pattern['lines']:
                    ax.plot([line[0][0], line[1][0]], [line[0][1], line[1][1]], 
                          'r-', linewidth=1, alpha=0.7)
            if 'spiral' in pattern:
                spiral = pattern['spiral']
                if len(spiral) > 0:
                    ax.plot(spiral[:, 0], spiral[:, 1], 'r-', linewidth=2)
        
        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        return ax,
    
    # Create the animation
    anim = animation.FuncAnimation(fig, update, frames=frames, interval=interval, blit=False)
    
    # Save the animation if a path is provided
    if save_path:
        anim.save(save_path, writer='pillow')
    
    return anim