"""
Fractal generators for sacred geometry.
"""
import numpy as np
from typing import List, Tuple, Dict, Any, Optional, Union
from ..core.core import create_circle, create_regular_polygon

def sierpinski_triangle(points: np.ndarray, depth: int) -> List[np.ndarray]:
    """
    Generate a Sierpinski triangle fractal.
    
    Args:
        points: Initial triangle vertices as a 3x2 array
        depth: Recursion depth
        
    Returns:
        List of triangles (each as a 3x2 array of vertices)
    """
    if depth == 0:
        return [points]
    
    # Get midpoints of each side of the triangle
    midpoints = np.array([
        (points[0] + points[1]) / 2,
        (points[1] + points[2]) / 2,
        (points[2] + points[0]) / 2
    ])
    
    # Create three new triangles
    triangles = []
    
    # Top triangle
    triangles.extend(sierpinski_triangle(
        np.array([points[0], midpoints[0], midpoints[2]]),
        depth - 1
    ))
    
    # Bottom left triangle
    triangles.extend(sierpinski_triangle(
        np.array([midpoints[0], points[1], midpoints[1]]),
        depth - 1
    ))
    
    # Bottom right triangle
    triangles.extend(sierpinski_triangle(
        np.array([midpoints[2], midpoints[1], points[2]]),
        depth - 1
    ))
    
    return triangles

def koch_snowflake(points: np.ndarray, depth: int) -> np.ndarray:
    """
    Generate a Koch snowflake fractal.
    
    Args:
        points: Initial polygon vertices
        depth: Recursion depth
        
    Returns:
        Array of points representing the Koch snowflake
    """
    if depth == 0:
        return points
    
    result = []
    n = len(points)
    
    for i in range(n):
        # Get start and end points of this segment
        start = points[i]
        end = points[(i + 1) % n]
        
        # Calculate the four new points that replace this segment
        segment = end - start
        p1 = start
        p2 = start + segment / 3
        
        # Calculate the position of the new peak
        # Rotate the vector from p2 to p3 by 60 degrees
        angle = np.pi / 3  # 60 degrees
        cos_angle = np.cos(angle)
        sin_angle = np.sin(angle)
        segment_third = segment / 3
        p3_x = p2[0] + cos_angle * segment_third[0] - sin_angle * segment_third[1]
        p3_y = p2[1] + sin_angle * segment_third[0] + cos_angle * segment_third[1]
        p3 = np.array([p3_x, p3_y])
        
        p4 = start + 2 * segment / 3
        
        # Add the new points to the result
        result.append(p1)
        result.append(p2)
        result.append(p3)
        result.append(p4)
    
    # Convert to numpy array and recurse
    new_points = np.array(result)
    return koch_snowflake(new_points, depth - 1)

def mandelbrot_set(
    xmin: float = -2.0, xmax: float = 1.0, 
    ymin: float = -1.5, ymax: float = 1.5,
    width: int = 1000, height: int = 1000,
    max_iter: int = 100, escape_radius: float = 2.0
) -> np.ndarray:
    """
    Generate the Mandelbrot set.
    
    Args:
        xmin, xmax, ymin, ymax: The region of the complex plane to plot
        width, height: Image dimensions
        max_iter: Maximum number of iterations
        escape_radius: Escape radius for the iterations
        
    Returns:
        2D array of iteration counts
    """
    x = np.linspace(xmin, xmax, width)
    y = np.linspace(ymin, ymax, height)
    c = x.reshape((1, width)) + 1j * y.reshape((height, 1))
    
    z = np.zeros_like(c, dtype=complex)
    escape_time = np.zeros_like(c, dtype=int)
    mask = np.full_like(escape_time, True, dtype=bool)
    
    for i in range(max_iter):
        # Compute z = z^2 + c for all points
        z[mask] = z[mask]**2 + c[mask]
        
        # Find points that escape
        escaped = np.abs(z) > escape_radius
        
        # Update escape times for newly escaped points
        escape_time[escaped & mask] = i
        
        # Update mask
        mask = mask & (~escaped)
        
        # If all points have escaped, break
        if not np.any(mask):
            break
    
    return escape_time

def julia_set(
    c: complex = -0.7 + 0.27j,  # Parameter that defines the specific Julia set
    xmin: float = -1.5, xmax: float = 1.5, 
    ymin: float = -1.5, ymax: float = 1.5,
    width: int = 1000, height: int = 1000,
    max_iter: int = 100, escape_radius: float = 2.0
) -> np.ndarray:
    """
    Generate a Julia set.
    
    Args:
        c: Complex parameter that defines the specific Julia set
        xmin, xmax, ymin, ymax: The region of the complex plane to plot
        width, height: Image dimensions
        max_iter: Maximum number of iterations
        escape_radius: Escape radius for the iterations
        
    Returns:
        2D array of iteration counts
    """
    x = np.linspace(xmin, xmax, width)
    y = np.linspace(ymin, ymax, height)
    z = x.reshape((1, width)) + 1j * y.reshape((height, 1))
    
    escape_time = np.zeros_like(z, dtype=int)
    mask = np.full_like(escape_time, True, dtype=bool)
    
    for i in range(max_iter):
        # Compute z = z^2 + c for all points
        z[mask] = z[mask]**2 + c
        
        # Find points that escape
        escaped = np.abs(z) > escape_radius
        
        # Update escape times for newly escaped points
        escape_time[escaped & mask] = i
        
        # Update mask
        mask = mask & (~escaped)
        
        # If all points have escaped, break
        if not np.any(mask):
            break
    
    return escape_time

def dragon_curve(iterations: int = 10) -> np.ndarray:
    """
    Generate the dragon curve fractal.
    
    Args:
        iterations: Number of iterations
        
    Returns:
        Array of points representing the curve
    """
    # Start with a simple line segment
    curve = np.array([[0, 0], [1, 0]])
    
    for _ in range(iterations):
        n = len(curve)
        new_curve = np.zeros((2 * n - 1, 2))
        
        # Copy the first half of the curve
        new_curve[:n] = curve
        
        # Calculate midpoint of the curve
        midpoint = (curve[0] + curve[-1]) / 2
        
        # For each point in the second half, rotate around the midpoint
        for i in range(n-1):
            # Rotate the point 90 degrees around the midpoint
            x = curve[n-i-2, 0] - midpoint[0]
            y = curve[n-i-2, 1] - midpoint[1]
            
            # 90 degree rotation
            rotated_x = -y + midpoint[0]
            rotated_y = x + midpoint[1]
            
            new_curve[n+i] = [rotated_x, rotated_y]
        
        curve = new_curve
    
    return curve

def recursive_flower_of_life(center: Tuple[float, float], radius: float, 
                           levels: int = 3) -> List[np.ndarray]:
    """
    Generate a recursive Flower of Life pattern.
    
    Args:
        center: (x, y) coordinates of the center
        radius: Radius of the initial circle
        levels: Number of recursive levels
        
    Returns:
        List of circles representing the pattern
    """
    from ..core.core import create_flower_of_life
    
    if levels <= 0:
        return [create_circle(center, radius)]
    
    # Start with the basic Flower of Life
    circles = create_flower_of_life(center, radius, layers=1)
    
    # For each level, add smaller Flowers of Life at each new circle
    if levels > 1:
        # Extract centers of the outer circles
        outer_centers = []
        for i, circle in enumerate(circles):
            if i > 0:  # Skip the center circle
                # Calculate the center
                points = circle
                x_avg = (points[0, 0] + points[points.shape[0]//2, 0]) / 2
                y_avg = (points[0, 1] + points[points.shape[0]//2, 1]) / 2
                outer_centers.append((x_avg, y_avg))
        
        # Create recursive Flowers of Life at each outer center
        for outer_center in outer_centers:
            smaller_circles = recursive_flower_of_life(
                outer_center, radius / 3, levels - 1
            )
            circles.extend(smaller_circles)
    
    return circles

def hilbert_curve(order: int = 3, size: float = 10.0) -> np.ndarray:
    """
    Generate a Hilbert curve fractal.
    
    Args:
        order: Order of the Hilbert curve
        size: Size of the resulting curve
        
    Returns:
        Array of points representing the curve
    """
    # Hilbert curve helper function
    def hilbert(x0, y0, xi, xj, yi, yj, n):
        if n <= 0:
            X = x0 + (xi + yi) / 2
            Y = y0 + (xj + yj) / 2
            return np.array([[X, Y]])
        
        # Recursively generate the four quadrants
        points = np.vstack([
            hilbert(x0, y0, yi/2, yj/2, xi/2, xj/2, n-1),
            hilbert(x0 + xi/2, y0 + xj/2, xi/2, xj/2, yi/2, yj/2, n-1),
            hilbert(x0 + xi/2 + yi/2, y0 + xj/2 + yj/2, xi/2, xj/2, yi/2, yj/2, n-1),
            hilbert(x0 + xi/2 + yi, y0 + xj/2 + yj, -yi/2, -yj/2, -xi/2, -xj/2, n-1)
        ])
        
        return points
    
    return hilbert(0, 0, size, 0, 0, size, order)

def sacred_spiral(center: Tuple[float, float], 
                 start_radius: float = 0.1, 
                 max_radius: float = 10.0, 
                 turns: float = 5.0,
                 points_per_turn: int = 100) -> np.ndarray:
    """
    Generate a sacred spiral based on the golden ratio.
    
    Args:
        center: (x, y) coordinates of the center
        start_radius: Starting radius
        max_radius: Maximum radius
        turns: Number of complete turns
        points_per_turn: Number of points per turn
        
    Returns:
        Array of points representing the spiral
    """
    # Golden ratio
    phi = (1 + np.sqrt(5)) / 2
    
    # Calculate number of points
    num_points = int(points_per_turn * turns)
    
    # Generate the spiral
    theta = np.linspace(0, turns * 2 * np.pi, num_points)
    
    # Logarithmic spiral formula based on golden ratio
    a = start_radius
    b = np.log(phi) / (np.pi / 2)  # Growth factor based on golden ratio
    
    r = a * np.exp(b * theta)
    
    # Limit to max radius
    r = np.minimum(r, max_radius)
    
    # Convert to Cartesian coordinates
    x = center[0] + r * np.cos(theta)
    y = center[1] + r * np.sin(theta)
    
    return np.column_stack((x, y))

def fractal_tree(start: Tuple[float, float], angle: float = np.pi/2, 
               length: float = 1.0, depth: int = 5, 
               length_factor: float = 0.7, angle_delta: float = np.pi/7) -> List[np.ndarray]:
    """
    Generate a fractal tree.
    
    Args:
        start: (x, y) coordinates of the starting point
        angle: Initial angle (radians)
        length: Length of the initial branch
        depth: Recursion depth
        length_factor: Factor to reduce length at each recursion
        angle_delta: Amount to change angle at each recursion
        
    Returns:
        List of line segments (each as a 2x2 array)
    """
    if depth <= 0:
        return []
    
    # Calculate end point of the current branch
    end_x = start[0] + length * np.cos(angle)
    end_y = start[1] + length * np.sin(angle)
    end = (end_x, end_y)
    
    # Create current branch
    branch = np.array([start, end])
    
    # Create left and right branches (recursively)
    left_branches = fractal_tree(
        end, angle + angle_delta, length * length_factor, 
        depth - 1, length_factor, angle_delta
    )
    
    right_branches = fractal_tree(
        end, angle - angle_delta, length * length_factor, 
        depth - 1, length_factor, angle_delta
    )
    
    # Combine all branches
    all_branches = [branch] + left_branches + right_branches
    
    return all_branches