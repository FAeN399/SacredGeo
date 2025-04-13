"""
3D sacred geometry shapes and polyhedra.
"""
import numpy as np
from typing import List, Tuple, Dict, Any

# Platonic solids
def create_tetrahedron(center: Tuple[float, float, float] = (0, 0, 0),
                       radius: float = 1.0) -> Dict[str, Any]:
    """
    Create a regular tetrahedron.
    
    Args:
        center: (x, y, z) coordinates of the center
        radius: Distance from center to vertices
        
    Returns:
        Dictionary containing vertices, edges, and faces
    """
    # Define the vertices of a tetrahedron centered at the origin
    vertices = np.array([
        [1, 1, 1],
        [1, -1, -1],
        [-1, 1, -1],
        [-1, -1, 1]
    ])
    
    # Normalize to the given radius
    norm = np.sqrt(3)
    vertices = vertices * (radius / norm)
    
    # Translate to the given center
    vertices = vertices + np.array(center)
    
    # Define the edges (pairs of vertex indices)
    edges = [
        (0, 1), (0, 2), (0, 3),
        (1, 2), (1, 3), (2, 3)
    ]
    
    # Define the faces (triplets of vertex indices)
    faces = [
        (0, 1, 2),
        (0, 1, 3),
        (0, 2, 3),
        (1, 2, 3)
    ]
    
    return {
        'vertices': vertices,
        'edges': edges,
        'faces': faces
    }

def create_cube(center: Tuple[float, float, float] = (0, 0, 0),
               radius: float = 1.0) -> Dict[str, Any]:
    """
    Create a regular cube (hexahedron).
    
    Args:
        center: (x, y, z) coordinates of the center
        radius: Distance from center to vertices
        
    Returns:
        Dictionary containing vertices, edges, and faces
    """
    # Define the vertices of a cube centered at the origin
    vertices = np.array([
        [1, 1, 1],
        [1, 1, -1],
        [1, -1, 1],
        [1, -1, -1],
        [-1, 1, 1],
        [-1, 1, -1],
        [-1, -1, 1],
        [-1, -1, -1]
    ])
    
    # Normalize to the given radius
    norm = np.sqrt(3)
    vertices = vertices * (radius / norm)
    
    # Translate to the given center
    vertices = vertices + np.array(center)
    
    # Define the edges (pairs of vertex indices)
    edges = [
        (0, 1), (0, 2), (0, 4),
        (1, 3), (1, 5),
        (2, 3), (2, 6),
        (3, 7),
        (4, 5), (4, 6),
        (5, 7),
        (6, 7)
    ]
    
    # Define the faces (quadruplets of vertex indices)
    faces = [
        (0, 1, 3, 2),  # x = 1 face
        (4, 5, 7, 6),  # x = -1 face
        (0, 1, 5, 4),  # y = 1 face
        (2, 3, 7, 6),  # y = -1 face
        (0, 2, 6, 4),  # z = 1 face
        (1, 3, 7, 5)   # z = -1 face
    ]
    
    return {
        'vertices': vertices,
        'edges': edges,
        'faces': faces
    }

def create_octahedron(center: Tuple[float, float, float] = (0, 0, 0),
                     radius: float = 1.0) -> Dict[str, Any]:
    """
    Create a regular octahedron.
    
    Args:
        center: (x, y, z) coordinates of the center
        radius: Distance from center to vertices
        
    Returns:
        Dictionary containing vertices, edges, and faces
    """
    # Define the vertices of an octahedron centered at the origin
    vertices = np.array([
        [1, 0, 0],
        [-1, 0, 0],
        [0, 1, 0],
        [0, -1, 0],
        [0, 0, 1],
        [0, 0, -1]
    ])
    
    # Scale to the given radius
    vertices = vertices * radius
    
    # Translate to the given center
    vertices = vertices + np.array(center)
    
    # Define the edges (pairs of vertex indices)
    edges = [
        (0, 2), (0, 3), (0, 4), (0, 5),
        (1, 2), (1, 3), (1, 4), (1, 5),
        (2, 4), (2, 5), (3, 4), (3, 5)
    ]
    
    # Define the faces (triplets of vertex indices)
    faces = [
        (0, 2, 4), (0, 4, 3),
        (0, 3, 5), (0, 5, 2),
        (1, 2, 4), (1, 4, 3),
        (1, 3, 5), (1, 5, 2)
    ]
    
    return {
        'vertices': vertices,
        'edges': edges,
        'faces': faces
    }

def create_icosahedron(center: Tuple[float, float, float] = (0, 0, 0),
                      radius: float = 1.0) -> Dict[str, Any]:
    """
    Create a regular icosahedron.
    
    Args:
        center: (x, y, z) coordinates of the center
        radius: Distance from center to vertices
        
    Returns:
        Dictionary containing vertices, edges, and faces
    """
    # Golden ratio
    phi = (1 + np.sqrt(5)) / 2
    
    # Define the vertices of an icosahedron centered at the origin
    vertices = np.array([
        [0, 1, phi], [0, -1, phi], [0, 1, -phi], [0, -1, -phi],
        [1, phi, 0], [-1, phi, 0], [1, -phi, 0], [-1, -phi, 0],
        [phi, 0, 1], [-phi, 0, 1], [phi, 0, -1], [-phi, 0, -1]
    ])
    
    # Normalize to the given radius
    norm = np.sqrt(1 + phi**2)
    vertices = vertices * (radius / norm)
    
    # Translate to the given center
    vertices = vertices + np.array(center)
    
    # Define the faces (triplets of vertex indices)
    faces = [
        (0, 8, 1), (0, 1, 9), (0, 9, 5), (0, 5, 4), (0, 4, 8),
        (1, 8, 6), (1, 6, 7), (1, 7, 9), (2, 10, 3), (2, 3, 11),
        (2, 11, 5), (2, 5, 4), (2, 4, 10), (3, 10, 6), (3, 6, 7),
        (3, 7, 11), (4, 5, 2), (5, 9, 11), (6, 10, 8), (7, 6, 3),
        (8, 4, 10), (9, 7, 11)
    ]
    
    # Define the edges (pairs of vertex indices) based on faces
    edges = set()
    for face in faces:
        for i in range(3):
            edge = tuple(sorted([face[i], face[(i+1)%3]]))
            edges.add(edge)
    
    return {
        'vertices': vertices,
        'edges': list(edges),
        'faces': faces
    }

def create_dodecahedron(center: Tuple[float, float, float] = (0, 0, 0),
                       radius: float = 1.0) -> Dict[str, Any]:
    """
    Create a regular dodecahedron.
    
    Args:
        center: (x, y, z) coordinates of the center
        radius: Distance from center to vertices
        
    Returns:
        Dictionary containing vertices, edges, and faces
    """
    # Golden ratio
    phi = (1 + np.sqrt(5)) / 2
    
    # Define the vertices of a dodecahedron centered at the origin
    vertices = np.array([
        [1, 1, 1], [1, 1, -1], [1, -1, 1], [1, -1, -1],
        [-1, 1, 1], [-1, 1, -1], [-1, -1, 1], [-1, -1, -1],
        [0, phi, 1/phi], [0, phi, -1/phi], [0, -phi, 1/phi], [0, -phi, -1/phi],
        [1/phi, 0, phi], [1/phi, 0, -phi], [-1/phi, 0, phi], [-1/phi, 0, -phi],
        [phi, 1/phi, 0], [phi, -1/phi, 0], [-phi, 1/phi, 0], [-phi, -1/phi, 0]
    ])
    
    # Normalize to the given radius
    norm = np.sqrt(3)
    vertices = vertices * (radius / norm)
    
    # Translate to the given center
    vertices = vertices + np.array(center)
    
    # Define the faces (pentagons defined by vertex indices)
    faces = [
        (0, 8, 4, 14, 12),
        (1, 9, 5, 15, 13),
        (2, 10, 6, 14, 12),
        (3, 11, 7, 15, 13),
        (0, 16, 17, 2, 12),
        (1, 16, 17, 3, 13),
        (4, 18, 19, 6, 14),
        (5, 18, 19, 7, 15),
        (0, 8, 9, 1, 16),
        (2, 10, 11, 3, 17),
        (4, 8, 9, 5, 18),
        (6, 10, 11, 7, 19)
    ]
    
    # Define the edges (pairs of vertex indices) based on faces
    edges = set()
    for face in faces:
        for i in range(len(face)):
            edge = tuple(sorted([face[i], face[(i+1)%len(face)]]))
            edges.add(edge)
    
    return {
        'vertices': vertices,
        'edges': list(edges),
        'faces': faces
    }

def create_merkaba(center: Tuple[float, float, float] = (0, 0, 0),
                  radius: float = 1.0, rotation: float = 0.0) -> Dict[str, Any]:
    """
    Create a Merkaba (Star Tetrahedron) by combining two interlocking tetrahedra.
    
    Args:
        center: (x, y, z) coordinates of the center
        radius: Distance from center to vertices
        rotation: Rotation angle in radians for the second tetrahedron
        
    Returns:
        Dictionary containing both tetrahedra
    """
    # Create the first tetrahedron pointing upward
    tetra1 = create_tetrahedron(center, radius)
    
    # Create the second tetrahedron pointing downward (inverted)
    # We can create an inverted tetrahedron by flipping the y-coordinate
    tetra2_verts = tetra1['vertices'].copy()
    tetra2_verts[:, 1] = -tetra2_verts[:, 1]  # Flip y coordinates
    
    # Apply rotation around the y-axis if specified
    if rotation != 0.0:
        cos_r = np.cos(rotation)
        sin_r = np.sin(rotation)
        rot_matrix = np.array([
            [cos_r, 0, sin_r],
            [0, 1, 0],
            [-sin_r, 0, cos_r]
        ])
        
        for i in range(len(tetra2_verts)):
            # Translate to origin, rotate, translate back
            v = tetra2_verts[i] - np.array(center)
            v = np.dot(rot_matrix, v)
            tetra2_verts[i] = v + np.array(center)
    
    # Recreate the second tetrahedron with the modified vertices
    tetra2 = {
        'vertices': tetra2_verts,
        'edges': tetra1['edges'],
        'faces': tetra1['faces']
    }
    
    return {
        'tetrahedron1': tetra1,
        'tetrahedron2': tetra2
    }

def create_cuboctahedron(center: Tuple[float, float, float] = (0, 0, 0),
                        radius: float = 1.0) -> Dict[str, Any]:
    """
    Create a cuboctahedron (vector equilibrium).
    
    Args:
        center: (x, y, z) coordinates of the center
        radius: Distance from center to vertices
        
    Returns:
        Dictionary containing vertices, edges, and faces
    """
    # Define the vertices of a cuboctahedron centered at the origin
    # A cuboctahedron has 12 vertices at the midpoints of the edges of a cube
    vertices = np.array([
        [1, 1, 0], [1, -1, 0], [-1, 1, 0], [-1, -1, 0],
        [1, 0, 1], [1, 0, -1], [-1, 0, 1], [-1, 0, -1],
        [0, 1, 1], [0, 1, -1], [0, -1, 1], [0, -1, -1]
    ])
    
    # Scale to the given radius
    vertices = vertices * (radius / np.sqrt(2))
    
    # Translate to the given center
    vertices = vertices + np.array(center)
    
    # Define the faces
    # 8 triangular faces
    triangular_faces = [
        (0, 4, 8), (0, 5, 9), (1, 4, 10), (1, 5, 11),
        (2, 6, 8), (2, 7, 9), (3, 6, 10), (3, 7, 11)
    ]
    
    # 6 square faces
    square_faces = [
        (0, 2, 3, 1),  # xy plane
        (4, 6, 7, 5),  # xz plane
        (8, 9, 7, 6),  # yz plane
        (0, 1, 5, 4),  # +x half
        (2, 3, 7, 6),  # -x half
        (8, 9, 5, 4)   # +y half
    ]
    
    # Define the edges based on faces
    edges = set()
    for face in triangular_faces:
        for i in range(len(face)):
            edge = tuple(sorted([face[i], face[(i+1)%len(face)]]))
            edges.add(edge)
    
    for face in square_faces:
        for i in range(len(face)):
            edge = tuple(sorted([face[i], face[(i+1)%len(face)]]))
            edges.add(edge)
    
    return {
        'vertices': vertices,
        'edges': list(edges),
        'triangular_faces': triangular_faces,
        'square_faces': square_faces
    }

def create_flower_of_life_3d(center: Tuple[float, float, float] = (0, 0, 0),
                           radius: float = 1.0, layers: int = 2) -> Dict[str, Any]:
    """
    Create a 3D version of the Flower of Life pattern.
    
    Args:
        center: (x, y, z) coordinates of the center
        radius: Radius of each sphere
        layers: Number of layers of spheres
        
    Returns:
        Dictionary containing sphere centers and radii
    """
    spheres = []
    points = set()  # Keep track of sphere centers
    
    # Add the center sphere
    spheres.append({
        'center': center,
        'radius': radius
    })
    points.add(center)
    
    # Define the 12 directions of an icosahedron (approximately evenly distributed)
    phi = (1 + np.sqrt(5)) / 2
    icosa_dirs = np.array([
        [0, 1, phi], [0, -1, phi], [0, 1, -phi], [0, -1, -phi],
        [1, phi, 0], [-1, phi, 0], [1, -phi, 0], [-1, -phi, 0],
        [phi, 0, 1], [-phi, 0, 1], [phi, 0, -1], [-phi, 0, -1]
    ])
    # Normalize directions
    icosa_dirs = icosa_dirs / np.sqrt(np.sum(icosa_dirs**2, axis=1))[:, np.newaxis]
    
    for layer in range(1, layers + 1):
        # For each existing point, create spheres in the 12 directions
        new_points = set()
        for point in points:
            for dir_vec in icosa_dirs:
                x = point[0] + 2 * radius * dir_vec[0]
                y = point[1] + 2 * radius * dir_vec[1]
                z = point[2] + 2 * radius * dir_vec[2]
                new_point = (round(x, 6), round(y, 6), round(z, 6))  # Round to avoid floating point issues
                
                if new_point not in points:
                    new_points.add(new_point)
        
        # Add new spheres
        for point in new_points:
            spheres.append({
                'center': point,
                'radius': radius
            })
        
        points.update(new_points)
    
    return {
        'spheres': spheres
    }

def create_torus(center: Tuple[float, float, float] = (0, 0, 0),
               major_radius: float = 2.0, minor_radius: float = 0.5,
               num_major_segments: int = 36, num_minor_segments: int = 18) -> Dict[str, Any]:
    """
    Create a torus (donut shape).
    
    Args:
        center: (x, y, z) coordinates of the center
        major_radius: Distance from center of torus to center of tube
        minor_radius: Radius of the tube
        num_major_segments: Number of segments around the major circle
        num_minor_segments: Number of segments around the minor circle
        
    Returns:
        Dictionary containing vertices and faces
    """
    vertices = []
    faces = []
    
    # Generate vertices
    for i in range(num_major_segments):
        theta = 2 * np.pi * i / num_major_segments
        cos_theta = np.cos(theta)
        sin_theta = np.sin(theta)
        
        for j in range(num_minor_segments):
            phi = 2 * np.pi * j / num_minor_segments
            cos_phi = np.cos(phi)
            sin_phi = np.sin(phi)
            
            # Calculate position of vertex
            x = center[0] + (major_radius + minor_radius * cos_phi) * cos_theta
            y = center[1] + (major_radius + minor_radius * cos_phi) * sin_theta
            z = center[2] + minor_radius * sin_phi
            
            vertices.append((x, y, z))
    
    # Generate faces
    for i in range(num_major_segments):
        for j in range(num_minor_segments):
            # Calculate indices of the four corners of a quad face
            i_next = (i + 1) % num_major_segments
            j_next = (j + 1) % num_minor_segments
            
            v1 = i * num_minor_segments + j
            v2 = i_next * num_minor_segments + j
            v3 = i_next * num_minor_segments + j_next
            v4 = i * num_minor_segments + j_next
            
            # Create two triangular faces for each quad
            faces.append((v1, v2, v3))
            faces.append((v1, v3, v4))
    
    return {
        'vertices': np.array(vertices),
        'faces': faces
    }