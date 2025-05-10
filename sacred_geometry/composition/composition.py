"""
Layered composition module for sacred geometry.

This module provides functionality for creating complex compositions
of sacred geometry shapes using a scene graph/hierarchy approach.
"""
import numpy as np
from typing import List, Dict, Tuple, Optional, Union
import copy

from sacred_geometry.shapes.shapes import (
    create_tetrahedron, create_cube, create_octahedron,
    create_icosahedron, create_dodecahedron, create_merkaba,
    create_cuboctahedron, create_torus
)
from sacred_geometry.core.core import get_golden_ratio

# Sacred ratios
PHI = get_golden_ratio()  # Golden Ratio
SQRT2 = np.sqrt(2)        # Square root of 2
SQRT3 = np.sqrt(3)        # Square root of 3
PI = np.pi               # Pi

class GeometryNode:
    """A node in the sacred geometry scene graph.

    Can represent either a single shape or a group of shapes.
    """
    def __init__(self, name: str, shape_data: Optional[Dict] = None,
                 color: Union[str, Tuple] = 'blue', alpha: float = 0.6,
                 position: Tuple[float, float, float] = (0, 0, 0),
                 rotation: float = 0, scale: float = 1.0):
        """
        Initialize a GeometryNode.

        Args:
            name: Name of the node
            shape_data: Dictionary containing shape information
            color: Color of the shape (name or RGB tuple)
            alpha: Transparency of the shape
            position: (x, y, z) position of the node
            rotation: Rotation in radians
            scale: Scale factor
        """
        self.name = name
        self.shape_data = shape_data  # The actual shape data dictionary
        self.color = color
        self.alpha = alpha
        self.position = position
        self.rotation = rotation
        self.scale = scale
        self.children = []
        self.visible = True
        self.parent = None

        # Enhanced transformation properties
        self.rotation_xyz = (0, 0, rotation)  # (x, y, z) rotation angles
        self.scale_xyz = (scale, scale, scale)  # (x, y, z) scale factors

    def add_child(self, child: 'GeometryNode') -> 'GeometryNode':
        """Add a child node to this node."""
        child.parent = self
        self.children.append(child)
        return child

    def remove_child(self, child: 'GeometryNode') -> None:
        """Remove a child node from this node."""
        if child in self.children:
            child.parent = None
            self.children.remove(child)

    def get_transform_matrix(self) -> np.ndarray:
        """Get the transformation matrix for this node."""
        # Create translation matrix
        tx, ty, tz = self.position
        T = np.array([
            [1, 0, 0, tx],
            [0, 1, 0, ty],
            [0, 0, 1, tz],
            [0, 0, 0, 1]
        ])

        # Create rotation matrices for each axis
        rx, ry, rz = self.rotation_xyz

        # X rotation
        Rx = np.array([
            [1, 0, 0, 0],
            [0, np.cos(rx), -np.sin(rx), 0],
            [0, np.sin(rx), np.cos(rx), 0],
            [0, 0, 0, 1]
        ])

        # Y rotation
        Ry = np.array([
            [np.cos(ry), 0, np.sin(ry), 0],
            [0, 1, 0, 0],
            [-np.sin(ry), 0, np.cos(ry), 0],
            [0, 0, 0, 1]
        ])

        # Z rotation
        Rz = np.array([
            [np.cos(rz), -np.sin(rz), 0, 0],
            [np.sin(rz), np.cos(rz), 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1]
        ])

        # Combined rotation (order: Z, Y, X)
        R = Rz @ Ry @ Rx

        # Create scale matrix with per-axis scaling
        sx, sy, sz = self.scale_xyz
        S = np.array([
            [sx, 0, 0, 0],
            [0, sy, 0, 0],
            [0, 0, sz, 0],
            [0, 0, 0, 1]
        ])

        # Combine transformations
        M = T @ R @ S

        # If we have a parent, multiply by parent's transform
        if self.parent:
            M = self.parent.get_transform_matrix() @ M

        return M

    def set_rotation(self, angles: Tuple[float, float, float]) -> 'GeometryNode':
        """Set rotation around all three axes (x, y, z) in radians."""
        self.rotation_xyz = angles
        self.rotation = angles[2]  # Keep the z-rotation in the original field for backwards compatibility
        return self

    def rotate(self, angles: Tuple[float, float, float]) -> 'GeometryNode':
        """Apply additional rotation around all three axes (x, y, z) in radians."""
        rx, ry, rz = angles
        old_rx, old_ry, old_rz = self.rotation_xyz
        self.rotation_xyz = (old_rx + rx, old_ry + ry, old_rz + rz)
        self.rotation = self.rotation_xyz[2]  # Update z-rotation for backwards compatibility
        return self

    def set_scale(self, scales: Tuple[float, float, float]) -> 'GeometryNode':
        """Set scale factors for all three axes (x, y, z)."""
        self.scale_xyz = scales
        self.scale = scales[0]  # Use x-scale for the original scale field for backwards compatibility
        return self

    def scale_by(self, factors: Tuple[float, float, float]) -> 'GeometryNode':
        """Apply additional scaling to all three axes (x, y, z)."""
        fx, fy, fz = factors
        old_sx, old_sy, old_sz = self.scale_xyz
        self.scale_xyz = (old_sx * fx, old_sy * fy, old_sz * fz)
        self.scale = self.scale_xyz[0]  # Update original scale field for backwards compatibility
        return self

    def get_transformed_shape(self) -> Optional[Dict]:
        """Get the shape data with transformations applied."""
        if self.shape_data is None:
            return None

        # Make a deep copy of shape_data to avoid modifying the original
        transformed_shape = copy.deepcopy(self.shape_data)

        # Get the full transformation matrix
        M = self.get_transform_matrix()

        # Apply transformation to all vertices
        if 'tetrahedron1' in transformed_shape and 'tetrahedron2' in transformed_shape:
            # Handle Merkaba case (two tetrahedra)
            for tetra_key in ['tetrahedron1', 'tetrahedron2']:
                vertices = transformed_shape[tetra_key]['vertices']
                homogeneous_vertices = np.hstack([vertices, np.ones((vertices.shape[0], 1))])
                transformed_vertices = np.dot(homogeneous_vertices, M.T)[:, :3]
                transformed_shape[tetra_key]['vertices'] = transformed_vertices
        elif 'vertices' in transformed_shape:
            # Handle regular shape with vertices
            vertices = transformed_shape['vertices']
            homogeneous_vertices = np.hstack([vertices, np.ones((vertices.shape[0], 1))])
            transformed_vertices = np.dot(homogeneous_vertices, M.T)[:, :3]
            transformed_shape['vertices'] = transformed_vertices

        return transformed_shape

    def scale_by_sacred_ratio(self, ratio_name: str,
                             power: float = 1.0,
                             axes: Tuple[bool, bool, bool] = (True, True, True)) -> 'GeometryNode':
        """Scale this node by a sacred ratio with optional power and per-axis application.

        Args:
            ratio_name: Name of the ratio ('phi', 'sqrt2', 'sqrt3', '1/phi', etc.)
            power: Power to raise the ratio to (e.g., 2.0 for phi²)
            axes: Which axes to apply scaling to (x, y, z)

        Returns:
            Self for method chaining
        """
        # Get the base ratio value
        ratio_value = 1.0
        if ratio_name == 'phi':
            ratio_value = PHI
        elif ratio_name == 'sqrt2':
            ratio_value = SQRT2
        elif ratio_name == 'sqrt3':
            ratio_value = SQRT3
        elif ratio_name == '1/phi':
            ratio_value = 1.0 / PHI
        elif ratio_name == 'pi':
            ratio_value = PI
        elif ratio_name == '1/pi':
            ratio_value = 1.0 / PI

        # Apply power
        ratio_value = ratio_value ** power

        # Get current scale values
        sx, sy, sz = self.scale_xyz

        # Apply to selected axes
        new_sx = sx * ratio_value if axes[0] else sx
        new_sy = sy * ratio_value if axes[1] else sy
        new_sz = sz * ratio_value if axes[2] else sz

        # Update scale values
        self.scale_xyz = (new_sx, new_sy, new_sz)
        self.scale = new_sx  # Update original scale field for backwards compatibility

        return self

    def __repr__(self) -> str:
        return "GeometryNode({}, scale={}, children={})".format(repr(self.name), repr(self.scale), repr(len(self.children)))

class GeometryScene:
    """A scene containing sacred geometry compositions."""
    def __init__(self):
        self.root = GeometryNode("Root")

    def create_merkaba_in_cuboctahedron(self, golden_ratio_scaled=True) -> GeometryNode:
        """Create a Merkaba inside a Vector Equilibrium (Cuboctahedron).

        Args:
            golden_ratio_scaled: If True, scale the Merkaba by 1/φ relative to the Cuboctahedron
        """
        # Create a group node
        group = GeometryNode("Merkaba in Cuboctahedron")
        self.root.add_child(group)

        # Create the Cuboctahedron
        ve_data = create_cuboctahedron(center=(0, 0, 0), radius=1.0)
        ve = GeometryNode("Vector Equilibrium", ve_data, color='gold', alpha=0.4)
        group.add_child(ve)

        # Create the Merkaba
        merkaba_data = create_merkaba(center=(0, 0, 0), radius=1.0, rotation=np.pi/4)
        merkaba = GeometryNode("Merkaba", merkaba_data, color='blue', alpha=0.6)

        # Scale the Merkaba by 1/φ if requested (golden ratio scaling)
        if golden_ratio_scaled:
            merkaba.scale = 1 / PHI
        else:
            merkaba.scale = 0.8  # Default scaling if not using golden ratio

        group.add_child(merkaba)

        return group

    def create_nested_platonic_solids(self) -> GeometryNode:
        """Create nested Platonic solids according to sacred proportions."""
        # Create a group node
        group = GeometryNode("Nested Platonic Solids")
        self.root.add_child(group)

        # Create outer Dodecahedron (usually the largest Platonic solid)
        dodeca_data = create_dodecahedron(center=(0, 0, 0), radius=1.0)
        dodeca = GeometryNode("Dodecahedron", dodeca_data, color='purple', alpha=0.3)
        group.add_child(dodeca)

        # Create Icosahedron scaled by 1/φ
        icosa_data = create_icosahedron(center=(0, 0, 0), radius=1.0)
        icosa = GeometryNode("Icosahedron", icosa_data, color='blue', alpha=0.4)
        icosa.scale = 0.9 / PHI
        group.add_child(icosa)

        # Create Octahedron scaled by 1/φ²
        octa_data = create_octahedron(center=(0, 0, 0), radius=1.0)
        octa = GeometryNode("Octahedron", octa_data, color='green', alpha=0.5)
        octa.scale = 0.8 / (PHI * PHI)
        group.add_child(octa)

        # Create Tetrahedron scaled by 1/φ³
        tetra_data = create_tetrahedron(center=(0, 0, 0), radius=1.0)
        tetra = GeometryNode("Tetrahedron", tetra_data, color='red', alpha=0.6)
        tetra.scale = 0.7 / (PHI * PHI * PHI)
        group.add_child(tetra)

        return group

    def create_64_tetrahedron_grid(self) -> GeometryNode:
        """Create a 64 Tetrahedron Grid (8 star tetrahedra arranged in a cube)."""
        # Create a group node
        group = GeometryNode("64 Tetrahedron Grid")
        self.root.add_child(group)

        # The 8 positions correspond to the corners of a cube
        cube_corners = [
            (0.5, 0.5, 0.5), (0.5, 0.5, -0.5), (0.5, -0.5, 0.5), (0.5, -0.5, -0.5),
            (-0.5, 0.5, 0.5), (-0.5, 0.5, -0.5), (-0.5, -0.5, 0.5), (-0.5, -0.5, -0.5)
        ]

        # Reference size for each star tetrahedron
        star_tetra_size = 0.35

        # Create 8 Merkabas (Star Tetrahedra) at cube corners
        for i, position in enumerate(cube_corners):
            merkaba_data = create_merkaba(center=(0, 0, 0), radius=1.0, rotation=np.pi/4)
            merkaba = GeometryNode(f"Merkaba_{i}", merkaba_data,
                                  color='blue', alpha=0.5, position=position)
            merkaba.scale = star_tetra_size
            group.add_child(merkaba)

        # Add a wireframe cube to show the structure
        cube_data = create_cube(center=(0, 0, 0), radius=0.5)
        cube = GeometryNode("Outer Cube", cube_data, color='gray', alpha=0.2)
        group.add_child(cube)

        return group

    def create_torus_with_embedded_merkaba(self) -> GeometryNode:
        """Create a Torus with an embedded Merkaba."""
        # Create a group node
        group = GeometryNode("Torus with Merkaba")
        self.root.add_child(group)

        # Create the Torus
        torus_data = create_torus(center=(0, 0, 0),
                                major_radius=1.0, minor_radius=0.4,
                                num_major_segments=36, num_minor_segments=18)
        torus = GeometryNode("Torus", torus_data, color='gold', alpha=0.3)
        group.add_child(torus)

        # Create the Merkaba inside
        merkaba_data = create_merkaba(center=(0, 0, 0), radius=1.0, rotation=np.pi/4)
        merkaba = GeometryNode("Merkaba", merkaba_data, color='blue', alpha=0.6)

        # Scale Merkaba to fit inside the torus's central opening
        merkaba.scale = 0.5
        group.add_child(merkaba)

        return group

    def create_fractal_tetrahedron(self, depth=2) -> GeometryNode:
        """Create a fractal tetrahedron with self-similar nested forms."""
        # Create a group node
        group = GeometryNode("Fractal Tetrahedron")
        self.root.add_child(group)

        # Create the main tetrahedron
        tetra_data = create_tetrahedron(center=(0, 0, 0), radius=1.0)
        main_tetra = GeometryNode("Main Tetrahedron", tetra_data, color='blue', alpha=0.4)
        group.add_child(main_tetra)

        # Recursively add smaller tetrahedra at the vertices
        self._add_corner_tetrahedra(main_tetra, depth, 1)

        return group

    def _add_corner_tetrahedra(self, parent_tetra, depth, current_depth) -> None:
        """Helper method to recursively add tetrahedra at corners."""
        if current_depth > depth:
            return

        # Get the transformed shape to get actual vertex positions
        parent_shape = parent_tetra.get_transformed_shape()
        parent_vertices = parent_shape['vertices']

        # Size factor for the corner tetrahedra (scaled by 1/φ)
        corner_scale = parent_tetra.scale / (PHI * 2)

        # Add a tetrahedron at each corner of the parent
        for i, vertex in enumerate(parent_vertices):
            tetra_data = create_tetrahedron(center=(0, 0, 0), radius=1.0)
            corner_tetra = GeometryNode(f"Tetra_L{current_depth}_{i}",
                                       tetra_data,
                                       color=f'C{current_depth}',
                                       alpha=0.5,
                                       position=tuple(vertex),
                                       scale=corner_scale)
            parent_tetra.add_child(corner_tetra)

            # Recursively add more tetrahedra
            self._add_corner_tetrahedra(corner_tetra, depth, current_depth + 1)

# Helper functions for creating common compositions
def create_merkaba_with_golden_ratio() -> GeometryNode:
    """Create a merkaba with golden ratio proportions."""
    merkaba_data = create_merkaba(center=(0, 0, 0), radius=1.0, rotation=np.pi/PHI)
    merkaba = GeometryNode("Golden Merkaba", merkaba_data, color='blue', alpha=0.6)
    return merkaba

def create_phi_scaled_nested_shapes() -> GeometryNode:
    """Create a series of shapes nested according to the golden ratio."""
    group = GeometryNode("Phi Scaled Nested Shapes")

    # Start with a large icosahedron
    icosa_data = create_icosahedron(center=(0, 0, 0), radius=1.0)
    icosa = GeometryNode("Icosahedron", icosa_data, color='blue', alpha=0.3)
    group.add_child(icosa)

    # Add a dodecahedron scaled by 1/φ
    dodeca_data = create_dodecahedron(center=(0, 0, 0), radius=1.0)
    dodeca = GeometryNode("Dodecahedron", dodeca_data, color='purple', alpha=0.4)
    dodeca.scale = 1 / PHI
    group.add_child(dodeca)

    # Add a cuboctahedron scaled by 1/φ²
    cuboct_data = create_cuboctahedron(center=(0, 0, 0), radius=1.0)
    cuboct = GeometryNode("Cuboctahedron", cuboct_data, color='gold', alpha=0.5)
    cuboct.scale = 1 / (PHI * PHI)
    group.add_child(cuboct)

    # Add a merkaba scaled by 1/φ³
    merkaba_data = create_merkaba(center=(0, 0, 0), radius=1.0, rotation=np.pi/4)
    merkaba = GeometryNode("Merkaba", merkaba_data, color='red', alpha=0.6)
    merkaba.scale = 1 / (PHI * PHI * PHI)
    group.add_child(merkaba)

    return group

def create_symmetric_arrangement(shape_creator,
                               positions,
                               base_color='blue',
                               alpha=0.5,
                               scale=1.0) -> GeometryNode:
    """Create a symmetric arrangement of shapes.

    Args:
        shape_creator: Function that creates a shape
        positions: List of positions for each shape
        base_color: Base color for the shapes
        alpha: Transparency
        scale: Base scale for each shape

    Returns:
        A GeometryNode containing the symmetric arrangement
    """
    group = GeometryNode("Symmetric Arrangement")

    # Color variations for visual distinction
    colors = ['blue', 'red', 'green', 'purple', 'orange', 'cyan', 'magenta', 'gold']

    # Create shapes at each position
    for i, position in enumerate(positions):
        # Get the shape data
        shape_data = shape_creator(center=(0, 0, 0), radius=1.0)

        # Choose color
        color = colors[i % len(colors)] if len(colors) > 1 else base_color

        # Create the node
        node = GeometryNode(f"Shape_{i}", shape_data, color=color, alpha=alpha,
                          position=position)
        node.scale = scale

        # Add to group
        group.add_child(node)

    return group

def apply_golden_ratio_proportions(node: GeometryNode, depth: int = 1) -> None:
    """Apply golden ratio proportions to a node and its children.

    This scales each child by 1/φ compared to its parent.

    Args:
        node: The GeometryNode to apply proportions to
        depth: Current recursion depth
    """
    if not node.children:
        return

    # Scale each child by 1/φ relative to the parent
    for child in node.children:
        child.scale = node.scale / (PHI ** depth)

        # Recursively apply to this child's children
        apply_golden_ratio_proportions(child, depth + 1)

# Enhanced symmetry functions and additional composition methods

def create_symmetry_group(shape_creator, symmetry_type: str, scale: float = 1.0, color: str = 'blue', alpha: float = 0.6) -> GeometryNode:
    """Create a group of shapes arranged according to a symmetry group.

    Args:
        shape_creator: Function that creates a shape
        symmetry_type: Type of symmetry ('tetrahedral', 'octahedral', 'icosahedral', 'dihedral-n' where n is an integer)
        scale: Scale factor for the shapes
        color: Base color for the shapes
        alpha: Transparency

    Returns:
        A GeometryNode containing the symmetric arrangement
    """
    group = GeometryNode(f"{symmetry_type.capitalize()} Symmetry Group")

    # Positions for each symmetry type
    positions = []
    rotations = []

    if symmetry_type == 'tetrahedral':
        # Tetrahedral symmetry (T) - 4 vertices of a tetrahedron
        positions = [
            (1, 1, 1), (-1, -1, 1), (1, -1, -1), (-1, 1, -1)
        ]
        # Normalize the positions
        norm_factor = np.sqrt(3)
        positions = [(x/norm_factor, y/norm_factor, z/norm_factor) for x, y, z in positions]

        # Rotations to align with tetrahedral symmetry
        rotations = [
            (0, 0, 0),
            (2*np.pi/3, 0, 0),
            (4*np.pi/3, 0, 0),
            (0, np.pi, 0)
        ]

    elif symmetry_type == 'octahedral':
        # Octahedral symmetry (O) - 6 vertices along the coordinate axes
        positions = [
            (1, 0, 0), (-1, 0, 0),
            (0, 1, 0), (0, -1, 0),
            (0, 0, 1), (0, 0, -1)
        ]

        # Rotations to align with octahedral symmetry
        rotations = [
            (0, 0, 0),
            (0, np.pi, 0),
            (0, 0, np.pi/2),
            (0, 0, -np.pi/2),
            (np.pi/2, 0, 0),
            (-np.pi/2, 0, 0)
        ]

    elif symmetry_type == 'icosahedral':
        # Icosahedral symmetry (I) - 12 vertices of an icosahedron
        # Using the golden ratio for the coordinates
        phi = (1 + np.sqrt(5)) / 2

        positions = [
            (0, 1, phi), (0, -1, phi), (0, 1, -phi), (0, -1, -phi),
            (1, phi, 0), (-1, phi, 0), (1, -phi, 0), (-1, -phi, 0),
            (phi, 0, 1), (-phi, 0, 1), (phi, 0, -1), (-phi, 0, -1)
        ]

        # Normalize the positions
        norm_factor = np.sqrt(1 + phi**2)
        positions = [(x/norm_factor, y/norm_factor, z/norm_factor) for x, y, z in positions]

        # Using default rotation for each position
        rotations = [(0, 0, 0) for _ in range(len(positions))]

    elif symmetry_type.startswith('dihedral-'):
        # Dihedral symmetry (Dn) - n-fold rotational symmetry with reflections
        try:
            n = int(symmetry_type.split('-')[1])
            if n < 2:
                n = 2  # Minimum value
        except:
            n = 4  # Default to D4

        # Create n equidistant points around a circle
        for i in range(n):
            angle = 2 * np.pi * i / n
            positions.append((np.cos(angle), np.sin(angle), 0))

            # Add a mirror point below the circle
            positions.append((np.cos(angle), np.sin(angle), -0.5))

            # Rotations - align with the radial direction
            rotations.append((0, 0, angle))
            rotations.append((np.pi, 0, angle))

    # Create shapes at the calculated positions
    for i, (position, rotation) in enumerate(zip(positions, rotations)):
        # Create the shape
        shape_data = shape_creator(center=(0, 0, 0), radius=1.0)

        # Create a node with the shape
        node = GeometryNode(f"Shape_{i}", shape_data,
                           color=color, alpha=alpha, position=position)

        # Set the rotation
        node.set_rotation(rotation)

        # Set the scale
        node.scale = scale

        # Add to the group
        group.add_child(node)

    return group

def create_fractal_shape(shape_creator, iterations: int = 3, scale_factor: float = 0.5,
                        base_color: str = 'blue', position_func=None) -> GeometryNode:
    """Create a fractal composition by recursively applying a shape generator.

    Args:
        shape_creator: Function that creates a base shape
        iterations: Number of recursive iterations
        scale_factor: Scale reduction factor for each iteration
        base_color: Base color for the shapes
        position_func: Optional function to determine child positions
                      Function signature: (parent_shape, iteration) -> list of positions

    Returns:
        A GeometryNode containing the fractal composition
    """
    # Create the root node
    root = GeometryNode("Fractal Composition")

    # Create the base shape
    base_shape_data = shape_creator(center=(0, 0, 0), radius=1.0)
    base_node = GeometryNode("Base Shape", base_shape_data, color=base_color, alpha=0.7)
    root.add_child(base_node)

    # Default position function: place children at vertices of parent
    def default_position_func(parent):
        # Get the transformed shape data
        transformed_shape = parent.get_transformed_shape()

        # Extract vertices - handle different shape types
        if 'tetrahedron1' in transformed_shape and 'tetrahedron2' in transformed_shape:
            # For Merkaba, use vertices from both tetrahedra
            vertices1 = transformed_shape['tetrahedron1']['vertices']
            vertices2 = transformed_shape['tetrahedron2']['vertices']
            all_vertices = np.vstack((vertices1, vertices2))
            return [tuple(vertex) for vertex in all_vertices]
        elif 'vertices' in transformed_shape:
            # Standard shape with vertices
            vertices = transformed_shape['vertices']
            return [tuple(vertex) for vertex in vertices]
        else:
            # Fallback: return a single position at the origin
            return [(0, 0, 0)]

    # Use the provided position function or the default
    pos_func = position_func if position_func is not None else default_position_func

    # Recursively add shapes
    def add_recursive_shapes(parent, current_iteration, current_scale):
        # Stop if we've reached the max iterations
        if current_iteration >= iterations:
            return

        # Get positions for the children
        positions = pos_func(parent, current_iteration)

        # Calculate new scale
        new_scale = current_scale * scale_factor

        # Add a shape at each position
        for i, pos in enumerate(positions):
            # Create the shape
            shape_data = shape_creator(center=(0, 0, 0), radius=1.0)

            # Color variation based on iteration level
            color_index = current_iteration % 7  # Cycle through 7 colors
            colors = ['blue', 'red', 'green', 'purple', 'orange', 'cyan', 'magenta']
            color = colors[color_index]

            # Create the node with positioning
            node = GeometryNode(f"Shape_L{current_iteration}_{i}",
                               shape_data, color=color, alpha=0.6 - 0.05 * current_iteration,
                               position=pos)
            node.scale = new_scale

            # Add to parent
            parent.add_child(node)

            # Recursive call for this node
            add_recursive_shapes(node, current_iteration + 1, new_scale)

    # Start the recursion with the base node
    add_recursive_shapes(base_node, 1, 1.0)

    return root

def create_shape_mandala(shape_creator, rings: int = 3, shapes_in_first_ring: int = 6,
                        spiral: bool = False, scale_factor: float = 0.8,
                        height_increment: float = 0.0) -> GeometryNode:
    """Create a mandala-like arrangement of shapes in concentric rings.

    Args:
        shape_creator: Function that creates a shape
        rings: Number of concentric rings
        shapes_in_first_ring: Number of shapes in the first ring
        spiral: Whether to create a spiral pattern by increasing height with each ring
        scale_factor: How much to scale down each successive ring
        height_increment: How much to increase height with each ring if spiral is True

    Returns:
        A GeometryNode containing the mandala arrangement
    """
    # Create the root node
    mandala = GeometryNode("Sacred Geometry Mandala")

    # Create a central shape
    center_shape_data = shape_creator(center=(0, 0, 0), radius=1.0)
    center_node = GeometryNode("Center", center_shape_data, color='gold', alpha=0.7)
    mandala.add_child(center_node)

    # Current scale and height for rings
    current_scale = 1.0
    current_height = 0.0

    # For each ring
    for ring in range(rings):
        # Number of shapes in this ring
        # Each successive ring has more shapes
        n_shapes = shapes_in_first_ring + (ring * shapes_in_first_ring // 2)

        # Update scale for this ring
        current_scale *= scale_factor

        # Update height if creating a spiral
        if spiral:
            current_height += height_increment

        # Create the shapes in this ring
        for i in range(n_shapes):
            # Calculate position in the ring
            angle = 2 * np.pi * i / n_shapes
            ring_radius = (ring + 1) * (1 - scale_factor) * 2  # Increase radius for each ring
            x = ring_radius * np.cos(angle)
            y = ring_radius * np.sin(angle)
            z = current_height

            # Create the shape
            shape_data = shape_creator(center=(0, 0, 0), radius=1.0)

            # Choose color - alternate between rings
            color_index = ring % 4
            colors = ['blue', 'purple', 'cyan', 'teal']
            color = colors[color_index]

            # Create the node
            node = GeometryNode(f"Ring{ring}_Shape{i}",
                              shape_data, color=color, alpha=0.6,
                              position=(x, y, z))

            # Set rotation to face center
            node.set_rotation((0, 0, angle + np.pi/2))

            # Set scale
            node.scale = current_scale

            # Add to mandala
            mandala.add_child(node)

    return mandala

def create_geometric_progression(shape_data: Dict,
                               count: int = 5,
                               ratio: str = 'phi',
                               direction: Tuple[float, float, float] = (1, 0, 0),
                               base_color: str = 'blue') -> GeometryNode:
    """Create a progression of shapes scaled and positioned according to a sacred ratio.

    Args:
        shape_data: Shape data dictionary for the base shape
        count: Number of shapes in the progression
        ratio: Sacred ratio for scaling ('phi', 'sqrt2', 'sqrt3', etc.)
        direction: Direction vector for the progression
        base_color: Base color for the shapes

    Returns:
        A GeometryNode containing the progression
    """
    # Create the root node
    progression = GeometryNode(f"{ratio.capitalize()} Progression")

    # Get the ratio value
    ratio_value = 1.0
    if ratio == 'phi':
        ratio_value = PHI
    elif ratio == 'sqrt2':
        ratio_value = SQRT2
    elif ratio == 'sqrt3':
        ratio_value = SQRT3
    elif ratio == '1/phi':
        ratio_value = 1.0 / PHI

    # Normalize the direction vector
    norm = np.sqrt(direction[0]**2 + direction[1]**2 + direction[2]**2)
    if norm > 0:
        direction = (direction[0]/norm, direction[1]/norm, direction[2]/norm)

    # Current position and scale
    current_position = (0, 0, 0)
    current_scale = 1.0

    # Create colors with varying transparency
    colors = []
    for i in range(count):
        if i == 0:
            colors.append((base_color, 0.8))  # Start with high alpha
        else:
            # Gradually reduce alpha for distant shapes
            alpha = max(0.3, 0.8 - (i * 0.1))
            colors.append((base_color, alpha))

    # Create each shape in the progression
    for i in range(count):
        # Create a copy of the node with the current position and scale
        node = GeometryNode(f"Shape_{i}",
                          shape_data,
                          color=colors[i][0],
                          alpha=colors[i][1],
                          position=current_position)
        node.scale = current_scale

        # Add to progression
        progression.add_child(node)

        # Update position and scale for next shape
        offset = ratio_value ** i  # Use powers of the ratio for spacing
        next_x = current_position[0] + direction[0] * offset
        next_y = current_position[1] + direction[1] * offset
        next_z = current_position[2] + direction[2] * offset
        current_position = (next_x, next_y, next_z)

        # Scale reduces with each step
        current_scale /= ratio_value

    return progression

# Symmetry transformation functions
def rotate_around_axis(node: GeometryNode, axis: str, angle: float) -> None:
    """Rotate a node around a specific axis.

    Args:
        node: The GeometryNode to rotate
        axis: Axis to rotate around ('x', 'y', or 'z')
        angle: Angle in radians
    """
    rx, ry, rz = node.rotation_xyz

    if axis.lower() == 'x':
        node.set_rotation((rx + angle, ry, rz))
    elif axis.lower() == 'y':
        node.set_rotation((rx, ry + angle, rz))
    elif axis.lower() == 'z':
        node.set_rotation((rx, ry, rz + angle))

def mirror_across_plane(node: GeometryNode, plane: str) -> GeometryNode:
    """Create a mirrored copy of a node across a coordinate plane.

    Args:
        node: The GeometryNode to mirror
        plane: Plane to mirror across ('xy', 'xz', or 'yz')

    Returns:
        A new GeometryNode that is the mirror of the original
    """
    # Make a copy of the node
    mirrored = copy.deepcopy(node)
    mirrored.name = f"{node.name}_mirrored"

    # Get the current position
    x, y, z = node.position

    # Get the current rotation
    rx, ry, rz = node.rotation_xyz

    # Mirror position and rotation based on the plane
    if plane.lower() == 'xy':
        mirrored.position = (x, y, -z)
        mirrored.set_rotation((-rx, -ry, rz))
    elif plane.lower() == 'xz':
        mirrored.position = (x, -y, z)
        mirrored.set_rotation((-rx, ry, -rz))
    elif plane.lower() == 'yz':
        mirrored.position = (-x, y, z)
        mirrored.set_rotation((rx, -ry, -rz))

    return mirrored

def apply_radial_symmetry(node: GeometryNode, count: int, axis: str = 'z') -> List[GeometryNode]:
    """Create copies of a node with radial symmetry around an axis.

    Args:
        node: The GeometryNode to replicate
        count: Number of copies to create
        axis: Axis to rotate around ('x', 'y', or 'z')

    Returns:
        A list of new GeometryNodes arranged with radial symmetry
    """
    results = []

    # Angle increment
    angle_step = 2 * np.pi / count

    for i in range(count):
        # Make a copy of the node
        if i == 0:
            copy_node = node  # Use the original for the first one
        else:
            copy_node = copy.deepcopy(node)
            copy_node.name = f"{node.name}_{i}"

        # Calculate the rotation angle
        angle = i * angle_step

        # Get the current position
        x, y, z = node.position

        # Apply rotation to the position
        if axis.lower() == 'z':
            new_x = x * np.cos(angle) - y * np.sin(angle)
            new_y = x * np.sin(angle) + y * np.cos(angle)
            new_z = z
            # Also rotate around z-axis
            rx, ry, rz = node.rotation_xyz
            copy_node.set_rotation((rx, ry, rz + angle))
        elif axis.lower() == 'y':
            new_x = x * np.cos(angle) - z * np.sin(angle)
            new_y = y
            new_z = x * np.sin(angle) + z * np.cos(angle)
            # Also rotate around y-axis
            rx, ry, rz = node.rotation_xyz
            copy_node.set_rotation((rx, ry + angle, rz))
        elif axis.lower() == 'x':
            new_x = x
            new_y = y * np.cos(angle) - z * np.sin(angle)
            new_z = y * np.sin(angle) + z * np.cos(angle)
            # Also rotate around x-axis
            rx, ry, rz = node.rotation_xyz
            copy_node.set_rotation((rx + angle, ry, rz))

        # Set the new position
        copy_node.position = (new_x, new_y, new_z)

        # Add to results
        results.append(copy_node)

    return results