"""
Lighting Effects Module for Sacred Geometry Visualization

This module provides enhanced lighting effects for 3D sacred geometry shapes.
It uses a simplified lighting model that works with matplotlib's 3D plotting.
"""
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import matplotlib.colors as mcolors
from typing import Dict, List, Tuple, Any, Optional, Union

# Type aliases
Point3D = Tuple[float, float, float]
RGB = Tuple[float, float, float]
RGBA = Tuple[float, float, float, float]
ColorType = Union[str, RGB, RGBA]

def calculate_normals(vertices: np.ndarray, faces: List[List[int]]) -> np.ndarray:
    """
    Calculate the normal vectors for each face in a 3D shape.
    
    Args:
        vertices: Array of vertex coordinates
        faces: List of faces, each containing indices of vertices
        
    Returns:
        Array of normal vectors for each face
    """
    normals = []
    for face in faces:
        if len(face) >= 3:
            # Get three vertices of the face
            v0 = vertices[face[0]]
            v1 = vertices[face[1]]
            v2 = vertices[face[2]]
            
            # Calculate two edges
            edge1 = v1 - v0
            edge2 = v2 - v0
            
            # Calculate the normal using cross product
            normal = np.cross(edge1, edge2)
            
            # Normalize the normal vector
            norm = np.linalg.norm(normal)
            if norm > 0:
                normal = normal / norm
            
            normals.append(normal)
        else:
            # If face has fewer than 3 vertices, add a zero normal
            normals.append(np.array([0, 0, 0]))
    
    return np.array(normals)

def apply_lighting(
    colors: List[str],
    normals: np.ndarray,
    light_direction: np.ndarray,
    ambient: float = 0.3,
    diffuse: float = 0.7
) -> List[str]:
    """
    Apply lighting to colors based on face normals and light direction.
    
    Args:
        colors: List of color strings
        normals: Normal vectors for each face
        light_direction: Direction of the light source (normalized)
        ambient: Ambient light intensity (0-1)
        diffuse: Diffuse light intensity (0-1)
        
    Returns:
        List of colors with lighting applied
    """
    # Normalize light direction
    light_direction = light_direction / np.linalg.norm(light_direction)
    
    # Convert colors to RGB
    rgb_colors = [mcolors.to_rgb(color) for color in colors]
    
    # Apply lighting to each color
    lit_colors = []
    for i, rgb in enumerate(rgb_colors):
        # Calculate diffuse component (dot product of normal and light direction)
        dot = max(0, np.dot(normals[i], light_direction))
        
        # Apply lighting formula: ambient + diffuse * dot
        lit_rgb = tuple(min(1.0, c * (ambient + diffuse * dot)) for c in rgb)
        
        # Convert back to hex color
        lit_colors.append(mcolors.to_hex(lit_rgb))
    
    return lit_colors

def enhance_material(
    colors: List[str],
    material: str,
    alpha: float
) -> Tuple[List[str], float]:
    """
    Enhance colors based on material type.
    
    Args:
        colors: List of color strings
        material: Material type (matte, metallic, glass, crystal, energy)
        alpha: Base transparency value
        
    Returns:
        Tuple of (enhanced colors, adjusted alpha)
    """
    enhanced_colors = colors.copy()
    adjusted_alpha = alpha
    
    if material == "metallic":
        # Make colors more reflective for metallic material
        enhanced_colors = [lighten_color(color, 1.2) for color in colors]
        adjusted_alpha = min(0.9, alpha + 0.1)
    
    elif material == "glass":
        # Make colors more transparent for glass material
        enhanced_colors = [lighten_color(color, 1.1) for color in colors]
        adjusted_alpha = min(0.5, alpha - 0.2)
    
    elif material == "crystal":
        # Make colors more vibrant for crystal material
        enhanced_colors = [saturate_color(color, 1.3) for color in colors]
        adjusted_alpha = min(0.7, alpha)
    
    elif material == "energy":
        # Make colors glow for energy material
        enhanced_colors = [saturate_color(color, 1.5) for color in colors]
        adjusted_alpha = min(0.8, alpha + 0.1)
    
    return enhanced_colors, adjusted_alpha

def lighten_color(color: str, factor: float) -> str:
    """
    Lighten a color by a factor.
    
    Args:
        color: Color string
        factor: Lightening factor (>1 for lighter)
        
    Returns:
        Lightened color string
    """
    rgb = mcolors.to_rgb(color)
    lightened = tuple(min(1.0, c * factor) for c in rgb)
    return mcolors.to_hex(lightened)

def saturate_color(color: str, factor: float) -> str:
    """
    Increase the saturation of a color.
    
    Args:
        color: Color string
        factor: Saturation factor (>1 for more saturated)
        
    Returns:
        Saturated color string
    """
    # Convert RGB to HSV
    rgb = mcolors.to_rgb(color)
    h, s, v = rgb_to_hsv(*rgb)
    
    # Increase saturation
    s = min(1.0, s * factor)
    
    # Convert back to RGB
    r, g, b = hsv_to_rgb(h, s, v)
    
    return mcolors.to_hex((r, g, b))

def rgb_to_hsv(r: float, g: float, b: float) -> Tuple[float, float, float]:
    """
    Convert RGB to HSV color space.
    
    Args:
        r, g, b: RGB values (0-1)
        
    Returns:
        HSV values (h: 0-1, s: 0-1, v: 0-1)
    """
    maxc = max(r, g, b)
    minc = min(r, g, b)
    v = maxc
    
    if minc == maxc:
        return 0.0, 0.0, v
    
    s = (maxc - minc) / maxc
    rc = (maxc - r) / (maxc - minc)
    gc = (maxc - g) / (maxc - minc)
    bc = (maxc - b) / (maxc - minc)
    
    if r == maxc:
        h = bc - gc
    elif g == maxc:
        h = 2.0 + rc - bc
    else:
        h = 4.0 + gc - rc
    
    h = (h / 6.0) % 1.0
    return h, s, v

def hsv_to_rgb(h: float, s: float, v: float) -> Tuple[float, float, float]:
    """
    Convert HSV to RGB color space.
    
    Args:
        h, s, v: HSV values (h: 0-1, s: 0-1, v: 0-1)
        
    Returns:
        RGB values (0-1)
    """
    if s == 0.0:
        return v, v, v
    
    i = int(h * 6.0)
    f = (h * 6.0) - i
    p = v * (1.0 - s)
    q = v * (1.0 - s * f)
    t = v * (1.0 - s * (1.0 - f))
    i %= 6
    
    if i == 0:
        return v, t, p
    elif i == 1:
        return q, v, p
    elif i == 2:
        return p, v, t
    elif i == 3:
        return p, q, v
    elif i == 4:
        return t, p, v
    else:
        return v, p, q

def plot_3d_shape_with_lighting(
    shape: Dict[str, Any],
    ax: Optional[plt.Axes] = None,
    color_scheme: str = "golden",
    material: str = "matte",
    alpha: float = 0.8,
    show_edges: bool = True,
    show_vertices: bool = False,
    light_direction: np.ndarray = np.array([1, 1, 1]),
    light_intensity: float = 1.0,
    title: Optional[str] = None
) -> plt.Axes:
    """
    Plot a 3D sacred geometry shape with enhanced lighting effects.
    
    Args:
        shape: Dictionary containing shape data (vertices, faces, etc.)
        ax: Matplotlib axes to plot on (created if None)
        color_scheme: Color scheme to use
        material: Material type (matte, metallic, glass, crystal, energy)
        alpha: Transparency value
        show_edges: Whether to show edges
        show_vertices: Whether to show vertices
        light_direction: Direction of the light source
        light_intensity: Intensity of the light
        title: Title for the plot
        
    Returns:
        The matplotlib axes with the plotted shape
    """
    from sacred_geometry.utils.color_schemes import get_color_scheme
    
    # Create axes if not provided
    if ax is None:
        fig = plt.figure(figsize=(10, 10))
        ax = fig.add_subplot(111, projection='3d')
    
    # Set dark theme for the axes
    ax.set_facecolor('#1a1a2e')
    
    # Get color scheme
    scheme = get_color_scheme(color_scheme)
    colors = scheme["colors"]
    edge_color = scheme["edge_color"]
    point_color = scheme["point_color"]
    
    # Extract vertices and faces
    vertices = shape["vertices"]
    faces = shape["faces"]
    
    # Calculate face normals
    normals = calculate_normals(vertices, faces)
    
    # Create face colors based on color scheme
    face_colors = []
    for i in range(len(faces)):
        color_idx = i % len(colors)
        face_colors.append(colors[color_idx])
    
    # Apply material enhancement
    face_colors, alpha = enhance_material(face_colors, material, alpha)
    
    # Apply lighting effects
    face_colors = apply_lighting(
        face_colors,
        normals,
        light_direction,
        ambient=0.3,
        diffuse=light_intensity * 0.7
    )
    
    # Create a list of vertices for each face
    face_vertices = [[vertices[idx] for idx in face] for face in faces]
    
    # Create Poly3DCollection
    poly3d = Poly3DCollection(
        face_vertices,
        facecolors=face_colors,
        linewidths=1 if show_edges else 0,
        edgecolors=edge_color if show_edges else 'none',
        alpha=alpha
    )
    
    # Add the collection to the axes
    ax.add_collection3d(poly3d)
    
    # Show vertices if requested
    if show_vertices:
        ax.scatter(
            vertices[:, 0], vertices[:, 1], vertices[:, 2],
            color=point_color,
            s=20,
            alpha=min(1.0, alpha + 0.2)
        )
    
    # Set axis limits to fit the shape
    max_range = np.max(vertices.max(axis=0) - vertices.min(axis=0))
    mid_x = (vertices[:, 0].min() + vertices[:, 0].max()) / 2
    mid_y = (vertices[:, 1].min() + vertices[:, 1].max()) / 2
    mid_z = (vertices[:, 2].min() + vertices[:, 2].max()) / 2
    
    ax.set_xlim(mid_x - max_range/2, mid_x + max_range/2)
    ax.set_ylim(mid_y - max_range/2, mid_y + max_range/2)
    ax.set_zlim(mid_z - max_range/2, mid_z + max_range/2)
    
    # Set equal aspect ratio
    ax.set_box_aspect([1, 1, 1])
    
    # Set title if provided
    if title:
        ax.set_title(title, color='white', fontsize=14)
    
    # Set axis labels
    ax.set_xlabel('X', color='white')
    ax.set_ylabel('Y', color='white')
    ax.set_zlabel('Z', color='white')
    
    ax.tick_params(colors='white')
    
    return ax
