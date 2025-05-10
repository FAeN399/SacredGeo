"""
Sacred Geometry Exporters Module

This module provides functions to export sacred geometry patterns and shapes
to various file formats, including:
- 2D formats: PNG, SVG, PDF
- 3D formats: OBJ, STL, GLTF
- Animation formats: GIF, MP4

It also includes utilities for preparing models for 3D printing and
high-resolution rendering.
"""
import os
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from typing import Dict, List, Tuple, Any, Optional, Union
import json
import datetime

# For 3D exports
try:
    import trimesh
    TRIMESH_AVAILABLE = True
except ImportError:
    TRIMESH_AVAILABLE = False
    print("Warning: trimesh not available. 3D exports will be limited.")

# For SVG exports
try:
    from svgwrite import Drawing
    SVG_AVAILABLE = True
except ImportError:
    SVG_AVAILABLE = False
    print("Warning: svgwrite not available. SVG export will not be available.")

# For animation exports
try:
    from PIL import Image
    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False
    print("Warning: PIL not available. GIF export will be limited.")


def export_2d_image(
    fig: Figure,
    filename: str,
    dpi: int = 300,
    transparent: bool = False,
    format: str = "png",
    **kwargs
) -> str:
    """
    Export a matplotlib figure as an image file.

    Args:
        fig: The matplotlib figure to export
        filename: Output filename (with or without extension)
        dpi: Resolution in dots per inch
        transparent: Whether to use a transparent background
        format: File format (png, jpg, pdf, etc.)
        **kwargs: Additional arguments to pass to fig.savefig()

    Returns:
        The full path to the saved file
    """
    # Ensure the filename has the correct extension
    if not filename.lower().endswith(f".{format.lower()}"):
        filename = f"{filename}.{format.lower()}"

    # Create directory if it doesn't exist
    os.makedirs(os.path.dirname(os.path.abspath(filename)), exist_ok=True)

    # Save the figure
    fig.savefig(
        filename,
        dpi=dpi,
        transparent=transparent,
        format=format,
        bbox_inches='tight',
        **kwargs
    )

    print(f"Image saved to {filename}")
    return os.path.abspath(filename)


def export_svg(
    pattern: Any,
    filename: str,
    width: str = "800px",
    height: str = "800px",
    background_color: Optional[str] = "#1a1a2e",
    line_color: str = "#daa520",
    line_width: float = 1.0,
    point_color: str = "#e6e6fa",
    point_size: float = 3.0,
    show_points: bool = False,
    scale_factor: float = 100.0
) -> str:
    """
    Export a sacred geometry pattern as an SVG file.

    Args:
        pattern: The pattern to export (various formats supported)
        filename: Output filename (with or without extension)
        width, height: Dimensions of the SVG
        background_color: Background color (None for transparent)
        line_color: Color for lines
        line_width: Width of lines
        point_color: Color for points
        point_size: Size of points
        show_points: Whether to show points/vertices
        scale_factor: Factor to scale the pattern by

    Returns:
        The full path to the saved file
    """
    if not SVG_AVAILABLE:
        raise ImportError("svgwrite is required for SVG export. Install with 'pip install svgwrite'")

    # Ensure the filename has the correct extension
    if not filename.lower().endswith(".svg"):
        filename = f"{filename}.svg"

    # Create directory if it doesn't exist
    os.makedirs(os.path.dirname(os.path.abspath(filename)), exist_ok=True)

    # Create SVG drawing
    dwg = Drawing(filename, size=(width, height), profile='tiny')

    # Add background if specified
    if background_color:
        dwg.add(dwg.rect(insert=(0, 0), size=('100%', '100%'), fill=background_color))

    # Calculate center offset for the drawing
    width_px = int(width.replace('px', ''))
    height_px = int(height.replace('px', ''))
    center_x = width_px / 2
    center_y = height_px / 2

    # Process the pattern based on its type
    if isinstance(pattern, list) and len(pattern) > 0 and isinstance(pattern[0], np.ndarray):
        # List of circles (like Flower of Life)
        for circle in pattern:
            points = [(p[0] * scale_factor + center_x, p[1] * scale_factor + center_y) for p in circle]
            dwg.add(dwg.polyline(points=points, stroke=line_color, fill='none', stroke_width=line_width))

            if show_points and len(circle) > 0:
                dwg.add(dwg.circle(center=(points[0][0], points[0][1]), r=point_size, fill=point_color))

    elif isinstance(pattern, dict):
        # Dictionary with different components

        # Process circles
        for key in ['circle', 'circle1', 'circle2', 'circles']:
            if key in pattern:
                circles = pattern[key] if key == 'circles' else [pattern[key]]
                if not isinstance(circles, list):
                    circles = [circles]

                for circle in circles:
                    points = [(p[0] * scale_factor + center_x, p[1] * scale_factor + center_y) for p in circle]
                    dwg.add(dwg.polyline(points=points, stroke=line_color, fill='none', stroke_width=line_width))

        # Process lines
        if 'lines' in pattern:
            for line in pattern['lines']:
                x1, y1 = line[0][0] * scale_factor + center_x, line[0][1] * scale_factor + center_y
                x2, y2 = line[1][0] * scale_factor + center_x, line[1][1] * scale_factor + center_y
                dwg.add(dwg.line(start=(x1, y1), end=(x2, y2), stroke=line_color, stroke_width=line_width))

        # Process points
        if show_points:
            for key in ['vertices', 'intersection_points']:
                if key in pattern:
                    points = pattern[key]
                    if len(points) > 0:
                        for point in points:
                            x, y = point[0] * scale_factor + center_x, point[1] * scale_factor + center_y
                            dwg.add(dwg.circle(center=(x, y), r=point_size, fill=point_color))

        # Process spiral
        if 'spiral' in pattern:
            spiral = pattern['spiral']
            if len(spiral) > 0:
                points = [(p[0] * scale_factor + center_x, p[1] * scale_factor + center_y) for p in spiral]
                dwg.add(dwg.polyline(points=points, stroke=line_color, fill='none', stroke_width=line_width))

    elif isinstance(pattern, np.ndarray):
        # Single shape like a polygon
        points = [(p[0] * scale_factor + center_x, p[1] * scale_factor + center_y) for p in pattern]
        # Close the shape by adding the first point again
        points.append(points[0])
        dwg.add(dwg.polyline(points=points, stroke=line_color, fill='none', stroke_width=line_width))

        if show_points:
            for point in points[:-1]:  # Skip the last point which is a duplicate of the first
                dwg.add(dwg.circle(center=point, r=point_size, fill=point_color))

    # Save the SVG
    dwg.save()

    print(f"SVG saved to {filename}")
    return os.path.abspath(filename)


def export_3d_obj(
    shape: Dict[str, Any],
    filename: str,
    scale: float = 1.0,
    include_normals: bool = True,
    include_materials: bool = True
) -> str:
    """
    Export a 3D sacred geometry shape as an OBJ file.

    Args:
        shape: Dictionary containing shape data (vertices, faces, etc.)
        filename: Output filename (with or without extension)
        scale: Scale factor for the model
        include_normals: Whether to include normal vectors
        include_materials: Whether to include material definitions

    Returns:
        The full path to the saved file
    """
    # Ensure the filename has the correct extension
    if not filename.lower().endswith(".obj"):
        filename = f"{filename}.obj"

    # Create directory if it doesn't exist
    os.makedirs(os.path.dirname(os.path.abspath(filename)), exist_ok=True)

    # Check if shape has the required data
    if 'vertices' not in shape:
        if 'tetrahedron1' in shape and 'tetrahedron2' in shape:
            # Special case for Merkaba (two tetrahedra)
            return export_merkaba_obj(shape, filename, scale, include_normals, include_materials)
        elif 'spheres' in shape:
            # Special case for 3D Flower of Life (spheres)
            return export_spheres_obj(shape, filename, scale, include_normals, include_materials)
        else:
            raise ValueError("Shape does not contain vertices data")

    vertices = shape['vertices'] * scale

    # Determine which faces to use
    if 'faces' in shape:
        faces = shape['faces']
    elif 'triangular_faces' in shape and 'square_faces' in shape:
        # For shapes like cuboctahedron with different face types
        faces = shape['triangular_faces'] + shape['square_faces']
    else:
        raise ValueError("Shape does not contain faces data")

    # Write OBJ file
    with open(filename, 'w') as f:
        # Write header
        f.write(f"# Sacred Geometry OBJ Export\n")
        f.write(f"# Generated on {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"# Vertices: {len(vertices)}, Faces: {len(faces)}\n\n")

        # Write material library reference if including materials
        if include_materials:
            mtl_filename = os.path.splitext(os.path.basename(filename))[0] + ".mtl"
            f.write(f"mtllib {mtl_filename}\n\n")
            f.write(f"g SacredGeometry\n")
            f.write(f"usemtl SacredGeometryMaterial\n\n")

        # Write vertices
        for v in vertices:
            f.write(f"v {v[0]:.6f} {v[1]:.6f} {v[2]:.6f}\n")

        # Write normals if requested
        if include_normals:
            # Calculate face normals
            for face in faces:
                if len(face) >= 3:  # Need at least 3 vertices to calculate normal
                    v0 = vertices[face[0]]
                    v1 = vertices[face[1]]
                    v2 = vertices[face[2]]

                    # Calculate normal using cross product
                    edge1 = v1 - v0
                    edge2 = v2 - v0
                    normal = np.cross(edge1, edge2)

                    # Normalize
                    norm = np.linalg.norm(normal)
                    if norm > 0:
                        normal = normal / norm
                        f.write(f"vn {normal[0]:.6f} {normal[1]:.6f} {normal[2]:.6f}\n")

        f.write("\n")

        # Write faces (OBJ uses 1-indexed vertices)
        for face in faces:
            # Convert face indices to 1-indexed
            face_str = " ".join([str(idx + 1) for idx in face])
            f.write(f"f {face_str}\n")

    # Create MTL file if including materials
    if include_materials:
        mtl_path = os.path.join(os.path.dirname(filename), mtl_filename)
        with open(mtl_path, 'w') as f:
            f.write(f"# Sacred Geometry Material\n")
            f.write(f"# Generated on {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")

            f.write(f"newmtl SacredGeometryMaterial\n")
            f.write(f"Ka 0.2 0.2 0.2\n")  # Ambient color
            f.write(f"Kd 0.8 0.7 0.2\n")  # Diffuse color (golden)
            f.write(f"Ks 1.0 1.0 1.0\n")  # Specular color
            f.write(f"Ns 100.0\n")        # Specular exponent
            f.write(f"d 0.7\n")           # Transparency (0.7 = slightly transparent)
            f.write(f"illum 2\n")         # Illumination model

    print(f"OBJ saved to {filename}")
    return os.path.abspath(filename)


def export_merkaba_obj(
    merkaba: Dict[str, Any],
    filename: str,
    scale: float = 1.0,
    include_normals: bool = True,
    include_materials: bool = True
) -> str:
    """
    Export a Merkaba (Star Tetrahedron) as an OBJ file.

    Args:
        merkaba: Dictionary containing two tetrahedra
        filename: Output filename
        scale: Scale factor
        include_normals: Whether to include normal vectors
        include_materials: Whether to include material definitions

    Returns:
        The full path to the saved file
    """
    # Ensure the filename has the correct extension
    if not filename.lower().endswith(".obj"):
        filename = f"{filename}.obj"

    # Create directory if it doesn't exist
    os.makedirs(os.path.dirname(os.path.abspath(filename)), exist_ok=True)

    tetra1 = merkaba['tetrahedron1']
    tetra2 = merkaba['tetrahedron2']

    vertices1 = tetra1['vertices'] * scale
    vertices2 = tetra2['vertices'] * scale
    faces1 = tetra1['faces']
    faces2 = tetra2['faces']

    # Write OBJ file
    with open(filename, 'w') as f:
        # Write header
        f.write(f"# Sacred Geometry Merkaba OBJ Export\n")
        f.write(f"# Generated on {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"# Total Vertices: {len(vertices1) + len(vertices2)}, Faces: {len(faces1) + len(faces2)}\n\n")

        # Write material library reference if including materials
        if include_materials:
            mtl_filename = os.path.splitext(os.path.basename(filename))[0] + ".mtl"
            f.write(f"mtllib {mtl_filename}\n\n")

        # Write first tetrahedron
        f.write(f"g Tetrahedron1\n")
        if include_materials:
            f.write(f"usemtl Tetrahedron1Material\n")

        # Write vertices for first tetrahedron
        for v in vertices1:
            f.write(f"v {v[0]:.6f} {v[1]:.6f} {v[2]:.6f}\n")

        # Write second tetrahedron
        f.write(f"g Tetrahedron2\n")
        if include_materials:
            f.write(f"usemtl Tetrahedron2Material\n")

        # Write vertices for second tetrahedron
        for v in vertices2:
            f.write(f"v {v[0]:.6f} {v[1]:.6f} {v[2]:.6f}\n")

        # Write normals if requested
        if include_normals:
            # Calculate and write normals for first tetrahedron
            for face in faces1:
                if len(face) >= 3:
                    v0 = vertices1[face[0]]
                    v1 = vertices1[face[1]]
                    v2 = vertices1[face[2]]

                    edge1 = v1 - v0
                    edge2 = v2 - v0
                    normal = np.cross(edge1, edge2)

                    norm = np.linalg.norm(normal)
                    if norm > 0:
                        normal = normal / norm
                        f.write(f"vn {normal[0]:.6f} {normal[1]:.6f} {normal[2]:.6f}\n")

            # Calculate and write normals for second tetrahedron
            for face in faces2:
                if len(face) >= 3:
                    v0 = vertices2[face[0]]
                    v1 = vertices2[face[1]]
                    v2 = vertices2[face[2]]

                    edge1 = v1 - v0
                    edge2 = v2 - v0
                    normal = np.cross(edge1, edge2)

                    norm = np.linalg.norm(normal)
                    if norm > 0:
                        normal = normal / norm
                        f.write(f"vn {normal[0]:.6f} {normal[1]:.6f} {normal[2]:.6f}\n")

        f.write("\n")

        # Write faces for first tetrahedron (OBJ uses 1-indexed vertices)
        f.write(f"g Tetrahedron1\n")
        for face in faces1:
            face_str = " ".join([str(idx + 1) for idx in face])
            f.write(f"f {face_str}\n")

        # Write faces for second tetrahedron
        # Need to offset indices by the number of vertices in the first tetrahedron
        f.write(f"g Tetrahedron2\n")
        offset = len(vertices1)
        for face in faces2:
            face_str = " ".join([str(idx + 1 + offset) for idx in face])
            f.write(f"f {face_str}\n")

    # Create MTL file if including materials
    if include_materials:
        mtl_path = os.path.join(os.path.dirname(filename), mtl_filename)
        with open(mtl_path, 'w') as f:
            f.write(f"# Sacred Geometry Merkaba Materials\n")
            f.write(f"# Generated on {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")

            # Material for first tetrahedron (golden)
            f.write(f"newmtl Tetrahedron1Material\n")
            f.write(f"Ka 0.2 0.2 0.2\n")
            f.write(f"Kd 0.8 0.7 0.2\n")
            f.write(f"Ks 1.0 1.0 1.0\n")
            f.write(f"Ns 100.0\n")
            f.write(f"d 0.7\n")
            f.write(f"illum 2\n\n")

            # Material for second tetrahedron (silver-blue)
            f.write(f"newmtl Tetrahedron2Material\n")
            f.write(f"Ka 0.2 0.2 0.2\n")
            f.write(f"Kd 0.2 0.4 0.8\n")
            f.write(f"Ks 1.0 1.0 1.0\n")
            f.write(f"Ns 100.0\n")
            f.write(f"d 0.7\n")
            f.write(f"illum 2\n")

    print(f"Merkaba OBJ saved to {filename}")
    return os.path.abspath(filename)


def export_spheres_obj(
    flower_of_life_3d: Dict[str, Any],
    filename: str,
    scale: float = 1.0,
    include_normals: bool = True,
    include_materials: bool = True
) -> str:
    """
    Export a 3D Flower of Life (spheres) as an OBJ file.

    Args:
        flower_of_life_3d: Dictionary containing spheres data
        filename: Output filename
        scale: Scale factor
        include_normals: Whether to include normal vectors
        include_materials: Whether to include material definitions

    Returns:
        The full path to the saved file
    """
    # Ensure the filename has the correct extension
    if not filename.lower().endswith(".obj"):
        filename = f"{filename}.obj"

    # Create directory if it doesn't exist
    os.makedirs(os.path.dirname(os.path.abspath(filename)), exist_ok=True)

    spheres = flower_of_life_3d['spheres']

    # Write OBJ file
    with open(filename, 'w') as f:
        # Write header
        f.write(f"# Sacred Geometry 3D Flower of Life OBJ Export\n")
        f.write(f"# Generated on {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"# Spheres: {len(spheres)}\n\n")

        # Write material library reference if including materials
        if include_materials:
            mtl_filename = os.path.splitext(os.path.basename(filename))[0] + ".mtl"
            f.write(f"mtllib {mtl_filename}\n\n")

        vertex_offset = 0

        # For each sphere, generate a UV sphere
        for i, sphere in enumerate(spheres):
            center = np.array(sphere['center']) * scale
            radius = sphere['radius'] * scale

            # Generate a UV sphere
            resolution = 16  # Number of segments
            vertices, faces = _generate_uv_sphere(center, radius, resolution)

            # Write sphere
            f.write(f"g Sphere{i+1}\n")
            if include_materials:
                f.write(f"usemtl SphereMaterial\n")

            # Write vertices
            for v in vertices:
                f.write(f"v {v[0]:.6f} {v[1]:.6f} {v[2]:.6f}\n")

            # Write normals if requested
            if include_normals:
                for v in vertices:
                    # For a sphere, the normal at each vertex is just the normalized
                    # vector from the center to the vertex
                    normal = v - center
                    norm = np.linalg.norm(normal)
                    if norm > 0:
                        normal = normal / norm
                        f.write(f"vn {normal[0]:.6f} {normal[1]:.6f} {normal[2]:.6f}\n")

            f.write("\n")

            # Write faces (OBJ uses 1-indexed vertices)
            for face in faces:
                # Offset indices by the current vertex offset
                face_str = " ".join([str(idx + 1 + vertex_offset) for idx in face])
                f.write(f"f {face_str}\n")

            # Update vertex offset for the next sphere
            vertex_offset += len(vertices)

    # Create MTL file if including materials
    if include_materials:
        mtl_path = os.path.join(os.path.dirname(filename), mtl_filename)
        with open(mtl_path, 'w') as f:
            f.write(f"# Sacred Geometry 3D Flower of Life Materials\n")
            f.write(f"# Generated on {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")

            # Material for spheres (translucent blue)
            f.write(f"newmtl SphereMaterial\n")
            f.write(f"Ka 0.1 0.1 0.2\n")
            f.write(f"Kd 0.3 0.5 0.8\n")
            f.write(f"Ks 0.8 0.8 1.0\n")
            f.write(f"Ns 50.0\n")
            f.write(f"d 0.4\n")
            f.write(f"illum 2\n")

    print(f"3D Flower of Life OBJ saved to {filename}")
    return os.path.abspath(filename)


def _generate_uv_sphere(center: np.ndarray, radius: float, resolution: int) -> Tuple[np.ndarray, List[List[int]]]:
    """
    Generate vertices and faces for a UV sphere.

    Args:
        center: Center of the sphere
        radius: Radius of the sphere
        resolution: Number of segments (higher = smoother)

    Returns:
        Tuple of (vertices, faces)
    """
    vertices = []
    faces = []

    # Generate vertices
    for i in range(resolution + 1):
        theta = i * np.pi / resolution
        sin_theta = np.sin(theta)
        cos_theta = np.cos(theta)

        for j in range(resolution * 2):
            phi = j * 2 * np.pi / (resolution * 2)
            sin_phi = np.sin(phi)
            cos_phi = np.cos(phi)

            x = center[0] + radius * sin_theta * cos_phi
            y = center[1] + radius * sin_theta * sin_phi
            z = center[2] + radius * cos_theta

            vertices.append(np.array([x, y, z]))

    # Generate faces
    for i in range(resolution):
        for j in range(resolution * 2):
            next_j = (j + 1) % (resolution * 2)

            # Current ring indices
            current = i * (resolution * 2) + j
            current_next = i * (resolution * 2) + next_j

            # Next ring indices
            next_ring = (i + 1) * (resolution * 2) + j
            next_ring_next = (i + 1) * (resolution * 2) + next_j

            # Add two triangular faces
            if i < resolution - 1:  # Not at the pole
                faces.append([current, next_ring, next_ring_next])
                faces.append([current, next_ring_next, current_next])

    return np.array(vertices), faces


def export_stl(
    shape: Dict[str, Any],
    filename: str,
    scale: float = 1.0,
    binary: bool = True
) -> str:
    """
    Export a 3D sacred geometry shape as an STL file.

    Args:
        shape: Dictionary containing shape data (vertices, faces, etc.)
        filename: Output filename (with or without extension)
        scale: Scale factor for the model
        binary: Whether to use binary STL format (more compact)

    Returns:
        The full path to the saved file
    """
    if not TRIMESH_AVAILABLE:
        raise ImportError("trimesh is required for STL export. Install with 'pip install trimesh'")

    # Ensure the filename has the correct extension
    if not filename.lower().endswith(".stl"):
        filename = f"{filename}.stl"

    # Create directory if it doesn't exist
    os.makedirs(os.path.dirname(os.path.abspath(filename)), exist_ok=True)

    # Check if shape has the required data
    if 'vertices' not in shape:
        if 'tetrahedron1' in shape and 'tetrahedron2' in shape:
            # Special case for Merkaba (two tetrahedra)
            return export_merkaba_stl(shape, filename, scale, binary)
        elif 'spheres' in shape:
            # Special case for 3D Flower of Life (spheres)
            return export_spheres_stl(shape, filename, scale, binary)
        else:
            raise ValueError("Shape does not contain vertices data")

    vertices = shape['vertices'] * scale

    # Determine which faces to use
    if 'faces' in shape:
        faces = shape['faces']
    elif 'triangular_faces' in shape and 'square_faces' in shape:
        # For shapes like cuboctahedron with different face types
        # STL requires triangular faces, so we need to triangulate any non-triangular faces
        triangular_faces = shape['triangular_faces']
        square_faces = shape['square_faces']

        # Triangulate square faces (split each square into two triangles)
        triangulated_squares = []
        for face in square_faces:
            if len(face) == 4:
                triangulated_squares.append([face[0], face[1], face[2]])
                triangulated_squares.append([face[0], face[2], face[3]])
            else:
                # If not a square, just add as is (though this shouldn't happen)
                triangulated_squares.append(face)

        faces = triangular_faces + triangulated_squares
    else:
        raise ValueError("Shape does not contain faces data")

    # Ensure all faces are triangular for STL
    triangular_faces = []
    for face in faces:
        if len(face) == 3:
            triangular_faces.append(face)
        elif len(face) > 3:
            # Simple triangulation by creating a fan from the first vertex
            for i in range(1, len(face) - 1):
                triangular_faces.append([face[0], face[i], face[i+1]])

    # Create a trimesh mesh
    mesh = trimesh.Trimesh(
        vertices=vertices,
        faces=np.array(triangular_faces),
        process=True  # Process the mesh to fix normals, etc.
    )

    # Export to STL
    mesh.export(filename, file_type='stl_binary' if binary else 'stl_ascii')

    print(f"STL saved to {filename}")
    return os.path.abspath(filename)


def export_merkaba_stl(
    merkaba: Dict[str, Any],
    filename: str,
    scale: float = 1.0,
    binary: bool = True
) -> str:
    """
    Export a Merkaba (Star Tetrahedron) as an STL file.

    Args:
        merkaba: Dictionary containing two tetrahedra
        filename: Output filename
        scale: Scale factor
        binary: Whether to use binary STL format

    Returns:
        The full path to the saved file
    """
    if not TRIMESH_AVAILABLE:
        raise ImportError("trimesh is required for STL export. Install with 'pip install trimesh'")

    # Ensure the filename has the correct extension
    if not filename.lower().endswith(".stl"):
        filename = f"{filename}.stl"

    # Create directory if it doesn't exist
    os.makedirs(os.path.dirname(os.path.abspath(filename)), exist_ok=True)

    tetra1 = merkaba['tetrahedron1']
    tetra2 = merkaba['tetrahedron2']

    vertices1 = tetra1['vertices'] * scale
    vertices2 = tetra2['vertices'] * scale
    faces1 = tetra1['faces']
    faces2 = tetra2['faces']

    # Create a trimesh mesh for each tetrahedron
    mesh1 = trimesh.Trimesh(
        vertices=vertices1,
        faces=np.array(faces1),
        process=True
    )

    mesh2 = trimesh.Trimesh(
        vertices=vertices2,
        faces=np.array(faces2),
        process=True
    )

    # Combine the meshes
    combined_mesh = trimesh.util.concatenate([mesh1, mesh2])

    # Export to STL
    combined_mesh.export(filename, file_type='stl_binary' if binary else 'stl_ascii')

    print(f"Merkaba STL saved to {filename}")
    return os.path.abspath(filename)


def export_spheres_stl(
    flower_of_life_3d: Dict[str, Any],
    filename: str,
    scale: float = 1.0,
    binary: bool = True
) -> str:
    """
    Export a 3D Flower of Life (spheres) as an STL file.

    Args:
        flower_of_life_3d: Dictionary containing spheres data
        filename: Output filename
        scale: Scale factor
        binary: Whether to use binary STL format

    Returns:
        The full path to the saved file
    """
    if not TRIMESH_AVAILABLE:
        raise ImportError("trimesh is required for STL export. Install with 'pip install trimesh'")

    # Ensure the filename has the correct extension
    if not filename.lower().endswith(".stl"):
        filename = f"{filename}.stl"

    # Create directory if it doesn't exist
    os.makedirs(os.path.dirname(os.path.abspath(filename)), exist_ok=True)

    spheres = flower_of_life_3d['spheres']
    meshes = []

    # Create a sphere mesh for each sphere
    for sphere in spheres:
        center = np.array(sphere['center']) * scale
        radius = sphere['radius'] * scale

        # Create a sphere mesh
        sphere_mesh = trimesh.creation.icosphere(radius=radius, subdivisions=2)

        # Translate to the correct position
        sphere_mesh.apply_translation(center)

        meshes.append(sphere_mesh)

    # Combine all sphere meshes
    if meshes:
        combined_mesh = trimesh.util.concatenate(meshes)

        # Export to STL
        combined_mesh.export(filename, file_type='stl_binary' if binary else 'stl_ascii')

        print(f"3D Flower of Life STL saved to {filename}")
        return os.path.abspath(filename)
    else:
        raise ValueError("No spheres found in the 3D Flower of Life data")


def export_animation_gif(
    frames: List[np.ndarray],
    filename: str,
    fps: int = 15,
    loop: int = 0,
    optimize: bool = True,
    dpi: int = 100
) -> str:
    """
    Export a sequence of frames as an animated GIF.

    Args:
        frames: List of numpy arrays representing the frames
        filename: Output filename (with or without extension)
        fps: Frames per second
        loop: Number of times to loop (0 = infinite)
        optimize: Whether to optimize the GIF
        dpi: Resolution in dots per inch

    Returns:
        The full path to the saved file
    """
    if not PIL_AVAILABLE:
        raise ImportError("PIL is required for GIF export. Install with 'pip install pillow'")

    # Ensure the filename has the correct extension
    if not filename.lower().endswith(".gif"):
        filename = f"{filename}.gif"

    # Create directory if it doesn't exist
    os.makedirs(os.path.dirname(os.path.abspath(filename)), exist_ok=True)

    # Convert frames to PIL images
    pil_frames = []
    for frame in frames:
        # Convert numpy array to PIL Image
        img = Image.fromarray(frame)
        pil_frames.append(img)

    # Calculate duration in milliseconds
    duration = int(1000 / fps)

    # Save as GIF
    pil_frames[0].save(
        filename,
        save_all=True,
        append_images=pil_frames[1:],
        optimize=optimize,
        duration=duration,
        loop=loop
    )

    print(f"GIF saved to {filename}")
    return os.path.abspath(filename)


def export_animation_from_figure_sequence(
    fig_sequence: List[Figure],
    filename: str,
    fps: int = 15,
    dpi: int = 100
) -> str:
    """
    Export a sequence of matplotlib figures as an animated GIF.

    Args:
        fig_sequence: List of matplotlib figures
        filename: Output filename (with or without extension)
        fps: Frames per second
        dpi: Resolution in dots per inch

    Returns:
        The full path to the saved file
    """
    if not PIL_AVAILABLE:
        raise ImportError("PIL is required for GIF export. Install with 'pip install pillow'")

    # Ensure the filename has the correct extension
    if not filename.lower().endswith(".gif"):
        filename = f"{filename}.gif"

    # Create directory if it doesn't exist
    os.makedirs(os.path.dirname(os.path.abspath(filename)), exist_ok=True)

    # Convert figures to PIL images
    pil_frames = []
    for fig in fig_sequence:
        # Convert figure to numpy array
        fig.canvas.draw()
        data = np.frombuffer(fig.canvas.tostring_rgb(), dtype=np.uint8)
        data = data.reshape(fig.canvas.get_width_height()[::-1] + (3,))

        # Convert numpy array to PIL Image
        img = Image.fromarray(data)
        pil_frames.append(img)

    # Calculate duration in milliseconds
    duration = int(1000 / fps)

    # Save as GIF
    pil_frames[0].save(
        filename,
        save_all=True,
        append_images=pil_frames[1:],
        optimize=True,
        duration=duration,
        loop=0
    )

    print(f"GIF saved to {filename}")
    return os.path.abspath(filename)


def export_for_3d_printing(
    shape: Dict[str, Any],
    filename: str,
    scale: float = 1.0,
    wall_thickness: float = 0.1,
    solid: bool = False,
    format: str = "stl"
) -> str:
    """
    Export a 3D sacred geometry shape optimized for 3D printing.

    Args:
        shape: Dictionary containing shape data
        filename: Output filename
        scale: Scale factor for the model
        wall_thickness: Thickness of walls for hollow models
        solid: Whether to create a solid model (True) or hollow (False)
        format: Output format ('stl' or 'obj')

    Returns:
        The full path to the saved file
    """
    if not TRIMESH_AVAILABLE:
        raise ImportError("trimesh is required for 3D printing export. Install with 'pip install trimesh'")

    # Ensure the filename has the correct extension
    if format.lower() not in ['stl', 'obj']:
        raise ValueError("Format must be 'stl' or 'obj'")

    if not filename.lower().endswith(f".{format.lower()}"):
        filename = f"{filename}.{format.lower()}"

    # Create directory if it doesn't exist
    os.makedirs(os.path.dirname(os.path.abspath(filename)), exist_ok=True)

    # Process the shape based on its type
    if 'tetrahedron1' in shape and 'tetrahedron2' in shape:
        # Merkaba case
        return export_merkaba_for_3d_printing(shape, filename, scale, wall_thickness, solid, format)
    elif 'spheres' in shape:
        # 3D Flower of Life case
        return export_spheres_for_3d_printing(shape, filename, scale, wall_thickness, solid, format)
    elif 'vertices' in shape and ('faces' in shape or 'triangular_faces' in shape):
        # Regular polyhedron case
        vertices = shape['vertices'] * scale

        # Determine which faces to use
        if 'faces' in shape:
            faces = shape['faces']
        elif 'triangular_faces' in shape and 'square_faces' in shape:
            # Triangulate square faces
            triangular_faces = shape['triangular_faces']
            square_faces = shape['square_faces']

            triangulated_squares = []
            for face in square_faces:
                if len(face) == 4:
                    triangulated_squares.append([face[0], face[1], face[2]])
                    triangulated_squares.append([face[0], face[2], face[3]])
                else:
                    triangulated_squares.append(face)

            faces = triangular_faces + triangulated_squares
        else:
            raise ValueError("Shape does not contain faces data")

        # Ensure all faces are triangular
        triangular_faces = []
        for face in faces:
            if len(face) == 3:
                triangular_faces.append(face)
            elif len(face) > 3:
                for i in range(1, len(face) - 1):
                    triangular_faces.append([face[0], face[i], face[i+1]])

        # Create a trimesh mesh
        mesh = trimesh.Trimesh(
            vertices=vertices,
            faces=np.array(triangular_faces),
            process=True
        )

        if not solid:
            # Create a hollow version with wall thickness
            # This is a simplified approach - for complex shapes, more sophisticated
            # hollowing algorithms would be needed
            try:
                # Inward offset to create inner shell
                inner_mesh = mesh.copy()
                inner_mesh.vertices -= inner_mesh.vertex_normals * wall_thickness

                # Flip normals of inner mesh
                inner_mesh.invert()

                # Combine outer and inner meshes
                combined_mesh = trimesh.util.concatenate([mesh, inner_mesh])

                # Export the combined mesh
                combined_mesh.export(filename)
            except Exception as e:
                print(f"Warning: Could not create hollow model: {e}. Exporting solid model instead.")
                mesh.export(filename)
        else:
            # Export solid model
            mesh.export(filename)

        print(f"3D printing model saved to {filename}")
        return os.path.abspath(filename)
    else:
        raise ValueError("Unsupported shape type for 3D printing export")


def export_merkaba_for_3d_printing(
    merkaba: Dict[str, Any],
    filename: str,
    scale: float = 1.0,
    wall_thickness: float = 0.1,
    solid: bool = False,
    format: str = "stl"
) -> str:
    """
    Export a Merkaba optimized for 3D printing.

    Args:
        merkaba: Dictionary containing two tetrahedra
        filename: Output filename
        scale: Scale factor
        wall_thickness: Thickness of walls for hollow models
        solid: Whether to create a solid model
        format: Output format

    Returns:
        The full path to the saved file
    """
    if not TRIMESH_AVAILABLE:
        raise ImportError("trimesh is required for 3D printing export")

    tetra1 = merkaba['tetrahedron1']
    tetra2 = merkaba['tetrahedron2']

    vertices1 = tetra1['vertices'] * scale
    vertices2 = tetra2['vertices'] * scale
    faces1 = tetra1['faces']
    faces2 = tetra2['faces']

    # Create trimesh meshes
    mesh1 = trimesh.Trimesh(
        vertices=vertices1,
        faces=np.array(faces1),
        process=True
    )

    mesh2 = trimesh.Trimesh(
        vertices=vertices2,
        faces=np.array(faces2),
        process=True
    )

    if not solid:
        try:
            # Create hollow versions
            inner_mesh1 = mesh1.copy()
            inner_mesh1.vertices -= inner_mesh1.vertex_normals * wall_thickness
            inner_mesh1.invert()

            inner_mesh2 = mesh2.copy()
            inner_mesh2.vertices -= inner_mesh2.vertex_normals * wall_thickness
            inner_mesh2.invert()

            # Combine all meshes
            combined_mesh = trimesh.util.concatenate([mesh1, inner_mesh1, mesh2, inner_mesh2])
            combined_mesh.export(filename)
        except Exception as e:
            print(f"Warning: Could not create hollow model: {e}. Exporting solid model instead.")
            combined_mesh = trimesh.util.concatenate([mesh1, mesh2])
            combined_mesh.export(filename)
    else:
        # Export solid model
        combined_mesh = trimesh.util.concatenate([mesh1, mesh2])
        combined_mesh.export(filename)

    print(f"Merkaba 3D printing model saved to {filename}")
    return os.path.abspath(filename)


def export_spheres_for_3d_printing(
    flower_of_life_3d: Dict[str, Any],
    filename: str,
    scale: float = 1.0,
    wall_thickness: float = 0.1,
    solid: bool = False,
    format: str = "stl"
) -> str:
    """
    Export a 3D Flower of Life optimized for 3D printing.

    Args:
        flower_of_life_3d: Dictionary containing spheres data
        filename: Output filename
        scale: Scale factor
        wall_thickness: Thickness of walls for hollow models
        solid: Whether to create a solid model
        format: Output format

    Returns:
        The full path to the saved file
    """
    if not TRIMESH_AVAILABLE:
        raise ImportError("trimesh is required for 3D printing export")

    spheres = flower_of_life_3d['spheres']
    meshes = []

    for sphere in spheres:
        center = np.array(sphere['center']) * scale
        radius = sphere['radius'] * scale

        # Create a sphere mesh
        sphere_mesh = trimesh.creation.icosphere(radius=radius, subdivisions=2)
        sphere_mesh.apply_translation(center)

        if not solid:
            try:
                # Create a hollow sphere
                inner_radius = max(0.01, radius - wall_thickness)
                inner_sphere = trimesh.creation.icosphere(radius=inner_radius, subdivisions=2)
                inner_sphere.apply_translation(center)
                inner_sphere.invert()

                # Combine outer and inner spheres
                combined_sphere = trimesh.util.concatenate([sphere_mesh, inner_sphere])
                meshes.append(combined_sphere)
            except Exception as e:
                print(f"Warning: Could not create hollow sphere: {e}. Using solid sphere instead.")
                meshes.append(sphere_mesh)
        else:
            meshes.append(sphere_mesh)

    # Combine all sphere meshes
    if meshes:
        combined_mesh = trimesh.util.concatenate(meshes)
        combined_mesh.export(filename)

        print(f"3D Flower of Life printing model saved to {filename}")
        return os.path.abspath(filename)
    else:
        raise ValueError("No spheres found in the 3D Flower of Life data")


def export_high_resolution_image(
    fig: Figure,
    filename: str,
    dpi: int = 600,
    format: str = "png",
    transparent: bool = False,
    **kwargs
) -> str:
    """
    Export a high-resolution image suitable for printing or large displays.

    Args:
        fig: The matplotlib figure to export
        filename: Output filename
        dpi: Resolution in dots per inch (300+ recommended for printing)
        format: File format (png, tiff, pdf recommended for high quality)
        transparent: Whether to use a transparent background
        **kwargs: Additional arguments to pass to fig.savefig()

    Returns:
        The full path to the saved file
    """
    # Ensure the filename has the correct extension
    if not filename.lower().endswith(f".{format.lower()}"):
        filename = f"{filename}.{format.lower()}"

    # Create directory if it doesn't exist
    os.makedirs(os.path.dirname(os.path.abspath(filename)), exist_ok=True)

    # Set figure size to a standard print size if not already set
    if 'figsize' in kwargs:
        fig.set_size_inches(kwargs.pop('figsize'))

    # Increase line widths and font sizes for high-resolution output
    for ax in fig.get_axes():
        # Increase line widths
        for line in ax.get_lines():
            line.set_linewidth(line.get_linewidth() * 2)

        # Increase font sizes
        ax.title.set_fontsize(ax.title.get_fontsize() * 1.5)
        ax.xaxis.label.set_fontsize(ax.xaxis.label.get_fontsize() * 1.5)
        ax.yaxis.label.set_fontsize(ax.yaxis.label.get_fontsize() * 1.5)
        ax.tick_params(axis='both', which='major', labelsize=ax.get_xticklabels()[0].get_fontsize() * 1.5 if ax.get_xticklabels() else 12)

    # Save the figure at high resolution
    fig.savefig(
        filename,
        dpi=dpi,
        transparent=transparent,
        format=format,
        bbox_inches='tight',
        **kwargs
    )

    print(f"High-resolution image saved to {filename}")
    return os.path.abspath(filename)
