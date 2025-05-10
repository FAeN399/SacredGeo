"""
Sacred Geometry Color Schemes Module

This module provides color schemes and palettes for sacred geometry visualizations.
It includes functions for color mapping, gradient generation, and custom color creation.
"""
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from typing import List, Tuple, Dict, Any, Union, Optional, Callable
import colorsys

# Type aliases
RGB = Tuple[float, float, float]  # RGB color tuple (0-1 range)
RGBA = Tuple[float, float, float, float]  # RGBA color tuple (0-1 range)
ColorType = Union[str, RGB, RGBA]  # A color can be a string name, RGB, or RGBA tuple

# Predefined color schemes
COLOR_SCHEMES: Dict[str, Dict[str, Any]] = {
    "rainbow": {
        "description": "Full spectrum rainbow colors",
        "colors": ["#FF0000", "#FF7F00", "#FFFF00", "#00FF00", "#0000FF", "#4B0082", "#9400D3"],
        "cmap": "rainbow",
        "background": "#1a1a2e",
        "edge_color": "#ffffff",
        "point_color": "#ffffff"
    },
    "golden": {
        "description": "Gold and amber tones representing divine light",
        "colors": ["#FFD700", "#FFC107", "#FF9800", "#FF5722", "#F4511E", "#BF360C", "#3E2723"],
        "cmap": "YlOrBr",
        "background": "#1a1a2e",
        "edge_color": "#daa520",
        "point_color": "#ffd700"
    },
    "monochrome": {
        "description": "Single color with varying shades",
        "colors": ["#E0E0E0", "#C0C0C0", "#A0A0A0", "#808080", "#606060", "#404040", "#202020"],
        "cmap": "Greys",
        "background": "#1a1a2e",
        "edge_color": "#e0e0e0",
        "point_color": "#ffffff"
    },
    "custom": {
        "description": "User-defined custom colors",
        "colors": ["#FF5252", "#FF4081", "#E040FB", "#7C4DFF", "#536DFE", "#448AFF", "#40C4FF"],
        "cmap": "viridis",
        "background": "#1a1a2e",
        "edge_color": "#ffffff",
        "point_color": "#ffffff"
    },
    "fire": {
        "description": "Fiery reds, oranges, and yellows",
        "colors": ["#FFEB3B", "#FFC107", "#FF9800", "#FF5722", "#F44336", "#E91E63", "#9C27B0"],
        "cmap": "inferno",
        "background": "#1a1a2e",
        "edge_color": "#ff5722",
        "point_color": "#ffeb3b"
    },
    "ice": {
        "description": "Cool blues and cyans",
        "colors": ["#E1F5FE", "#B3E5FC", "#81D4FA", "#4FC3F7", "#29B6F6", "#03A9F4", "#0288D1"],
        "cmap": "cool",
        "background": "#1a1a2e",
        "edge_color": "#81d4fa",
        "point_color": "#e1f5fe"
    },
    "earth": {
        "description": "Natural earth tones",
        "colors": ["#795548", "#6D4C41", "#5D4037", "#4E342E", "#3E2723", "#8D6E63", "#A1887F"],
        "cmap": "YlOrBr",
        "background": "#1a1a2e",
        "edge_color": "#a1887f",
        "point_color": "#d7ccc8"
    },
    "chakra": {
        "description": "Colors representing the seven chakras",
        "colors": ["#FF0000", "#FF7F00", "#FFFF00", "#00FF00", "#0000FF", "#4B0082", "#9400D3"],
        "cmap": "rainbow",
        "background": "#1a1a2e",
        "edge_color": "#ffffff",
        "point_color": "#ffffff"
    },
    "ethereal": {
        "description": "Soft, luminous pastel colors",
        "colors": ["#B39DDB", "#9FA8DA", "#90CAF9", "#81D4FA", "#80DEEA", "#80CBC4", "#A5D6A7"],
        "cmap": "plasma",
        "background": "#1a1a2e",
        "edge_color": "#b39ddb",
        "point_color": "#e1bee7"
    },
    "cosmic": {
        "description": "Deep space-inspired colors",
        "colors": ["#311B92", "#4527A0", "#512DA8", "#5E35B1", "#673AB7", "#7E57C2", "#9575CD"],
        "cmap": "magma",
        "background": "#0a0a1e",
        "edge_color": "#7e57c2",
        "point_color": "#d1c4e9"
    },
    "energy": {
        "description": "Vibrant energy colors",
        "colors": ["#FFEB3B", "#FFC107", "#FF9800", "#FF5722", "#F44336", "#E91E63", "#9C27B0"],
        "cmap": "plasma",
        "background": "#1a1a2e",
        "edge_color": "#ff5722",
        "point_color": "#ffeb3b"
    },
    "crystal": {
        "description": "Translucent crystal-like colors",
        "colors": ["#B3E5FC", "#81D4FA", "#4FC3F7", "#29B6F6", "#03A9F4", "#0288D1", "#0277BD"],
        "cmap": "cool",
        "background": "#1a1a2e",
        "edge_color": "#81d4fa",
        "point_color": "#e1f5fe",
        "alpha": 0.7
    }
}

# Material properties for 3D rendering
MATERIAL_PROPERTIES: Dict[str, Dict[str, Any]] = {
    "matte": {
        "description": "Non-reflective matte surface",
        "ambient": 0.3,
        "diffuse": 0.7,
        "specular": 0.1,
        "shininess": 10,
        "alpha": 1.0
    },
    "metallic": {
        "description": "Reflective metallic surface",
        "ambient": 0.2,
        "diffuse": 0.4,
        "specular": 0.9,
        "shininess": 100,
        "alpha": 0.9
    },
    "glass": {
        "description": "Transparent glass-like surface",
        "ambient": 0.1,
        "diffuse": 0.2,
        "specular": 0.8,
        "shininess": 50,
        "alpha": 0.4
    },
    "crystal": {
        "description": "Semi-transparent crystal-like surface",
        "ambient": 0.2,
        "diffuse": 0.3,
        "specular": 0.9,
        "shininess": 80,
        "alpha": 0.6
    },
    "energy": {
        "description": "Glowing energy-like surface",
        "ambient": 0.5,
        "diffuse": 0.7,
        "specular": 0.9,
        "shininess": 30,
        "alpha": 0.8,
        "emissive": 0.5
    }
}

def get_color_scheme(scheme_name: str) -> Dict[str, Any]:
    """
    Get a color scheme by name.
    
    Args:
        scheme_name: Name of the color scheme
        
    Returns:
        Dictionary containing color scheme information
    """
    scheme_name = scheme_name.lower()
    if scheme_name in COLOR_SCHEMES:
        return COLOR_SCHEMES[scheme_name]
    else:
        print(f"Warning: Color scheme '{scheme_name}' not found. Using 'golden' as default.")
        return COLOR_SCHEMES["golden"]

def get_material_properties(material_name: str) -> Dict[str, Any]:
    """
    Get material properties by name.
    
    Args:
        material_name: Name of the material
        
    Returns:
        Dictionary containing material properties
    """
    material_name = material_name.lower()
    if material_name in MATERIAL_PROPERTIES:
        return MATERIAL_PROPERTIES[material_name]
    else:
        print(f"Warning: Material '{material_name}' not found. Using 'matte' as default.")
        return MATERIAL_PROPERTIES["matte"]

def create_color_gradient(
    start_color: ColorType,
    end_color: ColorType,
    num_colors: int = 10
) -> List[str]:
    """
    Create a gradient between two colors.
    
    Args:
        start_color: Starting color
        end_color: Ending color
        num_colors: Number of colors in the gradient
        
    Returns:
        List of hex color strings
    """
    # Convert input colors to RGB tuples if they're strings
    if isinstance(start_color, str):
        start_rgb = mcolors.to_rgb(start_color)
    else:
        start_rgb = start_color[:3]  # Take only RGB components
    
    if isinstance(end_color, str):
        end_rgb = mcolors.to_rgb(end_color)
    else:
        end_rgb = end_color[:3]  # Take only RGB components
    
    # Create gradient
    gradient = []
    for i in range(num_colors):
        r = start_rgb[0] + (end_rgb[0] - start_rgb[0]) * i / (num_colors - 1)
        g = start_rgb[1] + (end_rgb[1] - start_rgb[1]) * i / (num_colors - 1)
        b = start_rgb[2] + (end_rgb[2] - start_rgb[2]) * i / (num_colors - 1)
        gradient.append(mcolors.to_hex((r, g, b)))
    
    return gradient

def create_rainbow_gradient(num_colors: int = 10) -> List[str]:
    """
    Create a rainbow gradient with the specified number of colors.
    
    Args:
        num_colors: Number of colors in the gradient
        
    Returns:
        List of hex color strings
    """
    gradient = []
    for i in range(num_colors):
        # Convert HSV to RGB (hue varies from 0 to 1)
        h = i / num_colors
        r, g, b = colorsys.hsv_to_rgb(h, 1.0, 1.0)
        gradient.append(mcolors.to_hex((r, g, b)))
    
    return gradient

def create_golden_gradient(num_colors: int = 10) -> List[str]:
    """
    Create a gradient of golden hues.
    
    Args:
        num_colors: Number of colors in the gradient
        
    Returns:
        List of hex color strings
    """
    # Golden hues range from yellow to amber to deep gold
    return create_color_gradient("#FFD700", "#B8860B", num_colors)

def create_custom_gradient(
    colors: List[ColorType],
    num_colors: int = 10
) -> List[str]:
    """
    Create a custom gradient using multiple color points.
    
    Args:
        colors: List of colors to use as gradient points
        num_colors: Total number of colors in the final gradient
        
    Returns:
        List of hex color strings
    """
    if len(colors) < 2:
        raise ValueError("At least two colors are required to create a gradient")
    
    # Convert all colors to RGB tuples
    rgb_colors = []
    for color in colors:
        if isinstance(color, str):
            rgb_colors.append(mcolors.to_rgb(color))
        else:
            rgb_colors.append(color[:3])  # Take only RGB components
    
    # Calculate how many colors to generate between each pair of input colors
    n_segments = len(rgb_colors) - 1
    colors_per_segment = [num_colors // n_segments] * n_segments
    
    # Distribute any remainder
    remainder = num_colors - sum(colors_per_segment)
    for i in range(remainder):
        colors_per_segment[i] += 1
    
    # Generate the gradient
    gradient = []
    for i in range(n_segments):
        start_rgb = rgb_colors[i]
        end_rgb = rgb_colors[i+1]
        segment_size = colors_per_segment[i]
        
        for j in range(segment_size):
            t = j / (segment_size - 1 if segment_size > 1 else 1)
            r = start_rgb[0] + (end_rgb[0] - start_rgb[0]) * t
            g = start_rgb[1] + (end_rgb[1] - start_rgb[1]) * t
            b = start_rgb[2] + (end_rgb[2] - start_rgb[2]) * t
            gradient.append(mcolors.to_hex((r, g, b)))
    
    return gradient

def apply_color_to_pattern(
    pattern: Any,
    color_scheme: str = "golden",
    alpha: float = 1.0
) -> Dict[str, Any]:
    """
    Apply a color scheme to a pattern.
    
    Args:
        pattern: The pattern to color
        color_scheme: Name of the color scheme to apply
        alpha: Transparency value (0-1)
        
    Returns:
        Dictionary with the pattern and color information
    """
    scheme = get_color_scheme(color_scheme)
    colors = scheme["colors"]
    
    # Create a result dictionary
    result = {
        "pattern": pattern,
        "colors": colors,
        "background": scheme["background"],
        "edge_color": scheme["edge_color"],
        "point_color": scheme["point_color"],
        "alpha": alpha
    }
    
    return result

def get_color_for_index(
    index: int,
    color_scheme: str = "golden",
    num_items: Optional[int] = None
) -> str:
    """
    Get a color for a specific index based on a color scheme.
    
    Args:
        index: Index to get color for
        color_scheme: Name of the color scheme
        num_items: Total number of items (used for gradient calculation)
        
    Returns:
        Hex color string
    """
    scheme = get_color_scheme(color_scheme)
    colors = scheme["colors"]
    
    if num_items is None or num_items <= len(colors):
        # Use colors directly if we have enough
        return colors[index % len(colors)]
    else:
        # Create a gradient with the exact number of colors needed
        if color_scheme == "rainbow":
            gradient = create_rainbow_gradient(num_items)
        elif color_scheme == "golden":
            gradient = create_golden_gradient(num_items)
        else:
            gradient = create_custom_gradient(colors, num_items)
        
        return gradient[index % len(gradient)]

def get_colormap(color_scheme: str) -> str:
    """
    Get the matplotlib colormap name for a color scheme.
    
    Args:
        color_scheme: Name of the color scheme
        
    Returns:
        Name of the matplotlib colormap
    """
    scheme = get_color_scheme(color_scheme)
    return scheme["cmap"]

def create_custom_colormap(
    colors: List[ColorType],
    name: str = "custom_cmap"
) -> mcolors.LinearSegmentedColormap:
    """
    Create a custom matplotlib colormap from a list of colors.
    
    Args:
        colors: List of colors
        name: Name for the colormap
        
    Returns:
        Matplotlib colormap
    """
    # Convert colors to RGB if they're strings
    rgb_colors = []
    for color in colors:
        if isinstance(color, str):
            rgb_colors.append(mcolors.to_rgb(color))
        else:
            rgb_colors.append(color[:3])  # Take only RGB components
    
    # Create and register the colormap
    cmap = mcolors.LinearSegmentedColormap.from_list(name, rgb_colors)
    plt.register_cmap(cmap=cmap)
    
    return cmap

def adjust_color_brightness(
    color: ColorType,
    factor: float
) -> str:
    """
    Adjust the brightness of a color.
    
    Args:
        color: Color to adjust
        factor: Brightness factor (>1 for brighter, <1 for darker)
        
    Returns:
        Adjusted color as hex string
    """
    # Convert to RGB if it's a string
    if isinstance(color, str):
        rgb = mcolors.to_rgb(color)
    else:
        rgb = color[:3]  # Take only RGB components
    
    # Convert to HSV, adjust brightness (V), convert back to RGB
    h, s, v = colorsys.rgb_to_hsv(*rgb)
    v = max(0, min(1, v * factor))  # Ensure v stays in [0, 1]
    r, g, b = colorsys.hsv_to_rgb(h, s, v)
    
    return mcolors.to_hex((r, g, b))

def get_complementary_color(color: ColorType) -> str:
    """
    Get the complementary color (opposite on the color wheel).
    
    Args:
        color: Input color
        
    Returns:
        Complementary color as hex string
    """
    # Convert to RGB if it's a string
    if isinstance(color, str):
        rgb = mcolors.to_rgb(color)
    else:
        rgb = color[:3]  # Take only RGB components
    
    # Convert to HSV, shift hue by 0.5 (180 degrees), convert back to RGB
    h, s, v = colorsys.rgb_to_hsv(*rgb)
    h = (h + 0.5) % 1.0
    r, g, b = colorsys.hsv_to_rgb(h, s, v)
    
    return mcolors.to_hex((r, g, b))
