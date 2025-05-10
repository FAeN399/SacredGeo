"""
Esoteric Sacred Geometry GUI Application

A comprehensive graphical user interface for generating and visualizing
sacred geometry patterns, shapes, and animations with an esoteric aesthetic.
"""
import os
import sys
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
import matplotlib.animation as animation
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QTabWidget, QLabel, QComboBox, QSlider, QCheckBox, QPushButton,
    QSpinBox, QDoubleSpinBox, QColorDialog, QFileDialog, QGroupBox,
    QFormLayout, QSplitter, QMessageBox, QRadioButton, QSizePolicy,
    QStatusBar, QToolBar, QAction, QDial
)
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QColor, QIcon

# Import core 2D pattern generators
from sacred_geometry.core.core import (
    create_flower_of_life, create_metatrons_cube, create_vesica_piscis,
    create_fibonacci_spiral, create_regular_polygon, create_golden_rectangle,
    create_seed_of_life, get_golden_ratio
)

# Import fractal pattern generators
from sacred_geometry.fractals.fractals import (
    sierpinski_triangle, koch_snowflake, sacred_spiral, fractal_tree,
    dragon_curve, hilbert_curve
)

# Import 3D shape generators
from sacred_geometry.shapes.shapes import (
    create_tetrahedron, create_cube, create_octahedron,
    create_icosahedron, create_dodecahedron, create_merkaba,
    create_cuboctahedron, create_flower_of_life_3d, create_torus
)

# Import custom compositions
from sacred_geometry.custom.compositions import (
    create_flower_of_life_with_fibonacci, create_sacred_geometry_mandala,
    create_metatrons_cube_with_platonic_projections, create_fractal_tree_with_golden_ratio,
    create_nested_platonic_solids, create_cosmic_torus_with_merkaba,
    create_tree_of_life_template, plot_composition
)

# Import visualization tools
from sacred_geometry.visualization.visualization import (
    plot_2d_pattern, plot_3d_shape
)

# Try to import advanced visualization modules
try:
    from sacred_geometry.visualization.lighting import plot_3d_shape_with_lighting
except ImportError:
    # Define a fallback function if the module is not available
    def plot_3d_shape_with_lighting(shape, ax=None, **kwargs):
        return plot_3d_shape(shape, ax=ax, **kwargs)

# Try to import exporters and utilities
try:
    from sacred_geometry.utils.exporters import (
        export_2d_image, export_svg, export_3d_obj, export_stl,
        export_animation_gif, export_high_resolution_image,
        export_for_3d_printing
    )
except ImportError:
    # Define fallback functions if the module is not available
    def export_2d_image(fig, filename, **kwargs):
        fig.savefig(filename, **kwargs)
        return filename

    def export_svg(pattern, filename, **kwargs):
        # Fallback to PNG if SVG export is not available
        plt.figure()
        for circle in pattern:
            plt.plot(circle[:, 0], circle[:, 1])
        plt.savefig(filename.replace('.svg', '.png'))
        return filename.replace('.svg', '.png')

    def export_3d_obj(shape, filename, **kwargs):
        # Just save a screenshot if OBJ export is not available
        plt.figure()
        plot_3d_shape(shape)
        plt.savefig(filename.replace('.obj', '.png'))
        return filename.replace('.obj', '.png')

    def export_stl(shape, filename, **kwargs):
        # Just save a screenshot if STL export is not available
        plt.figure()
        plot_3d_shape(shape)
        plt.savefig(filename.replace('.stl', '.png'))
        return filename.replace('.stl', '.png')

    def export_high_resolution_image(fig, filename, **kwargs):
        fig.savefig(filename, dpi=300)
        return filename

    def export_for_3d_printing(shape, filename, **kwargs):
        # Just save a screenshot if 3D printing export is not available
        plt.figure()
        plot_3d_shape(shape)
        plt.savefig(filename.replace('.stl', '.png'))
        return filename.replace('.stl', '.png')

# Try to import color schemes
try:
    from sacred_geometry.utils.color_schemes import (
        get_color_scheme, get_material_properties, create_color_gradient
    )
except ImportError:
    # Define fallback functions if the module is not available
    def get_color_scheme(scheme_name):
        # Default color schemes
        schemes = {
            "golden": {
                "colors": ["#FFD700", "#FFC107", "#FF9800", "#FF5722", "#F4511E"],
                "edge_color": "#daa520",
                "point_color": "#ffd700",
                "background": "#1a1a2e",
                "cmap": "YlOrBr"
            },
            "rainbow": {
                "colors": ["#FF0000", "#FF7F00", "#FFFF00", "#00FF00", "#0000FF", "#4B0082", "#9400D3"],
                "edge_color": "#ffffff",
                "point_color": "#ffffff",
                "background": "#1a1a2e",
                "cmap": "rainbow"
            }
        }
        return schemes.get(scheme_name.lower(), schemes["golden"])

    def get_material_properties(material_name):
        # Default material properties
        materials = {
            "matte": {"ambient": 0.3, "diffuse": 0.7, "specular": 0.1, "shininess": 10, "alpha": 1.0},
            "metallic": {"ambient": 0.2, "diffuse": 0.4, "specular": 0.9, "shininess": 100, "alpha": 0.9},
            "glass": {"ambient": 0.1, "diffuse": 0.2, "specular": 0.8, "shininess": 50, "alpha": 0.4},
            "crystal": {"ambient": 0.2, "diffuse": 0.3, "specular": 0.9, "shininess": 80, "alpha": 0.6},
            "energy": {"ambient": 0.5, "diffuse": 0.7, "specular": 0.9, "shininess": 30, "alpha": 0.8}
        }
        return materials.get(material_name.lower(), materials["matte"])

    def create_color_gradient(start_color, end_color, num_colors=10):
        # Simple linear gradient
        import matplotlib.colors as mcolors
        start_rgb = mcolors.to_rgb(start_color)
        end_rgb = mcolors.to_rgb(end_color)

        gradient = []
        for i in range(num_colors):
            r = start_rgb[0] + (end_rgb[0] - start_rgb[0]) * i / (num_colors - 1)
            g = start_rgb[1] + (end_rgb[1] - start_rgb[1]) * i / (num_colors - 1)
            b = start_rgb[2] + (end_rgb[2] - start_rgb[2]) * i / (num_colors - 1)
            gradient.append(mcolors.to_hex((r, g, b)))

        return gradient

# Try to import educational information
try:
    from sacred_geometry.education.information import (
        get_pattern_info, get_all_pattern_names, search_information
    )
except ImportError:
    # Define fallback functions if the module is not available
    def get_pattern_info(pattern_name):
        # Basic information for common patterns
        patterns = {
            "Flower of Life": {
                "summary": "The Flower of Life is one of the most ancient sacred geometry symbols.",
                "history": "The oldest known examples date back to ancient Assyria around 645 BCE.",
                "significance": "The Flower of Life is believed to contain the patterns of creation."
            },
            "Metatron's Cube": {
                "summary": "Metatron's Cube is a complex sacred geometry figure derived from the Flower of Life.",
                "history": "Named after the archangel Metatron, who appears in Jewish mystical texts.",
                "significance": "It contains all five Platonic solids and is considered a map of creation."
            }
        }
        return patterns.get(pattern_name, {"summary": "Information not available."})

    def get_all_pattern_names():
        return ["Flower of Life", "Metatron's Cube", "Vesica Piscis", "Seed of Life"]

    def search_information(query):
        return {"patterns": [], "traditions": [], "principles": []}

# Create output directories if they don't exist
output_dirs = {
    '2d': 'outputs/2d',
    '3d': 'outputs/3d',
    'animations': 'outputs/animations',
    'fractals': 'outputs/fractals',
    'custom': 'outputs/custom'
}

for dir_path in output_dirs.values():
    os.makedirs(dir_path, exist_ok=True)

class MatplotlibCanvas(FigureCanvas):
    """Enhanced Matplotlib canvas for displaying sacred geometry patterns and shapes."""

    def __init__(self, parent=None, width=8, height=8, dpi=100, is_3d=False):
        self.fig = Figure(figsize=(width, height), dpi=dpi)

        # Set dark theme for the figure
        self.fig.patch.set_facecolor('#1a1a2e')  # Match the dark background

        if is_3d:
            self.axes = self.fig.add_subplot(111, projection='3d')
            self.axes.set_facecolor('#1a1a2e')  # Dark background for 3D plots
        else:
            self.axes = self.fig.add_subplot(111)
            self.axes.set_facecolor('#1a1a2e')  # Dark background for 2D plots
            self.axes.set_aspect('equal')

        # Set dark theme for axes
        self.axes.tick_params(axis='x', colors='#c0c0d0')
        self.axes.tick_params(axis='y', colors='#c0c0d0')
        if is_3d:
            self.axes.tick_params(axis='z', colors='#c0c0d0')

        # Set dark theme for spines
        for spine in self.axes.spines.values():
            spine.set_color('#3c3c4f')

        # Set dark theme for labels
        self.axes.xaxis.label.set_color('#c0c0d0')
        self.axes.yaxis.label.set_color('#c0c0d0')
        if is_3d:
            self.axes.zaxis.label.set_color('#c0c0d0')

        # Set dark theme for title
        self.axes.title.set_color('#daa520')  # Golden title

        FigureCanvas.__init__(self, self.fig)
        self.setParent(parent)

        FigureCanvas.setSizePolicy(self,
                                  QSizePolicy.Expanding,
                                  QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)

    def clear_plot(self):
        """Clear the current plot."""
        self.axes.clear()

        # Restore dark theme settings after clearing
        self.axes.set_facecolor('#1a1a2e')
        self.axes.tick_params(axis='x', colors='#c0c0d0')
        self.axes.tick_params(axis='y', colors='#c0c0d0')
        if hasattr(self.axes, 'zaxis'):
            self.axes.tick_params(axis='z', colors='#c0c0d0')

        for spine in self.axes.spines.values():
            spine.set_color('#3c3c4f')

        self.axes.xaxis.label.set_color('#c0c0d0')
        self.axes.yaxis.label.set_color('#c0c0d0')
        if hasattr(self.axes, 'zaxis'):
            self.axes.zaxis.label.set_color('#c0c0d0')

        self.draw()

    def set_3d_axes(self):
        """Set up 3D axes for 3D shapes."""
        self.fig.clear()
        self.axes = self.fig.add_subplot(111, projection='3d')

        # Set dark theme for 3D axes
        self.axes.set_facecolor('#1a1a2e')
        self.axes.tick_params(axis='x', colors='#c0c0d0')
        self.axes.tick_params(axis='y', colors='#c0c0d0')
        self.axes.tick_params(axis='z', colors='#c0c0d0')
        self.axes.xaxis.label.set_color('#c0c0d0')
        self.axes.yaxis.label.set_color('#c0c0d0')
        self.axes.zaxis.label.set_color('#c0c0d0')
        self.axes.title.set_color('#daa520')  # Golden title

        self.draw()

    def set_2d_axes(self):
        """Set up 2D axes for 2D patterns."""
        self.fig.clear()
        self.axes = self.fig.add_subplot(111)

        # Set dark theme for 2D axes
        self.axes.set_facecolor('#1a1a2e')
        self.axes.set_aspect('equal')
        self.axes.tick_params(axis='x', colors='#c0c0d0')
        self.axes.tick_params(axis='y', colors='#c0c0d0')

        for spine in self.axes.spines.values():
            spine.set_color('#3c3c4f')

        self.axes.xaxis.label.set_color('#c0c0d0')
        self.axes.yaxis.label.set_color('#c0c0d0')
        self.axes.title.set_color('#daa520')  # Golden title

        self.draw()

class EnhancedNavigationToolbar(NavigationToolbar):
    """Custom navigation toolbar with dark theme styling."""

    def __init__(self, canvas, parent):
        super().__init__(canvas, parent)

        # Set dark theme for the toolbar
        self.setStyleSheet("""
            background-color: #252538;
            border: none;
            padding: 2px;
        """)

        # Add custom actions
        self.addSeparator()

        # Add 3D rotation controls if it's a 3D plot
        if hasattr(canvas.axes, 'zaxis'):
            self.view_front_action = QAction("Front View", self)
            self.view_front_action.triggered.connect(lambda: self.set_view('front'))
            self.addAction(self.view_front_action)

            self.view_top_action = QAction("Top View", self)
            self.view_top_action.triggered.connect(lambda: self.set_view('top'))
            self.addAction(self.view_top_action)

            self.view_side_action = QAction("Side View", self)
            self.view_side_action.triggered.connect(lambda: self.set_view('side'))
            self.addAction(self.view_side_action)

            self.view_isometric_action = QAction("Isometric View", self)
            self.view_isometric_action.triggered.connect(lambda: self.set_view('isometric'))
            self.addAction(self.view_isometric_action)

    def set_view(self, view_type):
        """Set the view angle for 3D plots."""
        if view_type == 'front':
            self.canvas.axes.view_init(elev=0, azim=0)
        elif view_type == 'top':
            self.canvas.axes.view_init(elev=90, azim=0)
        elif view_type == 'side':
            self.canvas.axes.view_init(elev=0, azim=90)
        elif view_type == 'isometric':
            self.canvas.axes.view_init(elev=30, azim=45)

        self.canvas.draw()

class SacredGeometryGUI(QMainWindow):
    """Main window for the Esoteric Sacred Geometry GUI application."""

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Sacred Geometry Explorer")
        self.setGeometry(100, 100, 1280, 800)

        # Load the dark esoteric theme stylesheet
        self.load_stylesheet()

        # Create the main widget and layout
        self.main_widget = QWidget()
        self.setCentralWidget(self.main_widget)

        # Create a splitter for the main layout
        self.splitter = QSplitter(Qt.Horizontal)

        # Create the control panel
        self.control_widget = QTabWidget()
        self.setup_control_panel()

        # Create the visualization panel
        self.viz_panel = QWidget()
        self.setup_viz_panel()

        # Add widgets to splitter
        self.splitter.addWidget(self.control_widget)
        self.splitter.addWidget(self.viz_panel)
        self.splitter.setSizes([400, 880])

        # Set up the main layout
        main_layout = QVBoxLayout()
        main_layout.addWidget(self.splitter)
        self.main_widget.setLayout(main_layout)

        # Create status bar
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage("Ready")

        # Create toolbar
        self.toolbar = QToolBar("Main Toolbar")
        self.addToolBar(self.toolbar)

        # Add toolbar actions
        self.setup_toolbar()

        # Initialize the current category and pattern
        self.current_category = "2D Patterns"
        self.current_pattern = "Flower of Life"

        # Setup 3D rotation timer for continuous rotation
        self.rotation_timer = QTimer(self)
        self.rotation_timer.timeout.connect(self.rotate_3d_shape)
        self.rotation_angle = 0
        self.rotation_speed = 2  # degrees per update

        # Generate initial pattern
        self.generate_output()

    def load_stylesheet(self):
        """Load the dark esoteric theme stylesheet."""
        try:
            with open("esoteric_style.qss", "r") as f:
                style = f.read()
                self.setStyleSheet(style)
        except FileNotFoundError:
            print("Style sheet file not found. Using default style.")

    def setup_toolbar(self):
        """Set up the main toolbar."""
        # Save action
        save_action = QAction("Save", self)
        save_action.triggered.connect(self.save_output)
        self.toolbar.addAction(save_action)

        # Export action
        export_action = QAction("Export 3D", self)
        export_action.triggered.connect(self.export_output)
        self.toolbar.addAction(export_action)

        self.toolbar.addSeparator()

        # Info action
        info_action = QAction("Pattern Info", self)
        info_action.triggered.connect(self.show_pattern_info)
        self.toolbar.addAction(info_action)

        # Help action
        help_action = QAction("Help", self)
        help_action.triggered.connect(self.show_help)
        self.toolbar.addAction(help_action)

    def setup_control_panel(self):
        """Set up the control panel with tabs for different categories."""
        # Create tabs for different categories
        self.tab_2d = QWidget()
        self.tab_3d = QWidget()
        self.tab_fractals = QWidget()
        self.tab_animations = QWidget()
        self.tab_compositions = QWidget()

        # Add tabs to the control panel
        self.control_widget.addTab(self.tab_2d, "2D Patterns")
        self.control_widget.addTab(self.tab_3d, "3D Shapes")
        self.control_widget.addTab(self.tab_fractals, "Fractals")
        self.control_widget.addTab(self.tab_animations, "Animations")
        self.control_widget.addTab(self.tab_compositions, "Compositions")

        # Connect tab change signal
        self.control_widget.currentChanged.connect(self.on_tab_changed)

        # Set up each tab
        self.setup_2d_tab()
        self.setup_3d_tab()
        self.setup_fractals_tab()
        self.setup_animations_tab()
        self.setup_compositions_tab()

    def setup_viz_panel(self):
        """Set up the visualization panel with matplotlib canvas."""
        viz_layout = QVBoxLayout()

        # Create title label
        self.title_label = QLabel("Sacred Geometry Explorer")
        self.title_label.setObjectName("titleLabel")
        self.title_label.setAlignment(Qt.AlignCenter)
        viz_layout.addWidget(self.title_label)

        # Create matplotlib canvas
        self.canvas = MatplotlibCanvas(self.viz_panel, width=8, height=8)
        self.toolbar = EnhancedNavigationToolbar(self.canvas, self.viz_panel)

        # Create control buttons layout
        control_layout = QHBoxLayout()

        # Create save button
        self.save_button = QPushButton("Save Output")
        self.save_button.clicked.connect(self.save_output)
        control_layout.addWidget(self.save_button)

        # Create export button
        self.export_button = QPushButton("Export 3D Model")
        self.export_button.clicked.connect(self.export_output)
        control_layout.addWidget(self.export_button)

        # Create rotation controls for 3D
        self.rotation_group = QGroupBox("3D Rotation")
        rotation_layout = QHBoxLayout()

        self.rotation_checkbox = QCheckBox("Auto-Rotate")
        self.rotation_checkbox.toggled.connect(self.toggle_rotation)
        rotation_layout.addWidget(self.rotation_checkbox)

        self.rotation_speed_dial = QDial()
        self.rotation_speed_dial.setMinimum(1)
        self.rotation_speed_dial.setMaximum(10)
        self.rotation_speed_dial.setValue(2)
        self.rotation_speed_dial.valueChanged.connect(self.set_rotation_speed)
        rotation_layout.addWidget(self.rotation_speed_dial)

        self.rotation_group.setLayout(rotation_layout)
        control_layout.addWidget(self.rotation_group)

        # Add widgets to layout
        viz_layout.addWidget(self.toolbar)
        viz_layout.addWidget(self.canvas)
        viz_layout.addLayout(control_layout)

        self.viz_panel.setLayout(viz_layout)

    def setup_2d_tab(self):
        """Set up the 2D patterns tab."""
        layout = QVBoxLayout()

        # Add title
        title_label = QLabel("2D Sacred Geometry Patterns")
        title_label.setObjectName("titleLabel")
        title_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(title_label)

        # Pattern selection
        pattern_group = QGroupBox("Pattern Selection")
        pattern_layout = QFormLayout()

        self.pattern_2d_combo = QComboBox()
        self.pattern_2d_combo.addItems([
            "Flower of Life", "Seed of Life", "Metatron's Cube",
            "Vesica Piscis", "Fibonacci Spiral", "Regular Polygon",
            "Golden Rectangle"
        ])
        self.pattern_2d_combo.currentTextChanged.connect(self.on_2d_pattern_changed)
        pattern_layout.addRow("Pattern:", self.pattern_2d_combo)

        pattern_group.setLayout(pattern_layout)
        layout.addWidget(pattern_group)

        # Pattern parameters
        self.params_2d_group = QGroupBox("Pattern Parameters")
        self.params_2d_layout = QFormLayout()

        # Common parameters
        self.radius_2d_spin = QDoubleSpinBox()
        self.radius_2d_spin.setRange(0.1, 10.0)
        self.radius_2d_spin.setValue(1.0)
        self.radius_2d_spin.setSingleStep(0.1)
        self.params_2d_layout.addRow("Radius:", self.radius_2d_spin)

        # Add radius slider
        self.radius_2d_slider = QSlider(Qt.Horizontal)
        self.radius_2d_slider.setRange(1, 100)
        self.radius_2d_slider.setValue(10)
        self.radius_2d_slider.valueChanged.connect(lambda v: self.radius_2d_spin.setValue(v/10))
        self.radius_2d_spin.valueChanged.connect(lambda v: self.radius_2d_slider.setValue(int(v*10)))
        self.params_2d_layout.addRow("", self.radius_2d_slider)

        # Flower of Life specific parameters
        self.layers_spin = QSpinBox()
        self.layers_spin.setRange(1, 10)
        self.layers_spin.setValue(3)
        self.params_2d_layout.addRow("Layers:", self.layers_spin)

        # Regular Polygon specific parameters
        self.sides_spin = QSpinBox()
        self.sides_spin.setRange(3, 20)
        self.sides_spin.setValue(6)
        self.sides_spin.hide()  # Hide initially
        self.params_2d_layout.addRow("Sides:", self.sides_spin)

        self.rotation_2d_spin = QDoubleSpinBox()
        self.rotation_2d_spin.setRange(0, 2*np.pi)
        self.rotation_2d_spin.setValue(0)
        self.rotation_2d_spin.setSingleStep(np.pi/12)
        self.rotation_2d_spin.hide()  # Hide initially
        self.params_2d_layout.addRow("Rotation:", self.rotation_2d_spin)

        # Visualization parameters
        self.color_scheme_combo = QComboBox()
        self.color_scheme_combo.addItems(["rainbow", "golden", "monochrome", "custom"])
        self.params_2d_layout.addRow("Color Scheme:", self.color_scheme_combo)

        self.show_points_check = QCheckBox()
        self.show_points_check.setChecked(False)
        self.params_2d_layout.addRow("Show Points:", self.show_points_check)

        self.params_2d_group.setLayout(self.params_2d_layout)
        layout.addWidget(self.params_2d_group)

        # Generate button
        self.generate_2d_button = QPushButton("Generate Pattern")
        self.generate_2d_button.setObjectName("generateButton")
        self.generate_2d_button.clicked.connect(self.generate_output)
        layout.addWidget(self.generate_2d_button)

        # Add stretch to push everything to the top
        layout.addStretch()

        self.tab_2d.setLayout(layout)

    def setup_3d_tab(self):
        """Set up the 3D shapes tab with enhanced controls."""
        layout = QVBoxLayout()

        # Add title
        title_label = QLabel("3D Sacred Geometry Shapes")
        title_label.setObjectName("titleLabel")
        title_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(title_label)

        # Shape selection
        shape_group = QGroupBox("Shape Selection")
        shape_layout = QFormLayout()

        self.shape_3d_combo = QComboBox()
        self.shape_3d_combo.addItems([
            "Tetrahedron", "Cube", "Octahedron", "Icosahedron", "Dodecahedron",
            "Merkaba", "Cuboctahedron (Vector Equilibrium)", "Torus", "Flower of Life 3D"
        ])
        self.shape_3d_combo.currentTextChanged.connect(self.on_3d_shape_changed)
        shape_layout.addRow("Shape:", self.shape_3d_combo)

        shape_group.setLayout(shape_layout)
        layout.addWidget(shape_group)

        # Shape parameters
        self.params_3d_group = QGroupBox("Shape Parameters")
        self.params_3d_layout = QFormLayout()

        # Common parameters
        self.radius_3d_spin = QDoubleSpinBox()
        self.radius_3d_spin.setRange(0.1, 10.0)
        self.radius_3d_spin.setValue(1.0)
        self.radius_3d_spin.setSingleStep(0.1)
        self.params_3d_layout.addRow("Radius:", self.radius_3d_spin)

        # Add radius slider
        self.radius_3d_slider = QSlider(Qt.Horizontal)
        self.radius_3d_slider.setRange(1, 100)
        self.radius_3d_slider.setValue(10)
        self.radius_3d_slider.valueChanged.connect(lambda v: self.radius_3d_spin.setValue(v/10))
        self.radius_3d_spin.valueChanged.connect(lambda v: self.radius_3d_slider.setValue(int(v*10)))
        self.params_3d_layout.addRow("", self.radius_3d_slider)

        # Merkaba specific parameters
        self.rotation_3d_spin = QDoubleSpinBox()
        self.rotation_3d_spin.setRange(0, 2*np.pi)
        self.rotation_3d_spin.setValue(np.pi/4)
        self.rotation_3d_spin.setSingleStep(np.pi/12)
        self.rotation_3d_spin.hide()  # Hide initially
        self.params_3d_layout.addRow("Rotation:", self.rotation_3d_spin)

        # Torus specific parameters
        self.major_radius_spin = QDoubleSpinBox()
        self.major_radius_spin.setRange(0.5, 5.0)
        self.major_radius_spin.setValue(2.0)
        self.major_radius_spin.setSingleStep(0.1)
        self.major_radius_spin.hide()  # Hide initially
        self.params_3d_layout.addRow("Major Radius:", self.major_radius_spin)

        self.minor_radius_spin = QDoubleSpinBox()
        self.minor_radius_spin.setRange(0.1, 2.0)
        self.minor_radius_spin.setValue(0.5)
        self.minor_radius_spin.setSingleStep(0.1)
        self.minor_radius_spin.hide()  # Hide initially
        self.params_3d_layout.addRow("Minor Radius:", self.minor_radius_spin)

        # Flower of Life 3D specific parameters
        self.layers_3d_spin = QSpinBox()
        self.layers_3d_spin.setRange(1, 5)
        self.layers_3d_spin.setValue(2)
        self.layers_3d_spin.hide()  # Hide initially
        self.params_3d_layout.addRow("Layers:", self.layers_3d_spin)

        # Visualization parameters
        viz_group = QGroupBox("Visualization")
        viz_layout = QFormLayout()

        self.color_scheme_3d_combo = QComboBox()
        self.color_scheme_3d_combo.addItems([
            "golden", "rainbow", "monochrome", "fire", "ice", "earth",
            "chakra", "cosmic", "ethereal", "crystal", "energy"
        ])
        viz_layout.addRow("Color Scheme:", self.color_scheme_3d_combo)

        self.alpha_3d_spin = QDoubleSpinBox()
        self.alpha_3d_spin.setRange(0.1, 1.0)
        self.alpha_3d_spin.setValue(0.7)
        self.alpha_3d_spin.setSingleStep(0.1)
        viz_layout.addRow("Transparency:", self.alpha_3d_spin)

        # Add alpha slider
        self.alpha_3d_slider = QSlider(Qt.Horizontal)
        self.alpha_3d_slider.setRange(1, 10)
        self.alpha_3d_slider.setValue(7)
        self.alpha_3d_slider.valueChanged.connect(lambda v: self.alpha_3d_spin.setValue(v/10))
        self.alpha_3d_spin.valueChanged.connect(lambda v: self.alpha_3d_slider.setValue(int(v*10)))
        viz_layout.addRow("", self.alpha_3d_slider)

        self.show_edges_check = QCheckBox()
        self.show_edges_check.setChecked(True)
        viz_layout.addRow("Show Edges:", self.show_edges_check)

        self.show_vertices_check = QCheckBox()
        self.show_vertices_check.setChecked(True)
        viz_layout.addRow("Show Vertices:", self.show_vertices_check)

        # Material selection
        self.material_combo = QComboBox()
        self.material_combo.addItems(["matte", "metallic", "glass", "crystal", "energy"])
        viz_layout.addRow("Material:", self.material_combo)

        # Advanced rendering toggle
        self.advanced_rendering_check = QCheckBox()
        self.advanced_rendering_check.setChecked(True)
        viz_layout.addRow("Enhanced Lighting:", self.advanced_rendering_check)

        viz_group.setLayout(viz_layout)
        self.params_3d_layout.addRow("", viz_group)

        # Lighting options
        self.lighting_group = QGroupBox("Lighting")
        lighting_layout = QFormLayout()

        self.light_intensity_spin = QDoubleSpinBox()
        self.light_intensity_spin.setRange(0.1, 2.0)
        self.light_intensity_spin.setValue(1.0)
        self.light_intensity_spin.setSingleStep(0.1)
        lighting_layout.addRow("Intensity:", self.light_intensity_spin)

        self.light_angle_spin = QDoubleSpinBox()
        self.light_angle_spin.setRange(0, 360)
        self.light_angle_spin.setValue(45)
        self.light_angle_spin.setSingleStep(15)
        lighting_layout.addRow("Angle:", self.light_angle_spin)

        self.light_elevation_spin = QDoubleSpinBox()
        self.light_elevation_spin.setRange(0, 90)
        self.light_elevation_spin.setValue(45)
        self.light_elevation_spin.setSingleStep(5)
        lighting_layout.addRow("Elevation:", self.light_elevation_spin)

        # Light color selection
        self.light_color_combo = QComboBox()
        self.light_color_combo.addItems(["white", "warm", "cool", "golden", "blue", "red", "green"])
        lighting_layout.addRow("Light Color:", self.light_color_combo)

        # Ambient light intensity
        self.ambient_intensity_spin = QDoubleSpinBox()
        self.ambient_intensity_spin.setRange(0.0, 1.0)
        self.ambient_intensity_spin.setValue(0.2)
        self.ambient_intensity_spin.setSingleStep(0.05)
        lighting_layout.addRow("Ambient Light:", self.ambient_intensity_spin)

        self.lighting_group.setLayout(lighting_layout)
        self.params_3d_layout.addRow("", self.lighting_group)

        self.params_3d_group.setLayout(self.params_3d_layout)
        layout.addWidget(self.params_3d_group)

        # Generate button
        self.generate_3d_button = QPushButton("Generate 3D Shape")
        self.generate_3d_button.setObjectName("generateButton")
        self.generate_3d_button.clicked.connect(self.generate_output)
        layout.addWidget(self.generate_3d_button)

        # Add stretch to push everything to the top
        layout.addStretch()

        self.tab_3d.setLayout(layout)

    def setup_fractals_tab(self):
        """Set up the fractals tab with enhanced controls."""
        layout = QVBoxLayout()

        # Add title
        title_label = QLabel("Sacred Geometry Fractals")
        title_label.setObjectName("titleLabel")
        title_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(title_label)

        # Fractal selection
        fractal_group = QGroupBox("Fractal Selection")
        fractal_layout = QFormLayout()

        self.fractal_combo = QComboBox()
        self.fractal_combo.addItems([
            "Sierpinski Triangle", "Koch Snowflake", "Sacred Spiral",
            "Fractal Tree", "Dragon Curve", "Hilbert Curve"
        ])
        self.fractal_combo.currentTextChanged.connect(self.on_fractal_changed)
        fractal_layout.addRow("Fractal:", self.fractal_combo)

        fractal_group.setLayout(fractal_layout)
        layout.addWidget(fractal_group)

        # Fractal parameters
        self.params_fractal_group = QGroupBox("Fractal Parameters")
        self.params_fractal_layout = QFormLayout()

        # Common parameters
        self.depth_spin = QSpinBox()
        self.depth_spin.setRange(1, 10)
        self.depth_spin.setValue(5)
        self.params_fractal_layout.addRow("Depth/Iterations:", self.depth_spin)

        # Add depth slider
        self.depth_slider = QSlider(Qt.Horizontal)
        self.depth_slider.setRange(1, 10)
        self.depth_slider.setValue(5)
        self.depth_slider.valueChanged.connect(self.depth_spin.setValue)
        self.depth_spin.valueChanged.connect(self.depth_slider.setValue)
        self.params_fractal_layout.addRow("", self.depth_slider)

        # Sierpinski Triangle specific parameters
        self.size_spin = QDoubleSpinBox()
        self.size_spin.setRange(0.1, 10.0)
        self.size_spin.setValue(1.0)
        self.size_spin.setSingleStep(0.1)
        self.params_fractal_layout.addRow("Size:", self.size_spin)

        # Fractal Tree specific parameters
        self.angle_spin = QDoubleSpinBox()
        self.angle_spin.setRange(0, np.pi)
        self.angle_spin.setValue(np.pi/7)
        self.angle_spin.setSingleStep(np.pi/36)
        self.angle_spin.hide()  # Hide initially
        self.params_fractal_layout.addRow("Angle Delta:", self.angle_spin)

        self.length_factor_spin = QDoubleSpinBox()
        self.length_factor_spin.setRange(0.1, 0.9)
        self.length_factor_spin.setValue(0.7)
        self.length_factor_spin.setSingleStep(0.05)
        self.length_factor_spin.hide()  # Hide initially
        self.params_fractal_layout.addRow("Length Factor:", self.length_factor_spin)

        # Sacred Spiral specific parameters
        self.turns_spin = QDoubleSpinBox()
        self.turns_spin.setRange(1, 20)
        self.turns_spin.setValue(5)
        self.turns_spin.setSingleStep(1)
        self.turns_spin.hide()  # Hide initially
        self.params_fractal_layout.addRow("Turns:", self.turns_spin)

        # Visualization parameters
        self.color_scheme_fractal_combo = QComboBox()
        self.color_scheme_fractal_combo.addItems(["rainbow", "golden", "monochrome", "custom", "fire", "earth"])
        self.params_fractal_layout.addRow("Color Scheme:", self.color_scheme_fractal_combo)

        self.params_fractal_group.setLayout(self.params_fractal_layout)
        layout.addWidget(self.params_fractal_group)

        # Generate button
        self.generate_fractal_button = QPushButton("Generate Fractal")
        self.generate_fractal_button.setObjectName("generateButton")
        self.generate_fractal_button.clicked.connect(self.generate_output)
        layout.addWidget(self.generate_fractal_button)

        # Add stretch to push everything to the top
        layout.addStretch()

        self.tab_fractals.setLayout(layout)

    def setup_animations_tab(self):
        """Set up the animations tab with enhanced controls."""
        layout = QVBoxLayout()

        # Add title
        title_label = QLabel("Sacred Geometry Animations")
        title_label.setObjectName("titleLabel")
        title_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(title_label)

        # Animation selection
        animation_group = QGroupBox("Animation Selection")
        animation_layout = QFormLayout()

        self.animation_combo = QComboBox()
        self.animation_combo.addItems([
            "Flower of Life Growth", "Rotating Merkaba", "Sacred Spiral Growth",
            "Metatron's Cube Formation", "Koch Snowflake Evolution"
        ])
        self.animation_combo.currentTextChanged.connect(self.on_animation_changed)
        animation_layout.addRow("Animation:", self.animation_combo)

        animation_group.setLayout(animation_layout)
        layout.addWidget(animation_group)

        # Animation parameters
        self.params_animation_group = QGroupBox("Animation Parameters")
        self.params_animation_layout = QFormLayout()

        # Common parameters
        self.frames_spin = QSpinBox()
        self.frames_spin.setRange(20, 200)
        self.frames_spin.setValue(60)
        self.params_animation_layout.addRow("Frames:", self.frames_spin)

        # Add frames slider
        self.frames_slider = QSlider(Qt.Horizontal)
        self.frames_slider.setRange(20, 200)
        self.frames_slider.setValue(60)
        self.frames_slider.valueChanged.connect(self.frames_spin.setValue)
        self.frames_spin.valueChanged.connect(self.frames_slider.setValue)
        self.params_animation_layout.addRow("", self.frames_slider)

        self.fps_spin = QSpinBox()
        self.fps_spin.setRange(5, 30)
        self.fps_spin.setValue(15)
        self.params_animation_layout.addRow("FPS:", self.fps_spin)

        # Animation specific parameters
        self.anim_radius_spin = QDoubleSpinBox()
        self.anim_radius_spin.setRange(0.1, 5.0)
        self.anim_radius_spin.setValue(1.0)
        self.anim_radius_spin.setSingleStep(0.1)
        self.params_animation_layout.addRow("Radius:", self.anim_radius_spin)

        self.anim_max_layers_spin = QSpinBox()
        self.anim_max_layers_spin.setRange(1, 5)
        self.anim_max_layers_spin.setValue(3)
        self.params_animation_layout.addRow("Max Layers:", self.anim_max_layers_spin)

        # Visualization parameters
        self.color_scheme_anim_combo = QComboBox()
        self.color_scheme_anim_combo.addItems(["rainbow", "golden", "monochrome", "custom", "fire", "earth"])
        self.params_animation_layout.addRow("Color Scheme:", self.color_scheme_anim_combo)

        # Output options
        self.output_group = QGroupBox("Output Options")
        output_layout = QFormLayout()

        self.gif_radio = QRadioButton("GIF")
        self.gif_radio.setChecked(True)
        self.mp4_radio = QRadioButton("MP4")

        output_radio_layout = QHBoxLayout()
        output_radio_layout.addWidget(self.gif_radio)
        output_radio_layout.addWidget(self.mp4_radio)
        output_layout.addRow("Format:", output_radio_layout)

        self.resolution_combo = QComboBox()
        self.resolution_combo.addItems(["480p", "720p", "1080p"])
        self.resolution_combo.setCurrentIndex(1)  # Default to 720p
        output_layout.addRow("Resolution:", self.resolution_combo)

        self.output_group.setLayout(output_layout)
        self.params_animation_layout.addRow("", self.output_group)

        self.params_animation_group.setLayout(self.params_animation_layout)
        layout.addWidget(self.params_animation_group)

        # Generate button
        self.generate_animation_button = QPushButton("Generate Animation")
        self.generate_animation_button.setObjectName("generateButton")
        self.generate_animation_button.clicked.connect(self.generate_animation)
        layout.addWidget(self.generate_animation_button)

        # Add stretch to push everything to the top
        layout.addStretch()

        self.tab_animations.setLayout(layout)

    def setup_compositions_tab(self):
        """Set up the custom compositions tab."""
        layout = QVBoxLayout()

        # Add title
        title_label = QLabel("Sacred Geometry Compositions")
        title_label.setObjectName("titleLabel")
        title_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(title_label)

        # Composition selection
        composition_group = QGroupBox("Composition Selection")
        composition_layout = QFormLayout()

        self.composition_combo = QComboBox()
        self.composition_combo.addItems([
            "Flower of Life with Fibonacci",
            "Sacred Geometry Mandala",
            "Metatron's Cube with Platonic Solids",
            "Fractal Tree with Golden Ratio",
            "Nested Platonic Solids",
            "Cosmic Torus with Merkaba",
            "Tree of Life Template"
        ])
        self.composition_combo.currentTextChanged.connect(self.on_composition_changed)
        composition_layout.addRow("Composition:", self.composition_combo)

        composition_group.setLayout(composition_layout)
        layout.addWidget(composition_group)

        # Composition parameters
        self.params_comp_group = QGroupBox("Composition Parameters")
        self.params_comp_layout = QFormLayout()

        # Common parameters
        self.radius_comp_spin = QDoubleSpinBox()
        self.radius_comp_spin.setRange(0.1, 10.0)
        self.radius_comp_spin.setValue(1.0)
        self.radius_comp_spin.setSingleStep(0.1)
        self.params_comp_layout.addRow("Base Radius:", self.radius_comp_spin)

        # Add radius slider
        self.radius_comp_slider = QSlider(Qt.Horizontal)
        self.radius_comp_slider.setRange(1, 100)
        self.radius_comp_slider.setValue(10)
        self.radius_comp_slider.valueChanged.connect(lambda v: self.radius_comp_spin.setValue(v/10))
        self.radius_comp_spin.valueChanged.connect(lambda v: self.radius_comp_slider.setValue(int(v*10)))
        self.params_comp_layout.addRow("", self.radius_comp_slider)

        # Complexity parameter
        self.complexity_spin = QSpinBox()
        self.complexity_spin.setRange(1, 5)
        self.complexity_spin.setValue(3)
        self.params_comp_layout.addRow("Complexity:", self.complexity_spin)

        # Rotation parameter
        self.rotation_comp_spin = QDoubleSpinBox()
        self.rotation_comp_spin.setRange(0, 2*np.pi)
        self.rotation_comp_spin.setValue(0)
        self.rotation_comp_spin.setSingleStep(np.pi/12)
        self.params_comp_layout.addRow("Rotation:", self.rotation_comp_spin)

        # Special parameters for specific compositions
        # Torus parameters
        self.major_radius_comp_spin = QDoubleSpinBox()
        self.major_radius_comp_spin.setRange(0.5, 5.0)
        self.major_radius_comp_spin.setValue(2.0)
        self.major_radius_comp_spin.setSingleStep(0.1)
        self.params_comp_layout.addRow("Major Radius:", self.major_radius_comp_spin)

        self.minor_radius_comp_spin = QDoubleSpinBox()
        self.minor_radius_comp_spin.setRange(0.1, 2.0)
        self.minor_radius_comp_spin.setValue(0.5)
        self.minor_radius_comp_spin.setSingleStep(0.1)
        self.params_comp_layout.addRow("Minor Radius:", self.minor_radius_comp_spin)

        # Tree parameters
        self.depth_comp_spin = QSpinBox()
        self.depth_comp_spin.setRange(1, 8)
        self.depth_comp_spin.setValue(5)
        self.params_comp_layout.addRow("Depth:", self.depth_comp_spin)

        # Golden ratio option
        self.golden_ratio_check = QCheckBox()
        self.golden_ratio_check.setChecked(True)
        self.params_comp_layout.addRow("Use Golden Ratio:", self.golden_ratio_check)

        # Show paths option (for Tree of Life)
        self.show_paths_check = QCheckBox()
        self.show_paths_check.setChecked(True)
        self.params_comp_layout.addRow("Show Paths:", self.show_paths_check)

        # Show all solids option (for Metatron's Cube with Platonic Solids)
        self.show_all_solids_check = QCheckBox()
        self.show_all_solids_check.setChecked(True)
        self.params_comp_layout.addRow("Show All Solids:", self.show_all_solids_check)

        # Visualization parameters
        self.color_scheme_comp_combo = QComboBox()
        self.color_scheme_comp_combo.addItems(["golden", "rainbow", "cosmic", "ethereal", "chakra"])
        self.params_comp_layout.addRow("Color Scheme:", self.color_scheme_comp_combo)

        self.alpha_comp_spin = QDoubleSpinBox()
        self.alpha_comp_spin.setRange(0.1, 1.0)
        self.alpha_comp_spin.setValue(0.7)
        self.alpha_comp_spin.setSingleStep(0.1)
        self.params_comp_layout.addRow("Transparency:", self.alpha_comp_spin)

        self.show_labels_check = QCheckBox()
        self.show_labels_check.setChecked(False)
        self.params_comp_layout.addRow("Show Labels:", self.show_labels_check)

        self.params_comp_group.setLayout(self.params_comp_layout)
        layout.addWidget(self.params_comp_group)

        # Generate button
        self.generate_comp_button = QPushButton("Generate Composition")
        self.generate_comp_button.setObjectName("generateButton")
        self.generate_comp_button.clicked.connect(self.generate_output)
        layout.addWidget(self.generate_comp_button)

        # Add stretch to push everything to the top
        layout.addStretch()

        self.tab_compositions.setLayout(layout)

        # Initially hide special parameters
        self.update_composition_parameters()

    def on_tab_changed(self, index):
        """Handle tab change event."""
        tab_names = ["2D Patterns", "3D Shapes", "Fractals", "Animations", "Compositions"]
        self.current_category = tab_names[index]

        # Update the current pattern based on the selected tab
        if index == 0:  # 2D Patterns
            self.current_pattern = self.pattern_2d_combo.currentText()
            self.canvas.set_2d_axes()
            self.rotation_group.hide()
            self.export_button.hide()
        elif index == 1:  # 3D Shapes
            self.current_pattern = self.shape_3d_combo.currentText()
            self.canvas.set_3d_axes()
            self.rotation_group.show()
            self.export_button.show()
        elif index == 2:  # Fractals
            self.current_pattern = self.fractal_combo.currentText()
            self.canvas.set_2d_axes()
            self.rotation_group.hide()
            self.export_button.hide()
        elif index == 3:  # Animations
            self.current_pattern = self.animation_combo.currentText()
            self.canvas.set_2d_axes()
            self.rotation_group.hide()
            self.export_button.hide()
        elif index == 4:  # Compositions
            self.current_pattern = self.composition_combo.currentText()

            # Set 2D or 3D axes based on the composition type
            if self.current_pattern in ["Metatron's Cube with Platonic Solids", "Nested Platonic Solids", "Cosmic Torus with Merkaba"]:
                self.canvas.set_3d_axes()
                self.rotation_group.show()
                self.export_button.show()
            else:
                self.canvas.set_2d_axes()
                self.rotation_group.hide()
                self.export_button.hide()

        # Update the title
        self.title_label.setText(f"Sacred Geometry Explorer - {self.current_pattern}")

        # Generate the output for the new tab
        self.generate_output()

    def on_composition_changed(self, composition_name):
        """Handle composition selection change."""
        self.current_pattern = composition_name
        self.title_label.setText(f"Sacred Geometry Explorer - {composition_name}")

        # Update parameters visibility based on the selected composition
        self.update_composition_parameters()

        # Set 2D or 3D axes based on the composition type
        if composition_name in ["Metatron's Cube with Platonic Solids", "Nested Platonic Solids", "Cosmic Torus with Merkaba"]:
            self.canvas.set_3d_axes()
            self.rotation_group.show()
            self.export_button.show()
        else:
            self.canvas.set_2d_axes()
            self.rotation_group.hide()
            self.export_button.hide()

        # Update the UI
        self.generate_output()

    def update_composition_parameters(self):
        """Update the visibility of composition parameters based on the selected composition."""
        composition_name = self.current_pattern if self.current_category == "Compositions" else self.composition_combo.currentText()

        # Hide all special parameters first
        self.major_radius_comp_spin.hide()
        self.minor_radius_comp_spin.hide()
        self.depth_comp_spin.hide()
        self.golden_ratio_check.hide()
        self.show_paths_check.hide()
        self.show_all_solids_check.hide()

        # Show parameters based on the selected composition
        if composition_name == "Flower of Life with Fibonacci":
            self.complexity_spin.show()
            self.rotation_comp_spin.hide()
        elif composition_name == "Sacred Geometry Mandala":
            self.complexity_spin.show()
            self.rotation_comp_spin.show()
        elif composition_name == "Metatron's Cube with Platonic Solids":
            self.complexity_spin.hide()
            self.rotation_comp_spin.hide()
            self.show_all_solids_check.show()
        elif composition_name == "Fractal Tree with Golden Ratio":
            self.complexity_spin.hide()
            self.rotation_comp_spin.hide()
            self.depth_comp_spin.show()
            self.golden_ratio_check.show()
        elif composition_name == "Nested Platonic Solids":
            self.complexity_spin.show()
            self.rotation_comp_spin.hide()
        elif composition_name == "Cosmic Torus with Merkaba":
            self.complexity_spin.hide()
            self.rotation_comp_spin.show()
            self.major_radius_comp_spin.show()
            self.minor_radius_comp_spin.show()
        elif composition_name == "Tree of Life Template":
            self.complexity_spin.hide()
            self.rotation_comp_spin.hide()
            self.show_paths_check.show()

    def on_2d_pattern_changed(self, pattern_name):
        """Handle 2D pattern selection change."""
        self.current_pattern = pattern_name
        self.title_label.setText(f"Sacred Geometry Explorer - {pattern_name}")

        # Show/hide pattern-specific parameters
        if pattern_name == "Regular Polygon":
            self.sides_spin.show()
            self.rotation_2d_spin.show()
        else:
            self.sides_spin.hide()
            self.rotation_2d_spin.hide()

        # Update the UI
        self.generate_output()

    def on_3d_shape_changed(self, shape_name):
        """Handle 3D shape selection change."""
        self.current_pattern = shape_name
        self.title_label.setText(f"Sacred Geometry Explorer - {shape_name}")

        # Show/hide shape-specific parameters
        if shape_name == "Merkaba":
            self.rotation_3d_spin.show()
            self.major_radius_spin.hide()
            self.minor_radius_spin.hide()
            self.layers_3d_spin.hide()
        elif shape_name == "Torus":
            self.rotation_3d_spin.hide()
            self.major_radius_spin.show()
            self.minor_radius_spin.show()
            self.layers_3d_spin.hide()
        elif shape_name == "Flower of Life 3D":
            self.rotation_3d_spin.hide()
            self.major_radius_spin.hide()
            self.minor_radius_spin.hide()
            self.layers_3d_spin.show()
        else:
            self.rotation_3d_spin.hide()
            self.major_radius_spin.hide()
            self.minor_radius_spin.hide()
            self.layers_3d_spin.hide()

        # Update the UI
        self.generate_output()

    def on_fractal_changed(self, fractal_name):
        """Handle fractal selection change."""
        self.current_pattern = fractal_name
        self.title_label.setText(f"Sacred Geometry Explorer - {fractal_name}")

        # Show/hide fractal-specific parameters
        if fractal_name == "Fractal Tree":
            self.angle_spin.show()
            self.length_factor_spin.show()
            self.turns_spin.hide()
        elif fractal_name == "Sacred Spiral":
            self.angle_spin.hide()
            self.length_factor_spin.hide()
            self.turns_spin.show()
        else:
            self.angle_spin.hide()
            self.length_factor_spin.hide()
            self.turns_spin.hide()

        # Update the UI
        self.generate_output()

    def on_animation_changed(self, animation_name):
        """Handle animation selection change."""
        self.current_pattern = animation_name
        self.title_label.setText(f"Sacred Geometry Explorer - {animation_name}")

    def toggle_rotation(self, checked):
        """Toggle 3D shape auto-rotation."""
        if checked:
            self.rotation_timer.start(50)  # Update every 50ms
            self.status_bar.showMessage("Auto-rotation enabled")
        else:
            self.rotation_timer.stop()
            self.status_bar.showMessage("Auto-rotation disabled")

    def set_rotation_speed(self, value):
        """Set the rotation speed."""
        self.rotation_speed = value
        self.status_bar.showMessage(f"Rotation speed set to {value}")

    def rotate_3d_shape(self):
        """Rotate the 3D shape for animation."""
        if hasattr(self.canvas.axes, 'azim'):
            # Get current view angles
            elev = self.canvas.axes.elev
            azim = (self.canvas.axes.azim + self.rotation_speed) % 360

            # Set new view angles
            self.canvas.axes.view_init(elev=elev, azim=azim)
            self.canvas.draw()

    def show_help(self):
        """Show help information."""
        QMessageBox.information(self, "Help",
                              "Sacred Geometry Explorer\n\n"
                              "This application allows you to explore and create sacred geometry patterns, "
                              "shapes, fractals, and animations.\n\n"
                              "1. Select a category from the tabs on the left\n"
                              "2. Choose a specific pattern or shape\n"
                              "3. Adjust parameters using the controls\n"
                              "4. Click the Generate button to create your sacred geometry\n"
                              "5. Use the toolbar to zoom, pan, and save your creation\n\n"
                              "For 3D shapes, you can enable auto-rotation and adjust the rotation speed.")

    def show_pattern_info(self):
        """Show educational information about the current pattern."""
        try:
            # Get information about the current pattern
            pattern_info = get_pattern_info(self.current_pattern)

            if pattern_info:
                # Create a formatted message with the pattern information
                message = f"<h2>{self.current_pattern}</h2>"
                message += f"<p><b>Summary:</b> {pattern_info['summary']}</p>"

                if 'history' in pattern_info:
                    message += f"<p><b>History:</b> {pattern_info['history']}</p>"

                if 'significance' in pattern_info:
                    message += f"<p><b>Significance:</b> {pattern_info['significance']}</p>"

                if 'mathematics' in pattern_info:
                    message += f"<p><b>Mathematics:</b> {pattern_info['mathematics']}</p>"

                if 'cultural_connections' in pattern_info:
                    message += "<p><b>Cultural Connections:</b></p><ul>"
                    for culture, connection in pattern_info['cultural_connections'].items():
                        message += f"<li><b>{culture}:</b> {connection}</li>"
                    message += "</ul>"

                if 'related_concepts' in pattern_info:
                    message += "<p><b>Related Concepts:</b> "
                    message += ", ".join(pattern_info['related_concepts'])
                    message += "</p>"

                # Show the information in a message box
                info_dialog = QMessageBox(self)
                info_dialog.setWindowTitle(f"About {self.current_pattern}")
                info_dialog.setTextFormat(Qt.RichText)
                info_dialog.setText(message)
                info_dialog.setIcon(QMessageBox.Information)
                info_dialog.exec_()
            else:
                QMessageBox.information(self, "Pattern Information",
                                      f"No detailed information available for {self.current_pattern}.")
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Error retrieving pattern information: {str(e)}")

    def save_output(self):
        """Save the current output to a file."""
        # Get the current pattern name for the default filename
        pattern_name = self.current_pattern.lower().replace(" ", "_").replace("'", "")

        # Get the appropriate directory based on the current category
        if self.current_category == "2D Patterns":
            directory = output_dirs['2d']
            file_filter = "PNG Files (*.png);;SVG Files (*.svg);;PDF Files (*.pdf);;High-Resolution PNG (*.png);;All Files (*)"
        elif self.current_category == "3D Shapes":
            directory = output_dirs['3d']
            file_filter = "PNG Files (*.png);;PDF Files (*.pdf);;All Files (*)"
        elif self.current_category == "Fractals":
            directory = output_dirs['fractals']
            file_filter = "PNG Files (*.png);;SVG Files (*.svg);;PDF Files (*.pdf);;High-Resolution PNG (*.png);;All Files (*)"
        elif self.current_category == "Compositions":
            # Create a compositions directory if it doesn't exist
            if not os.path.exists("outputs/compositions"):
                os.makedirs("outputs/compositions", exist_ok=True)
            directory = "outputs/compositions"

            # Determine file filter based on composition type
            if self.current_pattern in ["Metatron's Cube with Platonic Solids", "Nested Platonic Solids", "Cosmic Torus with Merkaba"]:
                file_filter = "PNG Files (*.png);;PDF Files (*.pdf);;All Files (*)"
            else:
                file_filter = "PNG Files (*.png);;SVG Files (*.svg);;PDF Files (*.pdf);;High-Resolution PNG (*.png);;All Files (*)"
        else:
            directory = "outputs"
            file_filter = "PNG Files (*.png);;All Files (*)"

        # Create the directory if it doesn't exist
        os.makedirs(directory, exist_ok=True)

        # Get the default filepath
        default_filepath = os.path.join(directory, f"{pattern_name}.png")

        # Open file dialog
        filepath, selected_filter = QFileDialog.getSaveFileName(
            self, "Save Output", default_filepath, file_filter
        )

        if filepath:
            try:
                # Determine the export format based on the file extension or selected filter
                file_ext = os.path.splitext(filepath)[1].lower()

                if "High-Resolution" in selected_filter or (file_ext == ".png" and "High-Resolution" in selected_filter):
                    # Export high-resolution image
                    export_high_resolution_image(
                        self.canvas.fig,
                        filepath,
                        dpi=600,
                        format="png" if file_ext == "" else file_ext[1:],
                        transparent=False
                    )
                elif file_ext == ".svg" or "SVG" in selected_filter:
                    # For 2D patterns, export as SVG
                    if self.current_category == "2D Patterns":
                        # Get the current pattern
                        if self.current_pattern == "Flower of Life":
                            pattern = create_flower_of_life(center=(0, 0), radius=self.radius_2d_spin.value(), layers=self.layers_spin.value())
                        elif self.current_pattern == "Seed of Life":
                            pattern = create_seed_of_life(center=(0, 0), radius=self.radius_2d_spin.value())
                        elif self.current_pattern == "Metatron's Cube":
                            pattern = create_metatrons_cube(center=(0, 0), radius=self.radius_2d_spin.value())
                        elif self.current_pattern == "Vesica Piscis":
                            radius = self.radius_2d_spin.value()
                            pattern = create_vesica_piscis(center1=(-radius/2, 0), center2=(radius/2, 0), radius=radius)
                        elif self.current_pattern == "Fibonacci Spiral":
                            pattern = create_fibonacci_spiral(center=(0, 0), scale=self.radius_2d_spin.value()/10, n_iterations=10)
                        elif self.current_pattern == "Regular Polygon":
                            pattern = create_regular_polygon(
                                center=(0, 0),
                                radius=self.radius_2d_spin.value(),
                                sides=self.sides_spin.value(),
                                rotation=self.rotation_2d_spin.value()
                            )
                        elif self.current_pattern == "Golden Rectangle":
                            pattern = create_golden_rectangle(center=(0, 0), width=self.radius_2d_spin.value()*2)

                        # Export as SVG
                        export_svg(
                            pattern,
                            filepath,
                            width="800px",
                            height="800px",
                            background_color="#1a1a2e",
                            line_color="#daa520",
                            show_points=self.show_points_check.isChecked()
                        )
                    else:
                        # For other categories, save as PNG
                        export_2d_image(
                            self.canvas.fig,
                            filepath,
                            dpi=300,
                            format="png",
                            transparent=False
                        )
                else:
                    # Default to PNG or PDF export
                    export_format = "pdf" if file_ext == ".pdf" else "png"
                    export_2d_image(
                        self.canvas.fig,
                        filepath,
                        dpi=300,
                        format=export_format,
                        transparent=False
                    )

                QMessageBox.information(self, "Save Complete", f"Output saved to {filepath}")
            except Exception as e:
                QMessageBox.warning(self, "Error", f"Error saving output: {str(e)}")

    def export_output(self):
        """Export the current 3D shape to a file."""
        if self.current_category != "3D Shapes" and (self.current_category != "Compositions" or
                                                   self.current_pattern not in ["Metatron's Cube with Platonic Solids",
                                                                              "Nested Platonic Solids",
                                                                              "Cosmic Torus with Merkaba"]):
            QMessageBox.warning(self, "Export Error", "Only 3D shapes and 3D compositions can be exported.")
            return

        # Get the export file path
        filepath, selected_filter = QFileDialog.getSaveFileName(
            self, "Export 3D Model",
            f"outputs/3d/{self.current_pattern.lower().replace(' ', '_')}.obj",
            "OBJ Files (*.obj);;STL Files (*.stl);;3D Print Ready (*.stl);;All Files (*)"
        )

        if filepath:
            try:
                # Get the current shape
                if self.current_category == "3D Shapes":
                    radius = self.radius_3d_spin.value()

                    if self.current_pattern == "Tetrahedron":
                        shape = create_tetrahedron(center=(0, 0, 0), radius=radius)
                    elif self.current_pattern == "Cube":
                        shape = create_cube(center=(0, 0, 0), radius=radius)
                    elif self.current_pattern == "Octahedron":
                        shape = create_octahedron(center=(0, 0, 0), radius=radius)
                    elif self.current_pattern == "Icosahedron":
                        shape = create_icosahedron(center=(0, 0, 0), radius=radius)
                    elif self.current_pattern == "Dodecahedron":
                        shape = create_dodecahedron(center=(0, 0, 0), radius=radius)
                    elif self.current_pattern == "Merkaba":
                        rotation = self.rotation_3d_spin.value()
                        shape = create_merkaba(center=(0, 0, 0), radius=radius, rotation=rotation)
                    elif self.current_pattern == "Cuboctahedron (Vector Equilibrium)":
                        shape = create_cuboctahedron(center=(0, 0, 0), radius=radius)
                    elif self.current_pattern == "Torus":
                        major_radius = self.major_radius_spin.value()
                        minor_radius = self.minor_radius_spin.value()
                        shape = create_torus(
                            center=(0, 0, 0),
                            major_radius=major_radius,
                            minor_radius=minor_radius,
                            num_major_segments=48,
                            num_minor_segments=24
                        )
                    elif self.current_pattern == "Flower of Life 3D":
                        layers = self.layers_3d_spin.value()
                        shape = create_flower_of_life_3d(center=(0, 0, 0), radius=radius, layers=layers)
                    else:
                        QMessageBox.warning(self, "Export Error", f"Shape {self.current_pattern} not supported for export.")
                        return

                elif self.current_category == "Compositions":
                    # Handle 3D compositions
                    radius = self.radius_comp_spin.value()

                    if self.current_pattern == "Metatron's Cube with Platonic Solids":
                        show_all_solids = self.show_all_solids_check.isChecked()
                        composition = create_metatrons_cube_with_platonic_projections(
                            center=(0, 0, 0),
                            radius=radius,
                            show_all_solids=show_all_solids
                        )

                        # For export, we'll use the first Platonic solid
                        if show_all_solids:
                            # Combine all solids for export
                            all_vertices = []
                            all_faces = []
                            vertex_offset = 0

                            for solid_name, solid in composition["platonic_solids"].items():
                                vertices = solid["vertices"]
                                faces = solid["faces"]
                                all_vertices.extend(vertices)

                                # Adjust face indices
                                adjusted_faces = [[idx + vertex_offset for idx in face] for face in faces]
                                all_faces.extend(adjusted_faces)

                                vertex_offset += len(vertices)

                            shape = {
                                "vertices": np.array(all_vertices),
                                "faces": all_faces
                            }
                        else:
                            # Just use the tetrahedron
                            shape = composition["platonic_solids"]["tetrahedron"]

                    elif self.current_pattern == "Nested Platonic Solids":
                        complexity = self.complexity_spin.value()
                        composition = create_nested_platonic_solids(
                            center=(0, 0, 0),
                            radius=radius,
                            complexity=complexity
                        )

                        # Combine all solids for export
                        all_vertices = []
                        all_faces = []
                        vertex_offset = 0

                        for solid_info in composition["solids"]:
                            solid = solid_info["solid"]
                            vertices = solid["vertices"]
                            faces = solid["faces"]
                            all_vertices.extend(vertices)

                            # Adjust face indices
                            adjusted_faces = [[idx + vertex_offset for idx in face] for face in faces]
                            all_faces.extend(adjusted_faces)

                            vertex_offset += len(vertices)

                        shape = {
                            "vertices": np.array(all_vertices),
                            "faces": all_faces
                        }

                    elif self.current_pattern == "Cosmic Torus with Merkaba":
                        major_radius = self.major_radius_comp_spin.value()
                        minor_radius = self.minor_radius_comp_spin.value()
                        rotation = self.rotation_comp_spin.value()
                        composition = create_cosmic_torus_with_merkaba(
                            center=(0, 0, 0),
                            major_radius=major_radius,
                            minor_radius=minor_radius,
                            merkaba_radius=radius,
                            merkaba_rotation=rotation
                        )

                        # For export, we'll combine the torus and merkaba
                        torus = composition["torus"]
                        merkaba = composition["merkaba"]

                        torus_vertices = torus["vertices"]
                        torus_faces = torus["faces"]
                        merkaba_vertices = merkaba["vertices"]
                        merkaba_faces = merkaba["faces"]

                        # Combine vertices and adjust face indices
                        all_vertices = np.vstack((torus_vertices, merkaba_vertices))
                        merkaba_faces_adjusted = [[idx + len(torus_vertices) for idx in face] for face in merkaba_faces]
                        all_faces = torus_faces + merkaba_faces_adjusted

                        shape = {
                            "vertices": all_vertices,
                            "faces": all_faces
                        }
                    else:
                        QMessageBox.warning(self, "Export Error", f"Composition {self.current_pattern} not supported for 3D export.")
                        return

                # Determine the export format based on the file extension or selected filter
                file_ext = os.path.splitext(filepath)[1].lower()

                if "3D Print Ready" in selected_filter:
                    # Export for 3D printing
                    export_for_3d_printing(
                        shape,
                        filepath,
                        scale=1.0,
                        wall_thickness=0.1,
                        solid=False,
                        format="stl" if file_ext == ".stl" else "obj"
                    )
                elif file_ext == ".stl" or "STL" in selected_filter:
                    # Export as STL
                    export_stl(
                        shape,
                        filepath,
                        scale=1.0,
                        binary=True
                    )
                else:
                    # Default to OBJ export
                    export_3d_obj(
                        shape,
                        filepath,
                        scale=1.0,
                        include_normals=True,
                        include_materials=True
                    )

                QMessageBox.information(self, "Export Complete", f"3D model exported to {filepath}")
            except Exception as e:
                QMessageBox.warning(self, "Export Error", f"Error exporting 3D model: {str(e)}")

    def generate_output(self):
        """Generate the selected pattern or shape and display it."""
        self.canvas.clear_plot()

        try:
            if self.current_category == "2D Patterns":
                self.generate_2d_pattern()
            elif self.current_category == "3D Shapes":
                self.generate_3d_shape()
            elif self.current_category == "Fractals":
                self.generate_fractal()
            elif self.current_category == "Compositions":
                self.generate_composition()

            self.canvas.draw()
            self.status_bar.showMessage(f"Generated {self.current_pattern}")
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Error generating output: {str(e)}")
            self.status_bar.showMessage("Error generating output")

    def generate_composition(self):
        """Generate a custom composition based on current settings."""
        # Get common parameters
        radius = self.radius_comp_spin.value()
        color_scheme = self.color_scheme_comp_combo.currentText().lower()
        alpha = self.alpha_comp_spin.value()
        show_labels = self.show_labels_check.isChecked()

        # Generate the composition based on selection
        if self.current_pattern == "Flower of Life with Fibonacci":
            complexity = self.complexity_spin.value()
            composition = create_flower_of_life_with_fibonacci(
                center=(0, 0),
                radius=radius,
                layers=complexity,
                spiral_scale=0.1,
                spiral_turns=complexity * 2
            )

        elif self.current_pattern == "Sacred Geometry Mandala":
            complexity = self.complexity_spin.value()
            rotation = self.rotation_comp_spin.value()
            composition = create_sacred_geometry_mandala(
                center=(0, 0),
                radius=radius,
                complexity=complexity,
                rotation=rotation
            )

        elif self.current_pattern == "Metatron's Cube with Platonic Solids":
            show_all_solids = self.show_all_solids_check.isChecked()
            composition = create_metatrons_cube_with_platonic_projections(
                center=(0, 0, 0),
                radius=radius,
                show_all_solids=show_all_solids
            )

        elif self.current_pattern == "Fractal Tree with Golden Ratio":
            depth = self.depth_comp_spin.value()
            use_golden_ratio = self.golden_ratio_check.isChecked()
            composition = create_fractal_tree_with_golden_ratio(
                center=(0, 0),
                size=radius,
                depth=depth,
                use_golden_ratio=use_golden_ratio
            )

        elif self.current_pattern == "Nested Platonic Solids":
            complexity = self.complexity_spin.value()
            composition = create_nested_platonic_solids(
                center=(0, 0, 0),
                radius=radius,
                complexity=complexity
            )

        elif self.current_pattern == "Cosmic Torus with Merkaba":
            major_radius = self.major_radius_comp_spin.value()
            minor_radius = self.minor_radius_comp_spin.value()
            rotation = self.rotation_comp_spin.value()
            composition = create_cosmic_torus_with_merkaba(
                center=(0, 0, 0),
                major_radius=major_radius,
                minor_radius=minor_radius,
                merkaba_radius=radius,
                merkaba_rotation=rotation
            )

        elif self.current_pattern == "Tree of Life Template":
            show_paths = self.show_paths_check.isChecked()
            composition = create_tree_of_life_template(
                center=(0, 0),
                size=radius * 2,
                with_paths=show_paths
            )

        else:
            return

        # Plot the composition using standard plotting
        plot_composition(
            composition,
            ax=self.canvas.axes,
            color_scheme=color_scheme,
            show_labels=show_labels,
            alpha=alpha
        )

        # Set axis limits based on composition type
        if composition["type"] == "2D":
            self.canvas.axes.set_xlim(-radius*3, radius*3)
            self.canvas.axes.set_ylim(-radius*3, radius*3)
        else:
            # For 3D compositions
            self.canvas.axes.set_xlim(-radius*2, radius*2)
            self.canvas.axes.set_ylim(-radius*2, radius*2)
            self.canvas.axes.set_zlim(-radius*2, radius*2)
            self.canvas.axes.set_box_aspect([1, 1, 1])  # Equal aspect ratio

    def generate_2d_pattern(self):
        """Generate a 2D pattern based on current settings."""
        # Get common parameters
        radius = self.radius_2d_spin.value()
        color_scheme = self.color_scheme_combo.currentText().lower()
        show_points = self.show_points_check.isChecked()

        # Generate the pattern based on selection
        if self.current_pattern == "Flower of Life":
            layers = self.layers_spin.value()
            pattern = create_flower_of_life(center=(0, 0), radius=radius, layers=layers)
        elif self.current_pattern == "Seed of Life":
            pattern = create_seed_of_life(center=(0, 0), radius=radius)
        elif self.current_pattern == "Metatron's Cube":
            pattern = create_metatrons_cube(center=(0, 0), radius=radius)
        elif self.current_pattern == "Vesica Piscis":
            pattern = create_vesica_piscis(center1=(-radius/2, 0), center2=(radius/2, 0), radius=radius)
        elif self.current_pattern == "Fibonacci Spiral":
            pattern = create_fibonacci_spiral(center=(0, 0), scale=radius/10, n_iterations=10)
        elif self.current_pattern == "Regular Polygon":
            sides = self.sides_spin.value()
            rotation = self.rotation_2d_spin.value()
            pattern = create_regular_polygon(center=(0, 0), radius=radius, sides=sides, rotation=rotation)
        elif self.current_pattern == "Golden Rectangle":
            pattern = create_golden_rectangle(center=(0, 0), width=radius*2)
        else:
            return

        # Plot the pattern
        plot_2d_pattern(
            pattern,
            title=self.current_pattern,
            show_points=show_points,
            color_scheme=color_scheme,
            figure_size=(8, 8),
            ax=self.canvas.axes
        )

        # Set axis limits
        self.canvas.axes.set_xlim(-radius*3, radius*3)
        self.canvas.axes.set_ylim(-radius*3, radius*3)

    def generate_3d_shape(self):
        """Generate a 3D shape based on current settings."""
        # Get common parameters
        radius = self.radius_3d_spin.value()
        color_scheme = self.color_scheme_3d_combo.currentText().lower()
        alpha = self.alpha_3d_spin.value()
        show_edges = self.show_edges_check.isChecked()
        show_vertices = self.show_vertices_check.isChecked()

        # Get material settings
        material = self.material_combo.currentText().lower()

        # Generate the shape based on selection
        if self.current_pattern == "Tetrahedron":
            shape = create_tetrahedron(center=(0, 0, 0), radius=radius)
        elif self.current_pattern == "Cube":
            shape = create_cube(center=(0, 0, 0), radius=radius)
        elif self.current_pattern == "Octahedron":
            shape = create_octahedron(center=(0, 0, 0), radius=radius)
        elif self.current_pattern == "Icosahedron":
            shape = create_icosahedron(center=(0, 0, 0), radius=radius)
        elif self.current_pattern == "Dodecahedron":
            shape = create_dodecahedron(center=(0, 0, 0), radius=radius)
        elif self.current_pattern == "Merkaba":
            rotation = self.rotation_3d_spin.value()
            shape = create_merkaba(center=(0, 0, 0), radius=radius, rotation=rotation)
        elif self.current_pattern == "Cuboctahedron (Vector Equilibrium)":
            shape = create_cuboctahedron(center=(0, 0, 0), radius=radius)
        elif self.current_pattern == "Torus":
            major_radius = self.major_radius_spin.value()
            minor_radius = self.minor_radius_spin.value()
            shape = create_torus(
                center=(0, 0, 0),
                major_radius=major_radius,
                minor_radius=minor_radius,
                num_major_segments=48,
                num_minor_segments=24
            )
        elif self.current_pattern == "Flower of Life 3D":
            layers = self.layers_3d_spin.value()
            shape = create_flower_of_life_3d(center=(0, 0, 0), radius=radius, layers=layers)
        else:
            return

        # Get lighting parameters for advanced rendering
        if self.advanced_rendering_check.isChecked():
            light_intensity = self.light_intensity_spin.value()
            light_angle = self.light_angle_spin.value() * np.pi / 180
            light_elevation = self.light_elevation_spin.value() * np.pi / 180

            # Calculate light direction from angle and elevation
            light_x = np.sin(light_angle) * np.cos(light_elevation)
            light_y = np.cos(light_angle) * np.cos(light_elevation)
            light_z = np.sin(light_elevation)
            light_direction = np.array([light_x, light_y, light_z])
        else:
            # Default values if not using advanced rendering
            light_intensity = 1.0
            light_direction = np.array([1, 1, 1])

        # Check if advanced rendering is enabled
        if self.advanced_rendering_check.isChecked():
            # Use lighting effects
            plot_3d_shape_with_lighting(
                shape,
                ax=self.canvas.axes,
                color_scheme=color_scheme,
                material=material,
                alpha=alpha,
                show_edges=show_edges,
                show_vertices=show_vertices,
                light_direction=light_direction,
                light_intensity=light_intensity,
                title=self.current_pattern
            )
        else:
            # Use standard 3D rendering
            plot_3d_shape(
                shape,
                title=self.current_pattern,
                color_scheme=color_scheme,
                alpha=alpha,
                show_edges=show_edges,
                show_vertices=show_vertices,
                figure_size=(8, 8),
                ax=self.canvas.axes
            )

    def generate_fractal(self):
        """Generate a fractal based on current settings."""
        # Get common parameters
        depth = self.depth_spin.value()
        size = self.size_spin.value()
        # Color scheme will be used in future updates for more advanced fractal rendering
        # color_scheme = self.color_scheme_fractal_combo.currentText().lower()

        # Generate the fractal based on selection
        if self.current_pattern == "Sierpinski Triangle":
            # Create initial triangle
            initial_triangle = np.array([
                [0, 0],
                [size, 0],
                [size/2, size*np.sqrt(3)/2]
            ])

            # Generate Sierpinski triangle
            triangles = sierpinski_triangle(initial_triangle, depth)

            # Plot the triangles
            for triangle in triangles:
                # Close the triangle by repeating the first vertex
                triangle_closed = np.vstack([triangle, triangle[0]])
                self.canvas.axes.plot(triangle_closed[:, 0], triangle_closed[:, 1], 'b-', linewidth=0.5)

            self.canvas.axes.set_title("Sierpinski Triangle")
            self.canvas.axes.set_aspect('equal')
            self.canvas.axes.set_xlim(-0.1*size, 1.1*size)
            self.canvas.axes.set_ylim(-0.1*size, 1.0*size)

        elif self.current_pattern == "Koch Snowflake":
            # Create initial hexagon
            initial_hexagon = create_regular_polygon(center=(0, 0), radius=size, sides=6)

            # Generate Koch snowflake
            snowflake = koch_snowflake(initial_hexagon, depth)

            # Close the curve by repeating the first vertex
            snowflake_closed = np.vstack([snowflake, snowflake[0]])
            self.canvas.axes.plot(snowflake_closed[:, 0], snowflake_closed[:, 1], 'b-', linewidth=1)

            self.canvas.axes.set_title("Koch Snowflake")
            self.canvas.axes.set_aspect('equal')
            self.canvas.axes.set_xlim(-1.5*size, 1.5*size)
            self.canvas.axes.set_ylim(-1.5*size, 1.5*size)

        elif self.current_pattern == "Sacred Spiral":
            turns = self.turns_spin.value()

            # Generate sacred spiral
            spiral = sacred_spiral(
                center=(0, 0),
                start_radius=0.1*size,
                max_radius=5.0*size,
                turns=turns,
                points_per_turn=100
            )

            self.canvas.axes.plot(spiral[:, 0], spiral[:, 1], 'r-', linewidth=2)

            self.canvas.axes.set_title("Sacred Spiral (Golden Ratio)")
            self.canvas.axes.set_aspect('equal')
            self.canvas.axes.set_xlim(-5.5*size, 5.5*size)
            self.canvas.axes.set_ylim(-5.5*size, 5.5*size)

        elif self.current_pattern == "Fractal Tree":
            angle_delta = self.angle_spin.value()
            length_factor = self.length_factor_spin.value()

            # Generate fractal tree
            tree_branches = fractal_tree(
                start=(0, -3*size),
                angle=np.pi/2,  # Initial angle (pointing up)
                length=2.0*size,  # Initial branch length
                depth=depth,
                length_factor=length_factor,
                angle_delta=angle_delta
            )

            for branch in tree_branches:
                self.canvas.axes.plot(branch[:, 0], branch[:, 1], 'brown', linewidth=1)

            self.canvas.axes.set_title("Fractal Tree")
            self.canvas.axes.set_aspect('equal')
            self.canvas.axes.set_xlim(-5*size, 5*size)
            self.canvas.axes.set_ylim(-3*size, 5*size)

        elif self.current_pattern == "Dragon Curve":
            # Generate dragon curve
            curve = dragon_curve(iterations=depth)

            self.canvas.axes.plot(curve[:, 0], curve[:, 1], 'g-', linewidth=1)

            self.canvas.axes.set_title("Dragon Curve")
            self.canvas.axes.set_aspect('equal')
            self.canvas.axes.set_xlim(-2*size, 2*size)
            self.canvas.axes.set_ylim(-2*size, 2*size)

        elif self.current_pattern == "Hilbert Curve":
            # Generate Hilbert curve
            curve = hilbert_curve(order=depth, size=size*10)

            self.canvas.axes.plot(curve[:, 0], curve[:, 1], 'b-', linewidth=1)

            self.canvas.axes.set_title("Hilbert Curve")
            self.canvas.axes.set_aspect('equal')
            self.canvas.axes.set_xlim(-1*size, 11*size)
            self.canvas.axes.set_ylim(-1*size, 11*size)

    def generate_animation(self):
        """Generate an animation based on current settings."""
        QMessageBox.information(self, "Animation",
                              "Animations will be saved to the outputs/animations directory.\n"
                              "This may take a moment...")

        # Get common parameters
        frames = self.frames_spin.value()
        fps = self.fps_spin.value()
        radius = self.anim_radius_spin.value()
        max_layers = self.anim_max_layers_spin.value()
        color_scheme = self.color_scheme_anim_combo.currentText().lower()

        # Create output directory if it doesn't exist
        os.makedirs(output_dirs['animations'], exist_ok=True)

        try:
            if self.current_pattern == "Flower of Life Growth":
                # Create figure for animation
                fig, ax = plt.subplots(figsize=(10, 10))
                ax.set_aspect('equal')

                # Set dark theme for the figure
                fig.patch.set_facecolor('#1a1a2e')
                ax.set_facecolor('#1a1a2e')
                ax.tick_params(axis='x', colors='#c0c0d0')
                ax.tick_params(axis='y', colors='#c0c0d0')
                for spine in ax.spines.values():
                    spine.set_color('#3c3c4f')
                ax.title.set_color('#daa520')

                # Animation function
                def update(frame):
                    ax.clear()
                    ax.set_aspect('equal')
                    ax.set_title("Growing Flower of Life")
                    ax.set_xlim(-4*radius, 4*radius)
                    ax.set_ylim(-4*radius, 4*radius)
                    ax.grid(True, linestyle='--', alpha=0.7)

                    # Set dark theme for the axes after clearing
                    ax.set_facecolor('#1a1a2e')
                    ax.tick_params(axis='x', colors='#c0c0d0')
                    ax.tick_params(axis='y', colors='#c0c0d0')
                    for spine in ax.spines.values():
                        spine.set_color('#3c3c4f')
                    ax.title.set_color('#daa520')

                    # Calculate layer based on frame
                    layer = 1 + int(frame / frames * max_layers)

                    # Generate the flower of life with appropriate layer
                    flower = create_flower_of_life(center=(0, 0), radius=radius, layers=layer)

                    # Plot each circle
                    for i, circle in enumerate(flower):
                        alpha = min(1.0, (frame / (frames / max_layers)) - i * 0.05)
                        if alpha > 0:
                            ax.plot(circle[:, 0], circle[:, 1], 'b-', alpha=alpha)

                    return ax,

                # Create the animation
                anim = animation.FuncAnimation(
                    fig, update, frames=frames, interval=50, blit=False
                )

                # Save the animation
                filename = os.path.join(output_dirs['animations'], "flower_of_life_growing.gif")

                # Use our custom exporter
                if self.gif_radio.isChecked():
                    # Save as GIF
                    anim.save(filename, writer='pillow', fps=fps)
                    plt.close(fig)
                else:
                    # Save as MP4
                    mp4_filename = filename.replace('.gif', '.mp4')
                    try:
                        # Try to use ffmpeg writer
                        Writer = animation.writers['ffmpeg']
                        writer = Writer(fps=fps, metadata=dict(artist='Sacred Geometry Explorer'), bitrate=1800)
                        anim.save(mp4_filename, writer=writer)
                    except Exception:
                        # Fall back to GIF if MP4 fails
                        anim.save(filename, writer='pillow', fps=fps)
                        mp4_filename = filename

                    plt.close(fig)
                    filename = mp4_filename

                QMessageBox.information(self, "Animation Complete",
                                      f"Animation saved to {filename}")

            elif self.current_pattern == "Rotating Merkaba":
                # Create figure for animation
                fig = plt.figure(figsize=(10, 10))
                ax = fig.add_subplot(111, projection='3d')

                # Set dark theme for the figure
                fig.patch.set_facecolor('#1a1a2e')
                ax.set_facecolor('#1a1a2e')
                ax.tick_params(axis='x', colors='#c0c0d0')
                ax.tick_params(axis='y', colors='#c0c0d0')
                ax.tick_params(axis='z', colors='#c0c0d0')
                ax.xaxis.label.set_color('#c0c0d0')
                ax.yaxis.label.set_color('#c0c0d0')
                ax.zaxis.label.set_color('#c0c0d0')
                ax.title.set_color('#daa520')

                # Animation function
                def update(frame):
                    ax.clear()
                    ax.set_title("Rotating Merkaba")

                    # Set dark theme for the axes after clearing
                    ax.set_facecolor('#1a1a2e')
                    ax.tick_params(axis='x', colors='#c0c0d0')
                    ax.tick_params(axis='y', colors='#c0c0d0')
                    ax.tick_params(axis='z', colors='#c0c0d0')
                    ax.xaxis.label.set_color('#c0c0d0')
                    ax.yaxis.label.set_color('#c0c0d0')
                    ax.zaxis.label.set_color('#c0c0d0')
                    ax.title.set_color('#daa520')

                    # Calculate rotation based on frame
                    rotation = frame / frames * 2 * np.pi

                    # Create merkaba with current rotation
                    merkaba = create_merkaba(center=(0, 0, 0), radius=radius, rotation=rotation)

                    # Check if advanced rendering is enabled
                    if self.advanced_rendering_check.isChecked():
                        # Use lighting effects
                        # Calculate light direction based on frame
                        light_angle = (frame / frames * 2 * np.pi) + np.pi/4
                        light_elevation = np.pi/4
                        light_x = np.sin(light_angle) * np.cos(light_elevation)
                        light_y = np.cos(light_angle) * np.cos(light_elevation)
                        light_z = np.sin(light_elevation)
                        light_direction = np.array([light_x, light_y, light_z])

                        # Get material
                        material = self.material_combo.currentText().lower()

                        # Plot with lighting effects
                        plot_3d_shape_with_lighting(
                            merkaba,
                            ax=ax,
                            color_scheme=color_scheme,
                            material=material,
                            alpha=0.7,
                            show_edges=True,
                            show_vertices=True,
                            light_direction=light_direction,
                            light_intensity=1.0,
                            title="Rotating Merkaba"
                        )
                    else:
                        # Use standard 3D rendering
                        plot_3d_shape(
                            merkaba,
                            color_scheme=color_scheme,
                            alpha=0.7,
                            show_edges=True,
                            show_vertices=True,
                            ax=ax
                        )

                    # Set axis limits
                    ax.set_xlim(-1.5*radius, 1.5*radius)
                    ax.set_ylim(-1.5*radius, 1.5*radius)
                    ax.set_zlim(-1.5*radius, 1.5*radius)

                    # Set equal aspect ratio
                    ax.set_box_aspect([1, 1, 1])

                    return ax,

                # Create the animation
                anim = animation.FuncAnimation(
                    fig, update, frames=frames, interval=50, blit=False
                )

                # Save the animation
                filename = os.path.join(output_dirs['animations'], "rotating_merkaba.gif")

                # Use our custom exporter
                if self.gif_radio.isChecked():
                    # Save as GIF
                    anim.save(filename, writer='pillow', fps=fps)
                    plt.close(fig)
                else:
                    # Save as MP4
                    mp4_filename = filename.replace('.gif', '.mp4')
                    try:
                        # Try to use ffmpeg writer
                        Writer = animation.writers['ffmpeg']
                        writer = Writer(fps=fps, metadata=dict(artist='Sacred Geometry Explorer'), bitrate=1800)
                        anim.save(mp4_filename, writer=writer)
                    except Exception:
                        # Fall back to GIF if MP4 fails
                        anim.save(filename, writer='pillow', fps=fps)
                        mp4_filename = filename

                    plt.close(fig)
                    filename = mp4_filename

                QMessageBox.information(self, "Animation Complete",
                                      f"Animation saved to {filename}")

            # Add other animations as needed...

        except Exception as e:
            QMessageBox.warning(self, "Error", f"Error generating animation: {str(e)}")

def main():
    """Main function to run the application."""
    app = QApplication(sys.argv)
    window = SacredGeometryGUI()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
