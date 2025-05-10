"""
Sacred Geometry Educational Information Module

This module provides historical, cultural, and mathematical context for
sacred geometry patterns and shapes. It includes information about the
significance of various patterns across different cultures and traditions.
"""
from typing import Dict, List, Any, Optional, Union, Tuple

# Dictionary of pattern information
PATTERN_INFO: Dict[str, Dict[str, Any]] = {
    "Flower of Life": {
        "summary": "The Flower of Life is one of the most ancient sacred geometry symbols, "
                  "consisting of overlapping circles arranged in a hexagonal pattern. It is "
                  "considered to contain the patterns of creation and the fundamental forms of space and time.",
        "history": "The oldest known examples date back to ancient Assyria around 645 BCE. "
                  "It appears in ancient Egyptian temples, including the Temple of Osiris at Abydos. "
                  "The symbol has been found across cultures worldwide, including in China, Japan, India, "
                  "and throughout the Middle East and Europe.",
        "significance": "The Flower of Life is believed to contain the patterns of creation and "
                       "is considered a visual expression of the connections of life that run through all sentient beings. "
                       "It is said to contain the blueprint of the universe, showing how all life emerges from one source.",
        "mathematics": "The pattern is formed by placing circles of the same size so that each circle's center "
                      "is on the circumference of six surrounding circles. This creates the perfect sixfold symmetry "
                      "seen throughout nature, from snowflakes to the arrangement of petals in certain flowers.",
        "derived_patterns": ["Seed of Life", "Fruit of Life", "Tree of Life", "Metatron's Cube"],
        "cultural_connections": {
            "Egyptian": "Found in the Temple of Osiris at Abydos, dating back thousands of years.",
            "Chinese": "Similar patterns appear in traditional Chinese art and architecture.",
            "European": "Leonardo da Vinci studied the Flower of Life and its mathematical properties.",
            "Modern": "Used in contemporary spiritual practices and sacred geometry art."
        },
        "related_concepts": ["Golden Ratio", "Vesica Piscis", "Sacred Geometry", "Platonic Solids"]
    },
    
    "Seed of Life": {
        "summary": "The Seed of Life is formed by seven circles of the same diameter. Six circles are placed "
                  "around a central circle, with each circle's center on the circumference of the central circle.",
        "history": "The Seed of Life is one of the earliest patterns derived from the Flower of Life. "
                  "It has been found in various ancient cultures and is considered a fundamental pattern of creation.",
        "significance": "The Seed of Life represents the seven days of creation in many traditions. "
                       "It symbolizes the beginning of all things and the fundamental patterns of molecular, cellular, "
                       "and universal structure.",
        "mathematics": "The Seed of Life demonstrates perfect sixfold symmetry. The centers of the six outer "
                      "circles form a perfect hexagon. This pattern is the foundation for more complex sacred "
                      "geometry patterns like the Flower of Life.",
        "cultural_connections": {
            "Judeo-Christian": "Associated with the seven days of creation in Genesis.",
            "Islamic": "Similar patterns appear in Islamic geometric art.",
            "Hindu": "Related to the seven chakras in yogic traditions."
        },
        "related_concepts": ["Flower of Life", "Vesica Piscis", "Creation Myths"]
    },
    
    "Metatron's Cube": {
        "summary": "Metatron's Cube is a complex sacred geometry figure derived from the Flower of Life. "
                  "It contains all five Platonic solids and is named after the archangel Metatron.",
        "history": "The concept of Metatron's Cube emerged from Jewish mystical texts, particularly the "
                  "Kabbalistic tradition. The archangel Metatron appears in Jewish apocryphal texts and is "
                  "considered the scribe of God and keeper of celestial secrets.",
        "significance": "Metatron's Cube is believed to contain all the geometric patterns that exist in the universe. "
                       "It is considered a map of creation and a powerful symbol for meditation and protection. "
                       "The figure is said to represent the work of the archangel Metatron, who watches over the flow "
                       "of energy in creation.",
        "mathematics": "When lines are drawn connecting the centers of the 13 circles in the Fruit of Life pattern, "
                      "Metatron's Cube is formed. This structure contains the projections of all five Platonic solids: "
                      "the tetrahedron, hexahedron (cube), octahedron, dodecahedron, and icosahedron.",
        "cultural_connections": {
            "Kabbalistic": "Associated with the archangel Metatron in Jewish mysticism.",
            "Hermetic": "Used in alchemical and hermetic traditions.",
            "New Age": "Popular in modern spiritual and metaphysical practices."
        },
        "related_concepts": ["Platonic Solids", "Sacred Geometry", "Flower of Life", "Kabbalah"]
    },
    
    "Vesica Piscis": {
        "summary": "The Vesica Piscis is formed by the intersection of two circles of the same radius, "
                  "where the center of each circle lies on the circumference of the other.",
        "history": "The Vesica Piscis is one of the oldest and most fundamental sacred geometry symbols. "
                  "It appears in ancient art and architecture across many cultures, from Egypt to Celtic Europe.",
        "significance": "The Vesica Piscis symbolizes the union of opposites, the intersection of the divine and "
                       "human realms, and the creation of life. In Christian symbolism, it became associated with "
                       "Christ, and the fish symbol (ichthys) is derived from its shape.",
        "mathematics": "The ratio of the height to the width of the Vesica Piscis is approximately 1.73:1, which is "
                      "the square root of 3. This proportion was considered sacred and was used in the design of "
                      "Gothic cathedrals. The Vesica Piscis also generates the equilateral triangle when lines are "
                      "drawn connecting the centers of the two circles with the intersection points.",
        "cultural_connections": {
            "Christian": "The fish symbol (ichthys) and mandorla (almond-shaped aura) in Christian art.",
            "Egyptian": "Found in the proportions of sacred buildings and art.",
            "Celtic": "Appears in Celtic knots and artwork."
        },
        "related_concepts": ["Sacred Proportions", "Flower of Life", "Trinity"]
    },
    
    "Fibonacci Spiral": {
        "summary": "The Fibonacci Spiral is a logarithmic spiral created by drawing arcs connecting the opposite "
                  "corners of squares in the Fibonacci tiling, where each square has a side length of a Fibonacci number.",
        "history": "The Fibonacci sequence was first described by Indian mathematicians as early as 200 BCE, but "
                  "was introduced to Western mathematics by Leonardo of Pisa (Fibonacci) in his book Liber Abaci (1202).",
        "significance": "The Fibonacci Spiral is considered a mathematical expression of the golden ratio, which "
                       "appears throughout nature. It represents growth, evolution, and the unfolding of life. "
                       "Many see it as evidence of divine design in nature.",
        "mathematics": "The Fibonacci sequence (0, 1, 1, 2, 3, 5, 8, 13, 21, 34, ...) is formed by adding the two "
                      "previous numbers. As the sequence progresses, the ratio between consecutive numbers approaches "
                      "the golden ratio (approximately 1.618). The Fibonacci Spiral approximates the golden spiral, "
                      "which grows by a factor of the golden ratio with each quarter turn.",
        "natural_examples": [
            "Nautilus shells", "Hurricane formations", "Galaxy spirals",
            "Pinecones", "Sunflower seed arrangements", "Pineapples"
        ],
        "cultural_connections": {
            "Ancient Greek": "Related to the golden ratio, studied by Greek mathematicians.",
            "Renaissance": "Used in art and architecture for balanced compositions.",
            "Modern Science": "Observed in phyllotaxis (the arrangement of leaves on plant stems)."
        },
        "related_concepts": ["Golden Ratio", "Logarithmic Spiral", "Phyllotaxis", "Divine Proportion"]
    },
    
    "Golden Rectangle": {
        "summary": "A Golden Rectangle is a rectangle whose sides are in the golden ratio (approximately 1:1.618).",
        "history": "The concept of the Golden Rectangle dates back to ancient Greece, where it was used in "
                  "architecture and art. It was particularly important during the Renaissance when artists and "
                  "architects like Leonardo da Vinci used it extensively.",
        "significance": "The Golden Rectangle is considered the most visually pleasing rectangle proportion. "
                       "It represents perfect harmony and balance and is believed to connect mathematics with "
                       "aesthetic beauty.",
        "mathematics": "If a square is removed from a Golden Rectangle, the remaining rectangle is also a Golden "
                      "Rectangle. This property allows for the creation of the Golden Spiral by drawing quarter-circles "
                      "inside each square of a Fibonacci tiling.",
        "cultural_examples": [
            "The Parthenon in Athens",
            "Leonardo da Vinci's paintings",
            "Le Corbusier's Modulor system of architectural proportion",
            "The UN Building in New York"
        ],
        "related_concepts": ["Golden Ratio", "Fibonacci Sequence", "Divine Proportion", "Sacred Geometry"]
    },
    
    "Platonic Solids": {
        "summary": "The Platonic solids are the five regular polyhedra: tetrahedron, cube, octahedron, "
                  "dodecahedron, and icosahedron. They are characterized by faces that are congruent regular polygons, "
                  "with the same number of faces meeting at each vertex.",
        "history": "Named after the ancient Greek philosopher Plato, who theorized in his dialogue Timaeus (c. 360 BCE) "
                  "that these five solids were the fundamental building blocks of the universe. However, these shapes "
                  "were likely known to the Pythagoreans before Plato.",
        "significance": "In Plato's cosmology, each solid was associated with one of the classical elements: "
                       "tetrahedron (fire), cube (earth), octahedron (air), icosahedron (water), and dodecahedron (ether/universe). "
                       "They were considered the geometric patterns underlying physical creation.",
        "mathematics": "The Platonic solids are the only regular polyhedra possible in three-dimensional space. "
                      "They possess the highest degree of symmetry of any polyhedra and are dual to each other "
                      "(except the tetrahedron, which is self-dual).",
        "cultural_connections": {
            "Greek": "Associated with the classical elements and cosmic order.",
            "Renaissance": "Studied by Kepler in relation to planetary orbits.",
            "Modern": "Used in molecular structures, viral shapes, and crystallography."
        },
        "individual_solids": {
            "Tetrahedron": {
                "faces": "4 equilateral triangles",
                "element": "Fire",
                "symbolism": "Stability, foundation, manifestation"
            },
            "Cube (Hexahedron)": {
                "faces": "6 squares",
                "element": "Earth",
                "symbolism": "Grounding, structure, material world"
            },
            "Octahedron": {
                "faces": "8 equilateral triangles",
                "element": "Air",
                "symbolism": "Thought, concept, intellect"
            },
            "Dodecahedron": {
                "faces": "12 regular pentagons",
                "element": "Ether/Universe",
                "symbolism": "Cosmic consciousness, higher dimensions"
            },
            "Icosahedron": {
                "faces": "20 equilateral triangles",
                "element": "Water",
                "symbolism": "Flow, emotion, adaptability"
            }
        },
        "related_concepts": ["Sacred Geometry", "Metatron's Cube", "Classical Elements", "Duality"]
    },
    
    "Merkaba": {
        "summary": "The Merkaba (or Merkabah) is a three-dimensional Star of David, formed by two interlocking "
                  "tetrahedra. One tetrahedron points upward, representing masculine energy and spiritual ascension, "
                  "while the other points downward, representing feminine energy and grounding.",
        "history": "The term 'Merkabah' comes from ancient Hebrew, meaning 'chariot' or 'vehicle', and refers to "
                  "the divine light vehicle used by ascended masters to connect with higher realms. It appears in "
                  "the vision of the prophet Ezekiel and in various mystical Jewish texts.",
        "significance": "The Merkaba is considered a powerful energy field that can be activated around the human body "
                       "through meditation and specific breathing techniques. It is believed to facilitate spiritual "
                       "ascension, protection, and interdimensional travel of consciousness.",
        "mathematics": "The Merkaba demonstrates perfect geometric balance and harmony. The two interlocking "
                      "tetrahedra create a stellated octahedron, with 8 points, 12 edges, and 8 faces.",
        "cultural_connections": {
            "Jewish": "Appears in Kabbalistic and mystical Jewish traditions.",
            "Egyptian": "Similar concepts appear in ancient Egyptian spirituality.",
            "New Age": "Central to many modern spiritual practices and meditation techniques."
        },
        "related_concepts": ["Star Tetrahedron", "Sacred Geometry", "Energy Fields", "Spiritual Ascension"]
    }
}

# Dictionary of cultural traditions and their relationship to sacred geometry
CULTURAL_TRADITIONS: Dict[str, Dict[str, Any]] = {
    "Ancient Egyptian": {
        "summary": "Ancient Egyptian civilization incorporated sacred geometry principles in their architecture, "
                  "art, and religious symbolism.",
        "key_patterns": ["Flower of Life", "Vesica Piscis", "Golden Ratio"],
        "examples": [
            "The Flower of Life at the Temple of Osiris in Abydos",
            "The proportions of the Great Pyramid of Giza",
            "The Eye of Horus symbol"
        ],
        "significance": "Sacred geometry was integral to Egyptian cosmology and their understanding of the "
                       "afterlife. Geometric patterns were believed to contain divine energy and were used in "
                       "temple design to create sacred spaces."
    },
    
    "Greek": {
        "summary": "Ancient Greek philosophers and mathematicians formalized many sacred geometry concepts, "
                  "particularly through the work of Pythagoras, Plato, and Euclid.",
        "key_patterns": ["Platonic Solids", "Golden Ratio", "Perfect Proportions"],
        "examples": [
            "The Parthenon's proportions based on the Golden Ratio",
            "Plato's association of the five regular polyhedra with the classical elements",
            "Pythagoras' work on harmonics and musical ratios"
        ],
        "significance": "The Greeks saw geometry as the link between the physical and divine realms. They believed "
                       "that geometric forms revealed the underlying mathematical harmony of the universe."
    },
    
    "Islamic": {
        "summary": "Islamic art and architecture feature complex geometric patterns that reflect the infinite "
                  "nature of Allah. The prohibition of representational art in religious contexts led to the "
                  "development of sophisticated geometric designs.",
        "key_patterns": ["Sixfold Symmetry", "Star Patterns", "Tessellations"],
        "examples": [
            "The intricate tile work in the Alhambra Palace in Spain",
            "Geometric patterns in mosque architecture",
            "The muqarnas (honeycomb vaulting) in Islamic architecture"
        ],
        "significance": "Islamic geometric patterns symbolize the infinite nature of Allah and the order of the "
                       "universe. The repetition and complexity of these patterns are meant to inspire contemplation "
                       "of divine infinity."
    },
    
    "Hindu": {
        "summary": "Hindu traditions incorporate sacred geometry in temple architecture, yantra designs, and "
                  "mandalas used for meditation and spiritual practice.",
        "key_patterns": ["Sri Yantra", "Mandalas", "Temple Proportions"],
        "examples": [
            "The Sri Yantra, composed of nine interlocking triangles",
            "Hindu temple architecture based on the Vastu Purusha Mandala",
            "The geometric proportions of the human body in yoga postures"
        ],
        "significance": "Sacred geometry in Hinduism represents the cosmos and divine creation. Yantras and "
                       "mandalas are used as tools for meditation and to invoke specific deities or energies."
    },
    
    "Buddhist": {
        "summary": "Buddhist traditions use geometric mandalas as meditation tools and incorporate sacred "
                  "proportions in stupas and temple architecture.",
        "key_patterns": ["Mandalas", "Dharma Wheel", "Stupa Design"],
        "examples": [
            "The Kalachakra Mandala with its complex geometric structure",
            "The eight-spoked Dharma Wheel",
            "The proportions of Buddhist stupas representing the Buddha's body"
        ],
        "significance": "In Buddhism, geometric patterns like mandalas represent the cosmos and are used as aids "
                       "for meditation and spiritual development. They serve as maps of the universe and the mind."
    },
    
    "Celtic": {
        "summary": "Celtic art and symbolism feature intricate knotwork, spirals, and geometric patterns that "
                  "reflect their understanding of the interconnectedness of all things.",
        "key_patterns": ["Celtic Knots", "Triskele (Triple Spiral)", "Celtic Cross"],
        "examples": [
            "The Book of Kells with its elaborate geometric illuminations",
            "Stone carvings featuring spirals and knotwork",
            "The geometric proportions of stone circles like Stonehenge"
        ],
        "significance": "Celtic geometric patterns symbolize eternity, interconnectedness, and the cycles of "
                       "nature. The endless knotwork represents the continuous flow of life, death, and rebirth."
    },
    
    "Renaissance": {
        "summary": "During the Renaissance, sacred geometry experienced a revival through the work of artists, "
                  "architects, and scientists who sought to understand divine proportion.",
        "key_patterns": ["Golden Ratio", "Vitruvian Man", "Perspective"],
        "examples": [
            "Leonardo da Vinci's Vitruvian Man",
            "The proportions of Renaissance cathedrals",
            "Botticelli's use of sacred geometry in compositions"
        ],
        "significance": "Renaissance thinkers saw sacred geometry as evidence of divine design and used it to "
                       "create harmonious art and architecture that reflected the perfection of God's creation."
    },
    
    "Modern/New Age": {
        "summary": "Contemporary spiritual movements have revived interest in sacred geometry, incorporating it "
                  "into healing practices, meditation, and understanding consciousness.",
        "key_patterns": ["Flower of Life", "Merkaba", "Crop Circles"],
        "examples": [
            "Crystal grids arranged in sacred geometric patterns",
            "Merkaba meditation practices",
            "Sacred geometry in modern architecture and design"
        ],
        "significance": "In modern spiritual contexts, sacred geometry is seen as a tool for personal "
                       "transformation, healing, and expanding consciousness. It is often associated with "
                       "energy work and vibrational healing."
    }
}

# Mathematical principles underlying sacred geometry
MATHEMATICAL_PRINCIPLES: Dict[str, Dict[str, Any]] = {
    "Golden Ratio": {
        "summary": "The Golden Ratio (φ or phi, approximately 1.618) is a special mathematical relationship "
                  "where a line is divided so that the ratio of the whole line to the larger segment equals "
                  "the ratio of the larger segment to the smaller segment.",
        "formula": "φ = (1 + √5) / 2 ≈ 1.618033988749895",
        "significance": "The Golden Ratio appears throughout nature and is considered the most aesthetically "
                       "pleasing proportion. It represents perfect harmony and balance.",
        "examples_in_nature": [
            "Spiral arrangement of leaves around a stem (phyllotaxis)",
            "Proportions of the human body",
            "Spiral patterns in shells, hurricanes, and galaxies"
        ],
        "examples_in_art": [
            "The Parthenon",
            "Leonardo da Vinci's paintings",
            "Salvador Dalí's 'The Sacrament of the Last Supper'"
        ]
    },
    
    "Fibonacci Sequence": {
        "summary": "The Fibonacci sequence is a series of numbers where each number is the sum of the two "
                  "preceding ones: 0, 1, 1, 2, 3, 5, 8, 13, 21, 34, ...",
        "formula": "F(n) = F(n-1) + F(n-2), with F(0) = 0 and F(1) = 1",
        "significance": "The Fibonacci sequence is closely related to the Golden Ratio. As the sequence "
                       "progresses, the ratio between consecutive numbers approaches the Golden Ratio.",
        "examples_in_nature": [
            "Number of petals on flowers (often Fibonacci numbers)",
            "Spiral arrangements in pinecones and sunflower seeds",
            "Branching patterns in trees"
        ]
    },
    
    "Symmetry": {
        "summary": "Symmetry is a fundamental principle in sacred geometry, representing balance, harmony, and order.",
        "types": {
            "Reflection": "Mirror symmetry across an axis",
            "Rotation": "Symmetry when rotated around a point",
            "Translation": "Symmetry when shifted in position",
            "Dilation": "Symmetry when scaled up or down"
        },
        "significance": "Symmetry is associated with beauty, perfection, and divine order. It appears in "
                       "natural structures from crystals to living organisms."
    },
    
    "Pi (π)": {
        "summary": "Pi is the ratio of a circle's circumference to its diameter, approximately 3.14159.",
        "formula": "π = C/d, where C is the circumference and d is the diameter",
        "significance": "Pi is a transcendental number that appears in many fundamental equations describing "
                       "natural phenomena. In sacred geometry, the circle represents unity, wholeness, and the divine."
    },
    
    "Squaring the Circle": {
        "summary": "The ancient geometric problem of constructing a square with the same area as a given circle "
                  "using only a compass and straightedge.",
        "significance": "This problem is mathematically impossible to solve exactly (as proven in 1882), but "
                       "it has profound symbolic meaning in sacred geometry. It represents the reconciliation "
                       "of heaven (circle) and earth (square), or spirit and matter."
    },
    
    "Vesica Piscis Proportions": {
        "summary": "The Vesica Piscis generates the square root of 3 proportion, which was considered sacred "
                  "in many traditions.",
        "formula": "The ratio of height to width is √3:1",
        "significance": "This proportion was used extensively in Gothic cathedral design and is related to "
                       "the equilateral triangle, which symbolizes divinity in many traditions."
    }
}

def get_pattern_info(pattern_name: str) -> Optional[Dict[str, Any]]:
    """
    Retrieve information about a specific sacred geometry pattern.
    
    Args:
        pattern_name: Name of the pattern (e.g., "Flower of Life", "Merkaba")
        
    Returns:
        Dictionary containing information about the pattern, or None if not found
    """
    return PATTERN_INFO.get(pattern_name)

def get_cultural_tradition(tradition_name: str) -> Optional[Dict[str, Any]]:
    """
    Retrieve information about a specific cultural tradition's use of sacred geometry.
    
    Args:
        tradition_name: Name of the tradition (e.g., "Ancient Egyptian", "Islamic")
        
    Returns:
        Dictionary containing information about the tradition, or None if not found
    """
    return CULTURAL_TRADITIONS.get(tradition_name)

def get_mathematical_principle(principle_name: str) -> Optional[Dict[str, Any]]:
    """
    Retrieve information about a specific mathematical principle in sacred geometry.
    
    Args:
        principle_name: Name of the principle (e.g., "Golden Ratio", "Fibonacci Sequence")
        
    Returns:
        Dictionary containing information about the principle, or None if not found
    """
    return MATHEMATICAL_PRINCIPLES.get(principle_name)

def get_all_pattern_names() -> List[str]:
    """
    Get a list of all available pattern names.
    
    Returns:
        List of pattern names
    """
    return list(PATTERN_INFO.keys())

def get_all_tradition_names() -> List[str]:
    """
    Get a list of all available cultural tradition names.
    
    Returns:
        List of tradition names
    """
    return list(CULTURAL_TRADITIONS.keys())

def get_all_principle_names() -> List[str]:
    """
    Get a list of all available mathematical principle names.
    
    Returns:
        List of principle names
    """
    return list(MATHEMATICAL_PRINCIPLES.keys())

def search_information(query: str) -> Dict[str, List[Dict[str, Any]]]:
    """
    Search for information across all categories based on a query string.
    
    Args:
        query: Search query string
        
    Returns:
        Dictionary with categories as keys and lists of matching items as values
    """
    query = query.lower()
    results = {
        "patterns": [],
        "traditions": [],
        "principles": []
    }
    
    # Search patterns
    for name, info in PATTERN_INFO.items():
        if query in name.lower() or query in info["summary"].lower():
            results["patterns"].append({"name": name, "info": info})
    
    # Search traditions
    for name, info in CULTURAL_TRADITIONS.items():
        if query in name.lower() or query in info["summary"].lower():
            results["traditions"].append({"name": name, "info": info})
    
    # Search principles
    for name, info in MATHEMATICAL_PRINCIPLES.items():
        if query in name.lower() or query in info["summary"].lower():
            results["principles"].append({"name": name, "info": info})
    
    return results

def get_related_patterns(pattern_name: str) -> List[str]:
    """
    Get a list of related patterns for a given pattern.
    
    Args:
        pattern_name: Name of the pattern
        
    Returns:
        List of related pattern names
    """
    pattern_info = get_pattern_info(pattern_name)
    if not pattern_info or "related_concepts" not in pattern_info:
        return []
    
    # Filter related concepts to only include those that are actual patterns
    return [concept for concept in pattern_info["related_concepts"] 
            if concept in PATTERN_INFO]
