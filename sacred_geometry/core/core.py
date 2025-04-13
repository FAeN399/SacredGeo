"""
Core geometric primitives and operations for sacred geometry.
"""
import numpy as np
import sympy as sp
from typing import List, Tuple, Union, Optional

# Fundamental 2D shape components
def create_circle(center: Tuple[float, float], radius: float, 
                 num_points: int = 100) -> np.ndarray:
    """
    Create a circle with the given center and radius.
    
    Args:
        center: (x, y) coordinates of the circle center
        radius: Radius of the circle
        num_points: Number of points to use for the circle representation
        
    Returns:
        Array of points representing the circle
    """
    theta = np.linspace(0, 2 * np.pi, num_points)
    x = center[0] + radius * np.cos(theta)
    y = center[1] + radius * np.sin(theta)
    return np.column_stack((x, y))

def create_regular_polygon(center: Tuple[float, float], radius: float, 
                          sides: int, rotation: float = 0) -> np.ndarray:
    """
    Create a regular polygon with the given center, radius, and number of sides.
    
    Args:
        center: (x, y) coordinates of the polygon center
        radius: Distance from center to vertices
        sides: Number of sides
        rotation: Rotation angle in radians
        
    Returns:
        Array of points representing the polygon vertices
    """
    theta = np.linspace(0, 2 * np.pi, sides, endpoint=False) + rotation
    x = center[0] + radius * np.cos(theta)
    y = center[1] + radius * np.sin(theta)
    return np.column_stack((x, y))

def create_golden_rectangle(center: Tuple[float, float], 
                          width: float) -> np.ndarray:
    """
    Create a golden rectangle with the given center and width.
    
    Args:
        center: (x, y) coordinates of the rectangle center
        width: Width of the rectangle
        
    Returns:
        Array of 4 points representing the rectangle vertices
    """
    # Golden ratio
    phi = (1 + np.sqrt(5)) / 2
    height = width / phi
    
    half_width = width / 2
    half_height = height / 2
    
    x = center[0]
    y = center[1]
    
    # Create vertices (counter-clockwise)
    vertices = np.array([
        [x - half_width, y - half_height],  # bottom-left
        [x + half_width, y - half_height],  # bottom-right
        [x + half_width, y + half_height],  # top-right
        [x - half_width, y + half_height]   # top-left
    ])
    
    return vertices

def intersect_circles(center1: Tuple[float, float], radius1: float,
                     center2: Tuple[float, float], radius2: float) -> np.ndarray:
    """
    Find the intersection points of two circles.
    
    Args:
        center1: (x, y) coordinates of the first circle center
        radius1: Radius of the first circle
        center2: (x, y) coordinates of the second circle center
        radius2: Radius of the second circle
        
    Returns:
        Array of intersection points (empty if no intersections)
    """
    x1, y1 = center1
    x2, y2 = center2
    
    # Distance between the centers
    d = np.sqrt((x2 - x1)**2 + (y2 - y1)**2)
    
    # Check if circles are too far apart or one is inside the other
    if d > radius1 + radius2 or d < abs(radius1 - radius2):
        return np.array([])  # No intersection
    
    # Calculate intersection points
    a = (radius1**2 - radius2**2 + d**2) / (2 * d)
    h = np.sqrt(radius1**2 - a**2)
    
    x3 = x1 + a * (x2 - x1) / d
    y3 = y1 + a * (y2 - y1) / d
    
    # Intersection points
    int_x1 = x3 + h * (y2 - y1) / d
    int_y1 = y3 - h * (x2 - x1) / d
    int_x2 = x3 - h * (y2 - y1) / d
    int_y2 = y3 + h * (x2 - x1) / d
    
    # If circles are tangent, return just one point
    if d == radius1 + radius2 or d == abs(radius1 - radius2):
        return np.array([[int_x1, int_y1]])
    
    return np.array([[int_x1, int_y1], [int_x2, int_y2]])

def create_seed_of_life(center: Tuple[float, float], radius: float) -> List[np.ndarray]:
    """
    Create the Seed of Life pattern.
    
    Args:
        center: (x, y) coordinates of the center
        radius: Radius of each circle
        
    Returns:
        List of arrays, each representing a circle in the pattern
    """
    circles = []
    
    # Center circle
    circles.append(create_circle(center, radius))
    
    # Six surrounding circles
    for i in range(6):
        angle = i * np.pi / 3
        x = center[0] + radius * np.cos(angle)
        y = center[1] + radius * np.sin(angle)
        circles.append(create_circle((x, y), radius))
    
    return circles

def create_flower_of_life(center: Tuple[float, float], radius: float, 
                         layers: int = 2) -> List[np.ndarray]:
    """
    Create the Flower of Life pattern with a specified number of layers.
    
    Args:
        center: (x, y) coordinates of the center
        radius: Radius of each circle
        layers: Number of layers of circles around the center
        
    Returns:
        List of arrays, each representing a circle in the pattern
    """
    circles = []
    points = set()  # Keep track of circle centers
    
    # Add the center circle
    circles.append(create_circle(center, radius))
    points.add(center)
    
    for layer in range(1, layers + 1):
        # For each existing point, create 6 circles around it
        new_points = set()
        for point in points:
            for i in range(6):
                angle = i * np.pi / 3
                x = point[0] + radius * np.cos(angle)
                y = point[1] + radius * np.sin(angle)
                new_point = (round(x, 6), round(y, 6))  # Round to avoid floating point issues
                
                if new_point not in points:
                    new_points.add(new_point)
        
        # Add new circles
        for point in new_points:
            circles.append(create_circle(point, radius))
        
        points.update(new_points)
    
    return circles

def create_metatrons_cube(center: Tuple[float, float], radius: float) -> dict:
    """
    Create Metatron's Cube based on the Fruit of Life pattern.
    
    Args:
        center: (x, y) coordinates of the center
        radius: Radius of each circle in the Fruit of Life
        
    Returns:
        Dictionary containing the Fruit of Life circles and the lines of Metatron's Cube
    """
    # First create the Fruit of Life (13 circles)
    circles = create_flower_of_life(center, radius, layers=2)
    
    # Extract the centers of all circles (these are the vertices of Metatron's Cube)
    vertices = []
    for i, circle in enumerate(circles):
        if i == 0:
            # Center circle
            vertices.append(center)
        else:
            # Get the center from the first point and the radius
            points = circle
            x_avg = (points[0, 0] + points[points.shape[0]//2, 0]) / 2
            y_avg = (points[0, 1] + points[points.shape[0]//2, 1]) / 2
            vertices.append((x_avg, y_avg))
    
    # Create lines connecting all vertices
    lines = []
    for i in range(len(vertices)):
        for j in range(i+1, len(vertices)):
            lines.append((vertices[i], vertices[j]))
    
    return {
        'circles': circles,
        'vertices': vertices,
        'lines': lines
    }

def create_vesica_piscis(center1: Tuple[float, float], center2: Tuple[float, float], 
                        radius: float) -> dict:
    """
    Create a Vesica Piscis from two overlapping circles.
    
    Args:
        center1: (x, y) coordinates of the first circle center
        center2: (x, y) coordinates of the second circle center
        radius: Radius of both circles
        
    Returns:
        Dictionary containing the two circles and their intersection points
    """
    circle1 = create_circle(center1, radius)
    circle2 = create_circle(center2, radius)
    
    intersection_points = intersect_circles(center1, radius, center2, radius)
    
    return {
        'circle1': circle1,
        'circle2': circle2,
        'intersection_points': intersection_points
    }

# Golden ratio and Fibonacci functions
def get_golden_ratio() -> float:
    """
    Return the golden ratio φ (phi).
    
    Returns:
        The golden ratio as a float
    """
    return (1 + np.sqrt(5)) / 2

def generate_fibonacci_sequence(n: int) -> List[int]:
    """
    Generate the first n numbers in the Fibonacci sequence.
    
    Args:
        n: Number of Fibonacci numbers to generate
        
    Returns:
        List of the first n Fibonacci numbers
    """
    if n <= 0:
        return []
    if n == 1:
        return [1]
    if n == 2:
        return [1, 1]
    
    fib = [1, 1]
    for i in range(2, n):
        fib.append(fib[i-1] + fib[i-2])
    
    return fib

def create_fibonacci_spiral(center: Tuple[float, float], scale: float, 
                          n_iterations: int = 8) -> dict:
    """
    Create a Fibonacci spiral.
    
    Args:
        center: (x, y) coordinates of the center
        scale: Scale factor for the spiral
        n_iterations: Number of iterations for the spiral
        
    Returns:
        Dictionary containing the squares and the spiral curve points
    """
    fibonacci = generate_fibonacci_sequence(n_iterations)
    squares = []
    spiral_points = []
    
    x, y = center
    angle = 0
    
    for i in range(len(fibonacci)):
        side = fibonacci[i] * scale
        
        # Calculate square vertices based on current position and angle
        if i > 0:  # Skip first square for spiral calculation
            # Create arc points for this quarter of the spiral
            radius = fibonacci[i-1] * scale
            start_angle = angle
            end_angle = angle + np.pi/2
            arc_points = np.linspace(start_angle, end_angle, 20)
            for theta in arc_points:
                px = x + radius * np.cos(theta)
                py = y + radius * np.sin(theta)
                spiral_points.append((px, py))
        
        # Update position for next square
        if i % 4 == 0:
            x += side
        elif i % 4 == 1:
            y -= side
        elif i % 4 == 2:
            x -= side
        else:  # i % 4 == 3
            y += side
        
        # Calculate square vertices
        square = {
            'side': side,
            'position': (x, y),
            'angle': angle
        }
        squares.append(square)
        
        # Update angle for next iteration
        angle += np.pi/2
    
    return {
        'squares': squares,
        'spiral': np.array(spiral_points)
    }