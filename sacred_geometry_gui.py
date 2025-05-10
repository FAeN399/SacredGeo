"""
Sacred Geometry GUI Application

A comprehensive graphical user interface for generating and visualizing
sacred geometry patterns, shapes, and animations.
"""
import os
import sys
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QTabWidget, QLabel, QComboBox, QSlider, QCheckBox, QPushButton,
    QSpinBox, QDoubleSpinBox, QColorDialog, QFileDialog, QGroupBox,
    QFormLayout, QSplitter, QFrame, QMessageBox, QRadioButton, QButtonGroup,
    QSizePolicy
)
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QColor, QPixmap, QIcon

# Import core 2D pattern generators
from sacred_geometry.core.core import (
    create_flower_of_life, create_metatrons_cube, create_vesica_piscis,
    create_fibonacci_spiral, create_regular_polygon, create_golden_rectangle,
    create_seed_of_life, get_golden_ratio
)

# Import fractal pattern generators
from sacred_geometry.fractals.fractals import (
    sierpinski_triangle, koch_snowflake, sacred_spiral, fractal_tree,
    recursive_flower_of_life, dragon_curve, hilbert_curve, mandelbrot_set, julia_set
)

# Import 3D shape generators
from sacred_geometry.shapes.shapes import (
    create_tetrahedron, create_cube, create_octahedron,
    create_icosahedron, create_dodecahedron, create_merkaba,
    create_cuboctahedron, create_flower_of_life_3d, create_torus
)

# Import visualization tools
from sacred_geometry.visualization.visualization import (
    plot_2d_pattern, plot_3d_shape
)

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
    """Matplotlib canvas for displaying sacred geometry patterns and shapes."""

    def __init__(self, parent=None, width=8, height=8, dpi=100):
        self.fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = self.fig.add_subplot(111)

        FigureCanvas.__init__(self, self.fig)
        self.setParent(parent)

        FigureCanvas.setSizePolicy(self,
                                  QSizePolicy.Expanding,
                                  QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)

    def clear_plot(self):
        """Clear the current plot."""
        self.axes.clear()
        self.draw()

    def set_3d_axes(self):
        """Set up 3D axes for 3D shapes."""
        self.fig.clear()
        self.axes = self.fig.add_subplot(111, projection='3d')
        self.draw()

    def set_2d_axes(self):
        """Set up 2D axes for 2D patterns."""
        self.fig.clear()
        self.axes = self.fig.add_subplot(111)
        self.axes.set_aspect('equal')
        self.draw()

class SacredGeometryGUI(QMainWindow):
    """Main window for the Sacred Geometry GUI application."""

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Sacred Geometry Generator")
        self.setGeometry(100, 100, 1200, 800)

        # Create the main widget and layout
        self.main_widget = QWidget()
        self.setCentralWidget(self.main_widget)

        # Create a splitter for the main layout
        self.splitter = QSplitter(Qt.Horizontal)

        # Create the control panel
        self.control_panel = QTabWidget()
        self.setup_control_panel()

        # Create the visualization panel
        self.viz_panel = QWidget()
        self.setup_viz_panel()

        # Add widgets to splitter
        self.splitter.addWidget(self.control_panel)
        self.splitter.addWidget(self.viz_panel)
        self.splitter.setSizes([400, 800])

        # Set up the main layout
        main_layout = QVBoxLayout()
        main_layout.addWidget(self.splitter)
        self.main_widget.setLayout(main_layout)

        # Initialize the current category and pattern
        self.current_category = "2D Patterns"
        self.current_pattern = "Flower of Life"

        # Generate initial pattern
        self.generate_output()

    def setup_control_panel(self):
        """Set up the control panel with tabs for different categories."""
        # Create tabs for different categories
        self.tab_2d = QWidget()
        self.tab_3d = QWidget()
        self.tab_fractals = QWidget()
        self.tab_animations = QWidget()
        self.tab_custom = QWidget()

        # Add tabs to the control panel
        self.control_panel.addTab(self.tab_2d, "2D Patterns")
        self.control_panel.addTab(self.tab_3d, "3D Shapes")
        self.control_panel.addTab(self.tab_fractals, "Fractals")
        self.control_panel.addTab(self.tab_animations, "Animations")
        self.control_panel.addTab(self.tab_custom, "Custom")

        # Connect tab change signal
        self.control_panel.currentChanged.connect(self.on_tab_changed)

        # Set up each tab
        self.setup_2d_tab()
        self.setup_3d_tab()
        self.setup_fractals_tab()
        self.setup_animations_tab()
        self.setup_custom_tab()

    def setup_viz_panel(self):
        """Set up the visualization panel with matplotlib canvas."""
        viz_layout = QVBoxLayout()

        # Create matplotlib canvas
        self.canvas = MatplotlibCanvas(self.viz_panel, width=8, height=8)
        self.toolbar = NavigationToolbar(self.canvas, self.viz_panel)

        # Create save button
        self.save_button = QPushButton("Save Output")
        self.save_button.clicked.connect(self.save_output)

        # Add widgets to layout
        viz_layout.addWidget(self.toolbar)
        viz_layout.addWidget(self.canvas)
        viz_layout.addWidget(self.save_button)

        self.viz_panel.setLayout(viz_layout)

    def setup_2d_tab(self):
        """Set up the 2D patterns tab."""
        layout = QVBoxLayout()

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
        self.generate_2d_button.clicked.connect(self.generate_output)
        layout.addWidget(self.generate_2d_button)

        # Add stretch to push everything to the top
        layout.addStretch()

        self.tab_2d.setLayout(layout)

    def setup_3d_tab(self):
        """Set up the 3D shapes tab."""
        layout = QVBoxLayout()

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
        self.color_scheme_3d_combo = QComboBox()
        self.color_scheme_3d_combo.addItems(["rainbow", "golden", "monochrome", "custom"])
        self.params_3d_layout.addRow("Color Scheme:", self.color_scheme_3d_combo)

        self.alpha_3d_spin = QDoubleSpinBox()
        self.alpha_3d_spin.setRange(0.1, 1.0)
        self.alpha_3d_spin.setValue(0.7)
        self.alpha_3d_spin.setSingleStep(0.1)
        self.params_3d_layout.addRow("Transparency:", self.alpha_3d_spin)

        self.show_edges_check = QCheckBox()
        self.show_edges_check.setChecked(True)
        self.params_3d_layout.addRow("Show Edges:", self.show_edges_check)

        self.show_vertices_check = QCheckBox()
        self.show_vertices_check.setChecked(True)
        self.params_3d_layout.addRow("Show Vertices:", self.show_vertices_check)

        self.params_3d_group.setLayout(self.params_3d_layout)
        layout.addWidget(self.params_3d_group)

        # Generate button
        self.generate_3d_button = QPushButton("Generate Shape")
        self.generate_3d_button.clicked.connect(self.generate_output)
        layout.addWidget(self.generate_3d_button)

        # Add stretch to push everything to the top
        layout.addStretch()

        self.tab_3d.setLayout(layout)

    def setup_fractals_tab(self):
        """Set up the fractals tab."""
        layout = QVBoxLayout()

        # Fractal selection
        fractal_group = QGroupBox("Fractal Selection")
        fractal_layout = QFormLayout()

        self.fractal_combo = QComboBox()
        self.fractal_combo.addItems([
            "Sierpinski Triangle", "Koch Snowflake", "Sacred Spiral",
            "Fractal Tree", "Dragon Curve", "Hilbert Curve",
            "Mandelbrot Set", "Julia Set"
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

        # Mandelbrot/Julia specific parameters
        self.max_iter_spin = QSpinBox()
        self.max_iter_spin.setRange(10, 1000)
        self.max_iter_spin.setValue(100)
        self.max_iter_spin.setSingleStep(10)
        self.max_iter_spin.hide()  # Hide initially
        self.params_fractal_layout.addRow("Max Iterations:", self.max_iter_spin)

        self.julia_c_real_spin = QDoubleSpinBox()
        self.julia_c_real_spin.setRange(-2.0, 2.0)
        self.julia_c_real_spin.setValue(-0.7)
        self.julia_c_real_spin.setSingleStep(0.05)
        self.julia_c_real_spin.hide()  # Hide initially
        self.params_fractal_layout.addRow("Julia c (real):", self.julia_c_real_spin)

        self.julia_c_imag_spin = QDoubleSpinBox()
        self.julia_c_imag_spin.setRange(-2.0, 2.0)
        self.julia_c_imag_spin.setValue(0.27)
        self.julia_c_imag_spin.setSingleStep(0.05)
        self.julia_c_imag_spin.hide()  # Hide initially
        self.params_fractal_layout.addRow("Julia c (imag):", self.julia_c_imag_spin)

        # Visualization parameters
        self.color_scheme_fractal_combo = QComboBox()
        self.color_scheme_fractal_combo.addItems(["rainbow", "golden", "monochrome", "custom"])
        self.params_fractal_layout.addRow("Color Scheme:", self.color_scheme_fractal_combo)

        self.params_fractal_group.setLayout(self.params_fractal_layout)
        layout.addWidget(self.params_fractal_group)

        # Generate button
        self.generate_fractal_button = QPushButton("Generate Fractal")
        self.generate_fractal_button.clicked.connect(self.generate_output)
        layout.addWidget(self.generate_fractal_button)

        # Add stretch to push everything to the top
        layout.addStretch()

        self.tab_fractals.setLayout(layout)

    def setup_animations_tab(self):
        """Set up the animations tab."""
        layout = QVBoxLayout()

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
        self.color_scheme_anim_combo.addItems(["rainbow", "golden", "monochrome", "custom"])
        self.params_animation_layout.addRow("Color Scheme:", self.color_scheme_anim_combo)

        self.params_animation_group.setLayout(self.params_animation_layout)
        layout.addWidget(self.params_animation_group)

        # Generate button
        self.generate_animation_button = QPushButton("Generate Animation")
        self.generate_animation_button.clicked.connect(self.generate_animation)
        layout.addWidget(self.generate_animation_button)

        # Add stretch to push everything to the top
        layout.addStretch()

        self.tab_animations.setLayout(layout)

    def setup_custom_tab(self):
        """Set up the custom tab for combined patterns."""
        layout = QVBoxLayout()

        # Custom pattern selection
        custom_group = QGroupBox("Custom Pattern Selection")
        custom_layout = QFormLayout()

        self.custom_combo = QComboBox()
        self.custom_combo.addItems([
            "Flower of Life with Fibonacci Spiral",
            "Sacred Geometry Mandala",
            "Metatron's Cube with Platonic Projections",
            "Fractal Tree with Golden Ratio",
            "Nested Platonic Solids"
        ])
        self.custom_combo.currentTextChanged.connect(self.on_custom_changed)
        custom_layout.addRow("Custom Pattern:", self.custom_combo)

        custom_group.setLayout(custom_layout)
        layout.addWidget(custom_group)

        # Custom parameters
        self.params_custom_group = QGroupBox("Custom Parameters")
        self.params_custom_layout = QFormLayout()

        # Common parameters
        self.custom_radius_spin = QDoubleSpinBox()
        self.custom_radius_spin.setRange(0.1, 5.0)
        self.custom_radius_spin.setValue(1.0)
        self.custom_radius_spin.setSingleStep(0.1)
        self.params_custom_layout.addRow("Radius:", self.custom_radius_spin)

        # Visualization parameters
        self.color_scheme_custom_combo = QComboBox()
        self.color_scheme_custom_combo.addItems(["rainbow", "golden", "monochrome", "custom"])
        self.params_custom_layout.addRow("Color Scheme:", self.color_scheme_custom_combo)

        self.params_custom_group.setLayout(self.params_custom_layout)
        layout.addWidget(self.params_custom_group)

        # Generate button
        self.generate_custom_button = QPushButton("Generate Custom Pattern")
        self.generate_custom_button.clicked.connect(self.generate_custom_output)
        layout.addWidget(self.generate_custom_button)

        # Add stretch to push everything to the top
        layout.addStretch()

        self.tab_custom.setLayout(layout)

    def on_tab_changed(self, index):
        """Handle tab change event."""
        tab_names = ["2D Patterns", "3D Shapes", "Fractals", "Animations", "Custom"]
        self.current_category = tab_names[index]

        # Update the current pattern based on the selected tab
        if index == 0:  # 2D Patterns
            self.current_pattern = self.pattern_2d_combo.currentText()
            self.canvas.set_2d_axes()
        elif index == 1:  # 3D Shapes
            self.current_pattern = self.shape_3d_combo.currentText()
            self.canvas.set_3d_axes()
        elif index == 2:  # Fractals
            self.current_pattern = self.fractal_combo.currentText()
            self.canvas.set_2d_axes()
        elif index == 3:  # Animations
            self.current_pattern = self.animation_combo.currentText()
            self.canvas.set_2d_axes()
        elif index == 4:  # Custom
            self.current_pattern = self.custom_combo.currentText()
            self.canvas.set_2d_axes()

        # Generate the output for the new tab
        self.generate_output()

    def on_2d_pattern_changed(self, pattern_name):
        """Handle 2D pattern selection change."""
        self.current_pattern = pattern_name

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

        # Show/hide fractal-specific parameters
        if fractal_name == "Fractal Tree":
            self.angle_spin.show()
            self.length_factor_spin.show()
            self.turns_spin.hide()
            self.max_iter_spin.hide()
            self.julia_c_real_spin.hide()
            self.julia_c_imag_spin.hide()
        elif fractal_name == "Sacred Spiral":
            self.angle_spin.hide()
            self.length_factor_spin.hide()
            self.turns_spin.show()
            self.max_iter_spin.hide()
            self.julia_c_real_spin.hide()
            self.julia_c_imag_spin.hide()
        elif fractal_name in ["Mandelbrot Set", "Julia Set"]:
            self.angle_spin.hide()
            self.length_factor_spin.hide()
            self.turns_spin.hide()
            self.max_iter_spin.show()
            if fractal_name == "Julia Set":
                self.julia_c_real_spin.show()
                self.julia_c_imag_spin.show()
            else:
                self.julia_c_real_spin.hide()
                self.julia_c_imag_spin.hide()
        else:
            self.angle_spin.hide()
            self.length_factor_spin.hide()
            self.turns_spin.hide()
            self.max_iter_spin.hide()
            self.julia_c_real_spin.hide()
            self.julia_c_imag_spin.hide()

        # Update the UI
        self.generate_output()

    def on_animation_changed(self, animation_name):
        """Handle animation selection change."""
        self.current_pattern = animation_name

    def on_custom_changed(self, custom_name):
        """Handle custom pattern selection change."""
        self.current_pattern = custom_name

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
            elif self.current_category == "Custom":
                self.generate_custom_output()

            self.canvas.draw()
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Error generating output: {str(e)}")

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

        # Plot the shape
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
        color_scheme = self.color_scheme_fractal_combo.currentText().lower()

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

        elif self.current_pattern == "Mandelbrot Set":
            max_iter = self.max_iter_spin.value()

            # Generate Mandelbrot set
            xmin, xmax = -2.0, 1.0
            ymin, ymax = -1.5, 1.5
            width, height = 800, 800

            mandelbrot = mandelbrot_set(
                xmin=xmin, xmax=xmax,
                ymin=ymin, ymax=ymax,
                width=width, height=height,
                max_iter=max_iter
            )

            # Plot as an image
            img = self.canvas.axes.imshow(
                mandelbrot,
                extent=[xmin, xmax, ymin, ymax],
                cmap='hot',
                origin='lower'
            )

            self.canvas.fig.colorbar(img, ax=self.canvas.axes)
            self.canvas.axes.set_title("Mandelbrot Set")

        elif self.current_pattern == "Julia Set":
            max_iter = self.max_iter_spin.value()
            c_real = self.julia_c_real_spin.value()
            c_imag = self.julia_c_imag_spin.value()

            # Generate Julia set
            xmin, xmax = -1.5, 1.5
            ymin, ymax = -1.5, 1.5
            width, height = 800, 800

            julia = julia_set(
                c=complex(c_real, c_imag),
                xmin=xmin, xmax=xmax,
                ymin=ymin, ymax=ymax,
                width=width, height=height,
                max_iter=max_iter
            )

            # Plot as an image
            img = self.canvas.axes.imshow(
                julia,
                extent=[xmin, xmax, ymin, ymax],
                cmap='hot',
                origin='lower'
            )

            self.canvas.fig.colorbar(img, ax=self.canvas.axes)
            self.canvas.axes.set_title(f"Julia Set (c={c_real}+{c_imag}i)")

    def generate_custom_output(self):
        """Generate a custom pattern based on current settings."""
        # Get common parameters
        radius = self.custom_radius_spin.value()
        color_scheme = self.color_scheme_custom_combo.currentText().lower()

        if self.current_pattern == "Flower of Life with Fibonacci Spiral":
            # Create Flower of Life
            flower = create_flower_of_life(center=(0, 0), radius=radius, layers=3)
            for circle in flower:
                self.canvas.axes.plot(circle[:, 0], circle[:, 1], 'b-', alpha=0.3, linewidth=1)

            # Create Fibonacci Spiral
            fibonacci = create_fibonacci_spiral(center=(0, 0), scale=radius/10, n_iterations=10)
            self.canvas.axes.plot(fibonacci['spiral'][:, 0], fibonacci['spiral'][:, 1], 'r-', linewidth=2)

            self.canvas.axes.set_title("Flower of Life with Fibonacci Spiral")
            self.canvas.axes.set_aspect('equal')
            self.canvas.axes.set_xlim(-4*radius, 4*radius)
            self.canvas.axes.set_ylim(-4*radius, 4*radius)

        elif self.current_pattern == "Sacred Geometry Mandala":
            # Create multiple layers of polygons with different rotations
            phi = get_golden_ratio()
            colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b']

            # Layer 1: Hexagon
            hexagon = create_regular_polygon(center=(0, 0), radius=3.0*radius, sides=6)
            self.canvas.axes.plot(np.append(hexagon[:, 0], hexagon[0, 0]),
                                np.append(hexagon[:, 1], hexagon[0, 1]),
                                '-', color=colors[0], linewidth=2)

            # Layer 2: Pentagon
            pentagon = create_regular_polygon(center=(0, 0), radius=2.5*radius, sides=5, rotation=np.pi/5)
            self.canvas.axes.plot(np.append(pentagon[:, 0], pentagon[0, 0]),
                                np.append(pentagon[:, 1], pentagon[0, 1]),
                                '-', color=colors[1], linewidth=2)

            # Layer 3: Heptagon (7 sides)
            heptagon = create_regular_polygon(center=(0, 0), radius=2.0*radius, sides=7, rotation=np.pi/7)
            self.canvas.axes.plot(np.append(heptagon[:, 0], heptagon[0, 0]),
                                np.append(heptagon[:, 1], heptagon[0, 1]),
                                '-', color=colors[2], linewidth=2)

            # Layer 4: Triangle
            triangle = create_regular_polygon(center=(0, 0), radius=1.5*radius, sides=3, rotation=np.pi/6)
            self.canvas.axes.plot(np.append(triangle[:, 0], triangle[0, 0]),
                                np.append(triangle[:, 1], triangle[0, 1]),
                                '-', color=colors[3], linewidth=2)

            # Layer 5: Square
            square = create_regular_polygon(center=(0, 0), radius=1.0*radius, sides=4, rotation=np.pi/4)
            self.canvas.axes.plot(np.append(square[:, 0], square[0, 0]),
                                np.append(square[:, 1], square[0, 1]),
                                '-', color=colors[4], linewidth=2)

            # Layer 6: Center circle
            circle = create_regular_polygon(center=(0, 0), radius=0.5*radius, sides=36)
            self.canvas.axes.plot(np.append(circle[:, 0], circle[0, 0]),
                                np.append(circle[:, 1], circle[0, 1]),
                                '-', color=colors[5], linewidth=2)

            # Add connecting lines
            for i in range(6):
                angle = i * np.pi / 3
                x = 3.0 * radius * np.cos(angle)
                y = 3.0 * radius * np.sin(angle)
                self.canvas.axes.plot([0, x], [0, y], 'k-', alpha=0.5, linewidth=1)

            self.canvas.axes.set_title("Sacred Geometry Mandala")
            self.canvas.axes.set_aspect('equal')
            self.canvas.axes.set_xlim(-3.5*radius, 3.5*radius)
            self.canvas.axes.set_ylim(-3.5*radius, 3.5*radius)
            self.canvas.axes.axis('off')

        elif self.current_pattern == "Metatron's Cube with Platonic Projections":
            # Create Metatron's Cube
            metatron = create_metatrons_cube(center=(0, 0), radius=radius)

            # Draw circles
            for circle in metatron['circles']:
                self.canvas.axes.plot(circle[:, 0], circle[:, 1], 'b-', alpha=0.3, linewidth=1)

            # Draw lines
            for line in metatron['lines']:
                self.canvas.axes.plot([line[0][0], line[1][0]], [line[0][1], line[1][1]],
                                    'k-', linewidth=0.5, alpha=0.7)

            # Draw vertices
            vertices = np.array(metatron['vertices'])
            self.canvas.axes.scatter(vertices[:, 0], vertices[:, 1], color='red', s=30)

            # Project platonic solids onto the 2D plane
            # Tetrahedron projection (simplified)
            tetra_edges = [(0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3)]
            for edge in tetra_edges:
                if edge[0] < len(vertices) and edge[1] < len(vertices):
                    self.canvas.axes.plot([vertices[edge[0], 0], vertices[edge[1], 0]],
                                        [vertices[edge[0], 1], vertices[edge[1], 1]],
                                        'r-', linewidth=1.5, alpha=0.7)

            # Cube projection (simplified)
            cube_edges = [(1, 2), (1, 3), (2, 4), (3, 4), (5, 6), (5, 7), (6, 8), (7, 8)]
            for edge in cube_edges:
                if edge[0] < len(vertices) and edge[1] < len(vertices):
                    self.canvas.axes.plot([vertices[edge[0], 0], vertices[edge[1], 0]],
                                        [vertices[edge[0], 1], vertices[edge[1], 1]],
                                        'g-', linewidth=1.5, alpha=0.7)

            self.canvas.axes.set_title("Metatron's Cube with Platonic Projections")
            self.canvas.axes.set_aspect('equal')
            self.canvas.axes.set_xlim(-3*radius, 3*radius)
            self.canvas.axes.set_ylim(-3*radius, 3*radius)

        elif self.current_pattern == "Fractal Tree with Golden Ratio":
            # Golden ratio
            phi = get_golden_ratio()

            # Create a fractal tree with golden ratio proportions
            tree_branches = fractal_tree(
                start=(0, -3*radius),
                angle=np.pi/2,  # Initial angle (pointing up)
                length=3.0*radius,  # Initial branch length
                depth=8,  # Recursion depth
                length_factor=1/phi,  # Golden ratio reduction
                angle_delta=np.pi/phi  # Golden angle
            )

            # Create a custom colormap for the branches
            from matplotlib.colors import LinearSegmentedColormap
            colors = [(0.6, 0.3, 0.1), (0.2, 0.8, 0.2)]  # Brown to green
            cmap = LinearSegmentedColormap.from_list("BrownToGreen", colors, N=len(tree_branches))

            # Plot each branch with a color based on its depth
            for i, branch in enumerate(tree_branches):
                color = cmap(i / len(tree_branches))
                self.canvas.axes.plot(branch[:, 0], branch[:, 1], color=color,
                                    linewidth=max(0.5, 3 * (1 - i/len(tree_branches))))

            self.canvas.axes.set_title("Fractal Tree with Golden Ratio Proportions")
            self.canvas.axes.set_aspect('equal')
            self.canvas.axes.set_xlim(-5*radius, 5*radius)
            self.canvas.axes.set_ylim(-3*radius, 7*radius)
            self.canvas.axes.axis('off')

        elif self.current_pattern == "Nested Platonic Solids":
            # Create a 3D axes
            self.canvas.set_3d_axes()

            # Golden ratio
            phi = get_golden_ratio()

            # Create nested platonic solids with golden ratio scaling
            tetra = create_tetrahedron(radius=radius)
            plot_3d_shape(tetra, color_scheme="custom", custom_color='red',
                         alpha=0.4, ax=self.canvas.axes)

            cube = create_cube(radius=radius * phi)
            plot_3d_shape(cube, color_scheme="custom", custom_color='blue',
                         alpha=0.3, ax=self.canvas.axes)

            octa = create_octahedron(radius=radius * phi * phi)
            plot_3d_shape(octa, color_scheme="custom", custom_color='green',
                         alpha=0.3, ax=self.canvas.axes)

            icosa = create_icosahedron(radius=radius * phi * phi * phi)
            plot_3d_shape(icosa, color_scheme="custom", custom_color='purple',
                         alpha=0.2, ax=self.canvas.axes)

            self.canvas.axes.set_title("Nested Platonic Solids (Golden Ratio Scaling)")

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

                # Animation function
                def update(frame):
                    ax.clear()
                    ax.set_aspect('equal')
                    ax.set_title("Growing Flower of Life")
                    ax.set_xlim(-4*radius, 4*radius)
                    ax.set_ylim(-4*radius, 4*radius)
                    ax.grid(True, linestyle='--', alpha=0.7)

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
                anim.save(filename, writer='pillow', fps=fps)
                plt.close(fig)

                QMessageBox.information(self, "Animation Complete",
                                      f"Animation saved to {filename}")

            elif self.current_pattern == "Rotating Merkaba":
                # Create figure for animation
                fig = plt.figure(figsize=(10, 10))
                ax = fig.add_subplot(111, projection='3d')

                # Animation function
                def update(frame):
                    ax.clear()
                    ax.set_title("Rotating Merkaba")

                    # Calculate rotation based on frame
                    rotation = frame / frames * 2 * np.pi

                    # Create merkaba with current rotation
                    merkaba = create_merkaba(center=(0, 0, 0), radius=radius, rotation=rotation)

                    # Plot the merkaba
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
                anim.save(filename, writer='pillow', fps=fps)
                plt.close(fig)

                QMessageBox.information(self, "Animation Complete",
                                      f"Animation saved to {filename}")

            # Add other animations as needed...

        except Exception as e:
            QMessageBox.warning(self, "Error", f"Error generating animation: {str(e)}")

    def save_output(self):
        """Save the current output to a file."""
        # Get the current pattern name for the default filename
        pattern_name = self.current_pattern.lower().replace(" ", "_").replace("'", "")

        # Get the appropriate directory based on the current category
        if self.current_category == "2D Patterns":
            directory = output_dirs['2d']
        elif self.current_category == "3D Shapes":
            directory = output_dirs['3d']
        elif self.current_category == "Fractals":
            directory = output_dirs['fractals']
        elif self.current_category == "Custom":
            directory = output_dirs['custom']
        else:
            directory = "outputs"

        # Create the directory if it doesn't exist
        os.makedirs(directory, exist_ok=True)

        # Get the default filepath
        default_filepath = os.path.join(directory, f"{pattern_name}.png")

        # Open file dialog
        filepath, _ = QFileDialog.getSaveFileName(
            self, "Save Output", default_filepath, "PNG Files (*.png);;All Files (*)"
        )

        if filepath:
            try:
                # Save the figure
                self.canvas.fig.savefig(filepath, dpi=300, bbox_inches='tight')
                QMessageBox.information(self, "Save Complete", f"Output saved to {filepath}")
            except Exception as e:
                QMessageBox.warning(self, "Error", f"Error saving output: {str(e)}")

def main():
    """Main function to run the application."""
    app = QApplication(sys.argv)
    window = SacredGeometryGUI()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
