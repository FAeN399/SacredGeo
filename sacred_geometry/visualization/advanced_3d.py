"""
Advanced 3D Visualization Module

This module provides enhanced 3D visualization capabilities with advanced lighting,
materials, and rendering effects for sacred geometry shapes.
"""
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import matplotlib.colors as mcolors
from typing import Dict, List, Tuple, Any, Optional, Union

# Import color schemes
from sacred_geometry.utils.color_schemes import get_color_scheme, get_material_properties

# Type aliases
Point3D = Tuple[float, float, float]
RGB = Tuple[float, float, float]
RGBA = Tuple[float, float, float, float]
ColorType = Union[str, RGB, RGBA]


def calculate_face_normals(vertices: np.ndarray, faces: List[List[int]]) -> np.ndarray:
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


def calculate_vertex_normals(vertices: np.ndarray, faces: List[List[int]]) -> np.ndarray:
    """
    Calculate the normal vectors for each vertex in a 3D shape.
    
    Args:
        vertices: Array of vertex coordinates
        faces: List of faces, each containing indices of vertices
        
    Returns:
        Array of normal vectors for each vertex
    """
    # Initialize vertex normals with zeros
    vertex_normals = np.zeros_like(vertices)
    
    # Calculate face normals
    face_normals = calculate_face_normals(vertices, faces)
    
    # For each face, add its normal to all its vertices
    for i, face in enumerate(faces):
        for vertex_idx in face:
            vertex_normals[vertex_idx] += face_normals[i]
    
    # Normalize the vertex normals
    norms = np.linalg.norm(vertex_normals, axis=1)
    valid_indices = norms > 0
    vertex_normals[valid_indices] = vertex_normals[valid_indices] / norms[valid_indices, np.newaxis]
    
    return vertex_normals


def apply_lighting(
    face_colors: np.ndarray,
    face_normals: np.ndarray,
    light_direction: np.ndarray,
    material: Dict[str, float],
    ambient_color: np.ndarray = np.array([1.0, 1.0, 1.0]),
    light_color: np.ndarray = np.array([1.0, 1.0, 1.0])
) -> np.ndarray:
    """
    Apply lighting to face colors using the Phong reflection model.
    
    Args:
        face_colors: Base colors for each face (Nx3 or Nx4 array)
        face_normals: Normal vectors for each face
        light_direction: Direction of the light source (normalized)
        material: Material properties (ambient, diffuse, specular, shininess)
        ambient_color: Color of ambient light
        light_color: Color of the light source
        
    Returns:
        Array of lit colors for each face
    """
    # Extract material properties
    ambient = material.get("ambient", 0.2)
    diffuse = material.get("diffuse", 0.7)
    specular = material.get("specular", 0.5)
    shininess = material.get("shininess", 32.0)
    
    # Normalize light direction
    light_direction = light_direction / np.linalg.norm(light_direction)
    
    # Initialize lit colors with ambient component
    lit_colors = np.zeros_like(face_colors)
    
    # Extract RGB components (handle both RGB and RGBA)
    if face_colors.shape[1] == 4:
        rgb_colors = face_colors[:, :3]
        alpha = face_colors[:, 3:4]
    else:
        rgb_colors = face_colors
        alpha = np.ones((len(face_colors), 1))
    
    # Calculate ambient component
    ambient_component = ambient * rgb_colors * ambient_color.reshape(1, 3)
    
    # Calculate diffuse component
    # Dot product of normal and light direction (clamped to 0)
    dot_products = np.maximum(0, np.sum(face_normals * light_direction, axis=1))
    diffuse_component = diffuse * rgb_colors * dot_products.reshape(-1, 1) * light_color.reshape(1, 3)
    
    # Calculate specular component (simplified)
    # For a proper specular component, we would need the view direction
    # Here we use a simplified approach assuming the view is from (0,0,1)
    view_direction = np.array([0, 0, 1])
    reflection_direction = 2 * np.outer(dot_products, face_normals) - light_direction
    reflection_direction = reflection_direction / np.linalg.norm(reflection_direction, axis=1, keepdims=True)
    spec_dot_products = np.maximum(0, np.sum(reflection_direction * view_direction, axis=1))
    specular_component = specular * np.power(spec_dot_products, shininess).reshape(-1, 1) * light_color.reshape(1, 3)
    
    # Combine components
    lit_rgb = np.minimum(1.0, ambient_component + diffuse_component + specular_component)
    
    # Recombine with alpha if needed
    if face_colors.shape[1] == 4:
        lit_colors = np.hstack((lit_rgb, alpha))
    else:
        lit_colors = lit_rgb
    
    return lit_colors


def render_3d_shape_advanced(
    shape: Dict[str, Any],
    ax: Optional[plt.Axes] = None,
    color_scheme: str = "golden",
    material: str = "matte",
    alpha: float = 0.8,
    show_edges: bool = True,
    show_vertices: bool = False,
    light_direction: np.ndarray = np.array([1, 1, 1]),
    light_intensity: float = 1.0,
    light_color: np.ndarray = np.array([1.0, 1.0, 1.0]),
    ambient_color: np.ndarray = np.array([0.2, 0.2, 0.3]),
    edge_color: Optional[str] = None,
    vertex_color: Optional[str] = None,
    edge_width: float = 0.5,
    vertex_size: float = 20,
    title: Optional[str] = None
) -> plt.Axes:
    """
    Render a 3D sacred geometry shape with advanced lighting and materials.
    
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
        light_color: Color of the light
        ambient_color: Color of ambient light
        edge_color: Color for edges (uses color scheme if None)
        vertex_color: Color for vertices (uses color scheme if None)
        edge_width: Width of edges
        vertex_size: Size of vertices
        title: Title for the plot
        
    Returns:
        The matplotlib axes with the plotted shape
    """
    # Create axes if not provided
    if ax is None:
        fig = plt.figure(figsize=(10, 10))
        ax = fig.add_subplot(111, projection='3d')
    
    # Set dark theme for the axes
    ax.set_facecolor('#1a1a2e')
    
    # Get color scheme and material properties
    scheme = get_color_scheme(color_scheme)
    mat_props = get_material_properties(material)
    
    # Adjust alpha based on material
    alpha = min(alpha, mat_props.get("alpha", 1.0))
    
    # Set default colors if not provided
    if edge_color is None:
        edge_color = scheme["edge_color"]
    if vertex_color is None:
        vertex_color = scheme["point_color"]
    
    # Extract vertices and faces
    vertices = shape["vertices"]
    faces = shape["faces"]
    
    # Calculate face and vertex normals
    face_normals = calculate_face_normals(vertices, faces)
    vertex_normals = calculate_vertex_normals(vertices, faces)
    
    # Create face colors based on color scheme
    colors = scheme["colors"]
    face_colors = []
    
    for i, face in enumerate(faces):
        # Use a color from the scheme based on face index
        color_idx = i % len(colors)
        color = mcolors.to_rgb(colors[color_idx])
        face_colors.append(color)
    
    face_colors = np.array(face_colors)
    
    # Apply lighting to face colors
    light_direction = light_direction / np.linalg.norm(light_direction)
    light_color = light_color * light_intensity
    lit_colors = apply_lighting(
        face_colors,
        face_normals,
        light_direction,
        mat_props,
        ambient_color,
        light_color
    )
    
    # Add alpha channel
    if lit_colors.shape[1] == 3:
        lit_colors = np.hstack((lit_colors, np.full((len(lit_colors), 1), alpha)))
    else:
        lit_colors[:, 3] = alpha
    
    # Create a list of vertices for each face
    face_vertices = [[vertices[idx] for idx in face] for face in faces]
    
    # Create Poly3DCollection
    poly3d = Poly3DCollection(
        face_vertices,
        facecolors=lit_colors,
        linewidths=edge_width if show_edges else 0,
        edgecolors=edge_color if show_edges else 'none',
        alpha=alpha
    )
    
    # Add the collection to the axes
    ax.add_collection3d(poly3d)
    
    # Show vertices if requested
    if show_vertices:
        ax.scatter(
            vertices[:, 0], vertices[:, 1], vertices[:, 2],
            color=vertex_color,
            s=vertex_size,
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
    
    # Remove axis labels and ticks for cleaner look
    ax.set_xlabel('X', color='white')
    ax.set_ylabel('Y', color='white')
    ax.set_zlabel('Z', color='white')
    
    ax.tick_params(colors='white')
    
    return ax


def render_multiple_shapes(
    shapes: List[Dict[str, Any]],
    colors: List[str] = None,
    materials: List[str] = None,
    alphas: List[float] = None,
    ax: Optional[plt.Axes] = None,
    light_direction: np.ndarray = np.array([1, 1, 1]),
    light_intensity: float = 1.0,
    show_edges: bool = True,
    title: Optional[str] = None
) -> plt.Axes:
    """
    Render multiple 3D shapes with different colors and materials.
    
    Args:
        shapes: List of shape dictionaries
        colors: List of color schemes for each shape
        materials: List of materials for each shape
        alphas: List of alpha values for each shape
        ax: Matplotlib axes to plot on (created if None)
        light_direction: Direction of the light source
        light_intensity: Intensity of the light
        show_edges: Whether to show edges
        title: Title for the plot
        
    Returns:
        The matplotlib axes with the plotted shapes
    """
    # Create axes if not provided
    if ax is None:
        fig = plt.figure(figsize=(10, 10))
        ax = fig.add_subplot(111, projection='3d')
    
    # Set dark theme for the axes
    ax.set_facecolor('#1a1a2e')
    
    # Set default values if not provided
    if colors is None:
        colors = ["golden"] * len(shapes)
    elif isinstance(colors, str):
        colors = [colors] * len(shapes)
    
    if materials is None:
        materials = ["matte"] * len(shapes)
    elif isinstance(materials, str):
        materials = [materials] * len(shapes)
    
    if alphas is None:
        alphas = [0.8] * len(shapes)
    elif isinstance(alphas, (int, float)):
        alphas = [alphas] * len(shapes)
    
    # Ensure lists are the right length
    colors = colors[:len(shapes)] + ["golden"] * max(0, len(shapes) - len(colors))
    materials = materials[:len(shapes)] + ["matte"] * max(0, len(shapes) - len(materials))
    alphas = alphas[:len(shapes)] + [0.8] * max(0, len(shapes) - len(alphas))
    
    # Collect all vertices to set axis limits
    all_vertices = []
    
    # Render each shape
    for i, shape in enumerate(shapes):
        # Extract vertices for axis limits calculation
        vertices = shape["vertices"]
        all_vertices.append(vertices)
        
        # Render the shape
        render_3d_shape_advanced(
            shape,
            ax=ax,
            color_scheme=colors[i],
            material=materials[i],
            alpha=alphas[i],
            show_edges=show_edges,
            show_vertices=False,
            light_direction=light_direction,
            light_intensity=light_intensity
        )
    
    # Set axis limits to fit all shapes
    if all_vertices:
        all_vertices = np.vstack(all_vertices)
        max_range = np.max(all_vertices.max(axis=0) - all_vertices.min(axis=0))
        mid_x = (all_vertices[:, 0].min() + all_vertices[:, 0].max()) / 2
        mid_y = (all_vertices[:, 1].min() + all_vertices[:, 1].max()) / 2
        mid_z = (all_vertices[:, 2].min() + all_vertices[:, 2].max()) / 2
        
        ax.set_xlim(mid_x - max_range/2, mid_x + max_range/2)
        ax.set_ylim(mid_y - max_range/2, mid_y + max_range/2)
        ax.set_zlim(mid_z - max_range/2, mid_z + max_range/2)
    
    # Set equal aspect ratio
    ax.set_box_aspect([1, 1, 1])
    
    # Set title if provided
    if title:
        ax.set_title(title, color='white', fontsize=14)
    
    # Remove axis labels and ticks for cleaner look
    ax.set_xlabel('X', color='white')
    ax.set_ylabel('Y', color='white')
    ax.set_zlabel('Z', color='white')
    
    ax.tick_params(colors='white')
    
    return ax
