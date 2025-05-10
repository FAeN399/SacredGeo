"""
Enhanced Sacred Geometry GUI Application

A comprehensive graphical user interface for generating and visualizing
sacred geometry patterns, shapes, and animations with an esoteric aesthetic
and advanced 3D visualization capabilities.
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
    QFormLayout, QSplitter, QFrame, QMessageBox, QRadioButton, QButtonGroup,
    QSizePolicy, QGridLayout, QToolBar, QAction, QStatusBar, QScrollArea,
    QDial, QProgressBar
)
from PyQt5.QtCore import Qt, QTimer, QSize, pyqtSignal, QThread
from PyQt5.QtGui import QColor, QPixmap, QIcon, QFont, QPalette, QLinearGradient, QGradient

# Try to import PyOpenGL for enhanced 3D rendering
try:
    from PyQt5.QtDataVisualization import (
        Q3DScatter, QScatter3DSeries, QScatterDataItem, QScatterDataProxy,
        Q3DTheme, QAbstract3DGraph
    )
    from PyQt5.Qt3DCore import QEntity, QTransform
    from PyQt5.Qt3DRender import QMesh, QMaterial
    from PyQt5.Qt3DExtras import (
        Qt3DWindow, QForwardRenderer, QPhongMaterial,
        QCylinderMesh, QSphereMesh, QTorusMesh, QConeMesh
    )
    OPENGL_AVAILABLE = True
except ImportError:
    OPENGL_AVAILABLE = False
    print("PyQt3D not available. Falling back to Matplotlib for 3D visualization.")

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
    """Enhanced main window for the Sacred Geometry GUI application."""

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
        self.control_panel = QScrollArea()
        self.control_panel.setWidgetResizable(True)
        self.control_panel.setMinimumWidth(350)
        self.control_panel.setMaximumWidth(450)

        self.control_widget = QTabWidget()
        self.setup_control_panel()
        self.control_panel.setWidget(self.control_widget)

        # Create the visualization panel
        self.viz_panel = QWidget()
        self.setup_viz_panel()

        # Add widgets to splitter
        self.splitter.addWidget(self.control_panel)
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
            with open("sacred_geometry_style.qss", "r") as f:
                style = f.read()
                self.setStyleSheet(style)
        except FileNotFoundError:
            print("Style sheet file not found. Using default style.")

    def setup_toolbar(self):
        """Set up the main toolbar."""
        # Save action
        save_action = QAction(QIcon(), "Save", self)
        save_action.triggered.connect(self.save_output)
        self.toolbar.addAction(save_action)

        # Export action
        export_action = QAction(QIcon(), "Export", self)
        export_action.triggered.connect(self.export_output)
        self.toolbar.addAction(export_action)

        self.toolbar.addSeparator()

        # Gallery action
        gallery_action = QAction(QIcon(), "Gallery", self)
        gallery_action.triggered.connect(self.open_gallery)
        self.toolbar.addAction(gallery_action)

        # Settings action
        settings_action = QAction(QIcon(), "Settings", self)
        settings_action.triggered.connect(self.open_settings)
        self.toolbar.addAction(settings_action)

        self.toolbar.addSeparator()

        # Help action
        help_action = QAction(QIcon(), "Help", self)
        help_action.triggered.connect(self.show_help)
        self.toolbar.addAction(help_action)

    def setup_control_panel(self):
        """Set up the control panel with tabs for different categories."""
        # Create tabs for different categories
        self.tab_2d = QWidget()
        self.tab_3d = QWidget()
        self.tab_fractals = QWidget()
        self.tab_animations = QWidget()
        self.tab_custom = QWidget()

        # Add tabs to the control panel
        self.control_widget.addTab(self.tab_2d, "2D Patterns")
        self.control_widget.addTab(self.tab_3d, "3D Shapes")
        self.control_widget.addTab(self.tab_fractals, "Fractals")
        self.control_widget.addTab(self.tab_animations, "Animations")
        self.control_widget.addTab(self.tab_custom, "Custom")

        # Connect tab change signal
        self.control_widget.currentChanged.connect(self.on_tab_changed)

        # Set up each tab
        self.setup_2d_tab()
        self.setup_3d_tab()
        self.setup_fractals_tab()
        self.setup_animations_tab()
        self.setup_custom_tab()

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

        # Add rotation slider
        self.rotation_3d_slider = QSlider(Qt.Horizontal)
        self.rotation_3d_slider.setRange(0, 360)
        self.rotation_3d_slider.setValue(45)
        self.rotation_3d_slider.valueChanged.connect(lambda v: self.rotation_3d_spin.setValue(v * np.pi / 180))
        self.rotation_3d_spin.valueChanged.connect(lambda v: self.rotation_3d_slider.setValue(int(v * 180 / np.pi)))
        self.rotation_3d_slider.hide()  # Hide initially
        self.params_3d_layout.addRow("", self.rotation_3d_slider)

        # Torus specific parameters
        self.major_radius_spin = QDoubleSpinBox()
        self.major_radius_spin.setRange(0.5, 5.0)
        self.major_radius_spin.setValue(2.0)
        self.major_radius_spin.setSingleStep(0.1)
        self.major_radius_spin.hide()  # Hide initially
        self.params_3d_layout.addRow("Major Radius:", self.major_radius_spin)

        # Add major radius slider
        self.major_radius_slider = QSlider(Qt.Horizontal)
        self.major_radius_slider.setRange(5, 50)
        self.major_radius_slider.setValue(20)
        self.major_radius_slider.valueChanged.connect(lambda v: self.major_radius_spin.setValue(v/10))
        self.major_radius_spin.valueChanged.connect(lambda v: self.major_radius_slider.setValue(int(v*10)))
        self.major_radius_slider.hide()  # Hide initially
        self.params_3d_layout.addRow("", self.major_radius_slider)

        self.minor_radius_spin = QDoubleSpinBox()
        self.minor_radius_spin.setRange(0.1, 2.0)
        self.minor_radius_spin.setValue(0.5)
        self.minor_radius_spin.setSingleStep(0.1)
        self.minor_radius_spin.hide()  # Hide initially
        self.params_3d_layout.addRow("Minor Radius:", self.minor_radius_spin)

        # Add minor radius slider
        self.minor_radius_slider = QSlider(Qt.Horizontal)
        self.minor_radius_slider.setRange(1, 20)
        self.minor_radius_slider.setValue(5)
        self.minor_radius_slider.valueChanged.connect(lambda v: self.minor_radius_spin.setValue(v/10))
        self.minor_radius_spin.valueChanged.connect(lambda v: self.minor_radius_slider.setValue(int(v*10)))
        self.minor_radius_slider.hide()  # Hide initially
        self.params_3d_layout.addRow("", self.minor_radius_slider)

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

        # Material options
        self.material_combo = QComboBox()
        self.material_combo.addItems(["Matte", "Metallic", "Glass", "Crystal"])
        self.params_3d_layout.addRow("Material:", self.material_combo)

        self.alpha_3d_spin = QDoubleSpinBox()
        self.alpha_3d_spin.setRange(0.1, 1.0)
        self.alpha_3d_spin.setValue(0.7)
        self.alpha_3d_spin.setSingleStep(0.1)
        self.params_3d_layout.addRow("Transparency:", self.alpha_3d_spin)

        # Add alpha slider
        self.alpha_3d_slider = QSlider(Qt.Horizontal)
        self.alpha_3d_slider.setRange(1, 10)
        self.alpha_3d_slider.setValue(7)
        self.alpha_3d_slider.valueChanged.connect(lambda v: self.alpha_3d_spin.setValue(v/10))
        self.alpha_3d_spin.valueChanged.connect(lambda v: self.alpha_3d_slider.setValue(int(v*10)))
        self.params_3d_layout.addRow("", self.alpha_3d_slider)

        self.show_edges_check = QCheckBox()
        self.show_edges_check.setChecked(True)
        self.params_3d_layout.addRow("Show Edges:", self.show_edges_check)

        self.show_vertices_check = QCheckBox()
        self.show_vertices_check.setChecked(True)
        self.params_3d_layout.addRow("Show Vertices:", self.show_vertices_check)

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

        # Add size slider
        self.size_slider = QSlider(Qt.Horizontal)
        self.size_slider.setRange(1, 100)
        self.size_slider.setValue(10)
        self.size_slider.valueChanged.connect(lambda v: self.size_spin.setValue(v/10))
        self.size_spin.valueChanged.connect(lambda v: self.size_slider.setValue(int(v*10)))
        self.params_fractal_layout.addRow("", self.size_slider)

        # Fractal Tree specific parameters
        self.angle_spin = QDoubleSpinBox()
        self.angle_spin.setRange(0, np.pi)
        self.angle_spin.setValue(np.pi/7)
        self.angle_spin.setSingleStep(np.pi/36)
        self.angle_spin.hide()  # Hide initially
        self.params_fractal_layout.addRow("Angle Delta:", self.angle_spin)

        # Add angle slider
        self.angle_slider = QSlider(Qt.Horizontal)
        self.angle_slider.setRange(0, 180)
        self.angle_slider.setValue(int(180/7))
        self.angle_slider.valueChanged.connect(lambda v: self.angle_spin.setValue(v * np.pi / 180))
        self.angle_spin.valueChanged.connect(lambda v: self.angle_slider.setValue(int(v * 180 / np.pi)))
        self.angle_slider.hide()  # Hide initially
        self.params_fractal_layout.addRow("", self.angle_slider)

        self.length_factor_spin = QDoubleSpinBox()
        self.length_factor_spin.setRange(0.1, 0.9)
        self.length_factor_spin.setValue(0.7)
        self.length_factor_spin.setSingleStep(0.05)
        self.length_factor_spin.hide()  # Hide initially
        self.params_fractal_layout.addRow("Length Factor:", self.length_factor_spin)

        # Add length factor slider
        self.length_factor_slider = QSlider(Qt.Horizontal)
        self.length_factor_slider.setRange(1, 9)
        self.length_factor_slider.setValue(7)
        self.length_factor_slider.valueChanged.connect(lambda v: self.length_factor_spin.setValue(v/10))
        self.length_factor_spin.valueChanged.connect(lambda v: self.length_factor_slider.setValue(int(v*10)))
        self.length_factor_slider.hide()  # Hide initially
        self.params_fractal_layout.addRow("", self.length_factor_slider)

        # Sacred Spiral specific parameters
        self.turns_spin = QDoubleSpinBox()
        self.turns_spin.setRange(1, 20)
        self.turns_spin.setValue(5)
        self.turns_spin.setSingleStep(1)
        self.turns_spin.hide()  # Hide initially
        self.params_fractal_layout.addRow("Turns:", self.turns_spin)

        # Add turns slider
        self.turns_slider = QSlider(Qt.Horizontal)
        self.turns_slider.setRange(1, 20)
        self.turns_slider.setValue(5)
        self.turns_slider.valueChanged.connect(self.turns_spin.setValue)
        self.turns_spin.valueChanged.connect(lambda v: self.turns_slider.setValue(int(v)))
        self.turns_slider.hide()  # Hide initially
        self.params_fractal_layout.addRow("", self.turns_slider)

        # Mandelbrot/Julia specific parameters
        self.max_iter_spin = QSpinBox()
        self.max_iter_spin.setRange(10, 1000)
        self.max_iter_spin.setValue(100)
        self.max_iter_spin.setSingleStep(10)
        self.max_iter_spin.hide()  # Hide initially
        self.params_fractal_layout.addRow("Max Iterations:", self.max_iter_spin)

        # Add max iterations slider
        self.max_iter_slider = QSlider(Qt.Horizontal)
        self.max_iter_slider.setRange(10, 1000)
        self.max_iter_slider.setValue(100)
        self.max_iter_slider.valueChanged.connect(self.max_iter_spin.setValue)
        self.max_iter_spin.valueChanged.connect(self.max_iter_slider.setValue)
        self.max_iter_slider.hide()  # Hide initially
        self.params_fractal_layout.addRow("", self.max_iter_slider)

        self.julia_c_real_spin = QDoubleSpinBox()
        self.julia_c_real_spin.setRange(-2.0, 2.0)
        self.julia_c_real_spin.setValue(-0.7)
        self.julia_c_real_spin.setSingleStep(0.05)
        self.julia_c_real_spin.hide()  # Hide initially
        self.params_fractal_layout.addRow("Julia c (real):", self.julia_c_real_spin)

        # Add julia c real slider
        self.julia_c_real_slider = QSlider(Qt.Horizontal)
        self.julia_c_real_slider.setRange(-200, 200)
        self.julia_c_real_slider.setValue(-70)
        self.julia_c_real_slider.valueChanged.connect(lambda v: self.julia_c_real_spin.setValue(v/100))
        self.julia_c_real_spin.valueChanged.connect(lambda v: self.julia_c_real_slider.setValue(int(v*100)))
        self.julia_c_real_slider.hide()  # Hide initially
        self.params_fractal_layout.addRow("", self.julia_c_real_slider)

        self.julia_c_imag_spin = QDoubleSpinBox()
        self.julia_c_imag_spin.setRange(-2.0, 2.0)
        self.julia_c_imag_spin.setValue(0.27)
        self.julia_c_imag_spin.setSingleStep(0.05)
        self.julia_c_imag_spin.hide()  # Hide initially
        self.params_fractal_layout.addRow("Julia c (imag):", self.julia_c_imag_spin)

        # Add julia c imag slider
        self.julia_c_imag_slider = QSlider(Qt.Horizontal)
        self.julia_c_imag_slider.setRange(-200, 200)
        self.julia_c_imag_slider.setValue(27)
        self.julia_c_imag_slider.valueChanged.connect(lambda v: self.julia_c_imag_spin.setValue(v/100))
        self.julia_c_imag_spin.valueChanged.connect(lambda v: self.julia_c_imag_slider.setValue(int(v*100)))
        self.julia_c_imag_slider.hide()  # Hide initially
        self.params_fractal_layout.addRow("", self.julia_c_imag_slider)

        # Visualization parameters
        self.color_scheme_fractal_combo = QComboBox()
        self.color_scheme_fractal_combo.addItems(["rainbow", "golden", "monochrome", "custom", "fire", "ice", "earth"])
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
            "Metatron's Cube Formation", "Koch Snowflake Evolution",
            "Platonic Solid Morphing", "Golden Ratio Spiral"
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

        # Add fps slider
        self.fps_slider = QSlider(Qt.Horizontal)
        self.fps_slider.setRange(5, 30)
        self.fps_slider.setValue(15)
        self.fps_slider.valueChanged.connect(self.fps_spin.setValue)
        self.fps_spin.valueChanged.connect(self.fps_slider.setValue)
        self.params_animation_layout.addRow("", self.fps_slider)

        # Animation specific parameters
        self.anim_radius_spin = QDoubleSpinBox()
        self.anim_radius_spin.setRange(0.1, 5.0)
        self.anim_radius_spin.setValue(1.0)
        self.anim_radius_spin.setSingleStep(0.1)
        self.params_animation_layout.addRow("Radius:", self.anim_radius_spin)

        # Add radius slider
        self.anim_radius_slider = QSlider(Qt.Horizontal)
        self.anim_radius_slider.setRange(1, 50)
        self.anim_radius_slider.setValue(10)
        self.anim_radius_slider.valueChanged.connect(lambda v: self.anim_radius_spin.setValue(v/10))
        self.anim_radius_spin.valueChanged.connect(lambda v: self.anim_radius_slider.setValue(int(v*10)))
        self.params_animation_layout.addRow("", self.anim_radius_slider)

        self.anim_max_layers_spin = QSpinBox()
        self.anim_max_layers_spin.setRange(1, 5)
        self.anim_max_layers_spin.setValue(3)
        self.params_animation_layout.addRow("Max Layers:", self.anim_max_layers_spin)

        # Add max layers slider
        self.anim_max_layers_slider = QSlider(Qt.Horizontal)
        self.anim_max_layers_slider.setRange(1, 5)
        self.anim_max_layers_slider.setValue(3)
        self.anim_max_layers_slider.valueChanged.connect(self.anim_max_layers_spin.setValue)
        self.anim_max_layers_spin.valueChanged.connect(self.anim_max_layers_slider.setValue)
        self.params_animation_layout.addRow("", self.anim_max_layers_slider)

        # Visualization parameters
        self.color_scheme_anim_combo = QComboBox()
        self.color_scheme_anim_combo.addItems(["rainbow", "golden", "monochrome", "custom", "fire", "ice", "earth"])
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

    def setup_custom_tab(self):
        """Set up the custom tab for combined patterns."""
        layout = QVBoxLayout()

        # Add title
        title_label = QLabel("Custom Sacred Geometry Compositions")
        title_label.setObjectName("titleLabel")
        title_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(title_label)

        # Custom pattern selection
        custom_group = QGroupBox("Composition Selection")
        custom_layout = QFormLayout()

        self.custom_combo = QComboBox()
        self.custom_combo.addItems([
            "Flower of Life with Fibonacci Spiral",
            "Sacred Geometry Mandala",
            "Metatron's Cube with Platonic Projections",
            "Fractal Tree with Golden Ratio",
            "Nested Platonic Solids",
            "Cosmic Torus with Merkaba",
            "Tree of Life Template"
        ])
        self.custom_combo.currentTextChanged.connect(self.on_custom_changed)
        custom_layout.addRow("Composition:", self.custom_combo)

        custom_group.setLayout(custom_layout)
        layout.addWidget(custom_group)

        # Custom parameters
        self.params_custom_group = QGroupBox("Composition Parameters")
        self.params_custom_layout = QFormLayout()

        # Common parameters
        self.custom_radius_spin = QDoubleSpinBox()
        self.custom_radius_spin.setRange(0.1, 5.0)
        self.custom_radius_spin.setValue(1.0)
        self.custom_radius_spin.setSingleStep(0.1)
        self.params_custom_layout.addRow("Base Radius:", self.custom_radius_spin)

        # Add radius slider
        self.custom_radius_slider = QSlider(Qt.Horizontal)
        self.custom_radius_slider.setRange(1, 50)
        self.custom_radius_slider.setValue(10)
        self.custom_radius_slider.valueChanged.connect(lambda v: self.custom_radius_spin.setValue(v/10))
        self.custom_radius_spin.valueChanged.connect(lambda v: self.custom_radius_slider.setValue(int(v*10)))
        self.params_custom_layout.addRow("", self.custom_radius_slider)

        # Complexity parameter
        self.complexity_spin = QSpinBox()
        self.complexity_spin.setRange(1, 5)
        self.complexity_spin.setValue(3)
        self.params_custom_layout.addRow("Complexity:", self.complexity_spin)

        # Add complexity slider
        self.complexity_slider = QSlider(Qt.Horizontal)
        self.complexity_slider.setRange(1, 5)
        self.complexity_slider.setValue(3)
        self.complexity_slider.valueChanged.connect(self.complexity_spin.setValue)
        self.complexity_spin.valueChanged.connect(self.complexity_slider.setValue)
        self.params_custom_layout.addRow("", self.complexity_slider)

        # Dimension selection
        self.dimension_combo = QComboBox()
        self.dimension_combo.addItems(["2D", "3D"])
        self.params_custom_layout.addRow("Dimension:", self.dimension_combo)

        # Visualization parameters
        self.color_scheme_custom_combo = QComboBox()
        self.color_scheme_custom_combo.addItems(["rainbow", "golden", "monochrome", "custom", "fire", "ice", "earth"])
        self.params_custom_layout.addRow("Color Scheme:", self.color_scheme_custom_combo)

        # Custom color picker button
        self.color_picker_button = QPushButton("Pick Custom Colors")
        self.color_picker_button.clicked.connect(self.pick_custom_colors)
        self.params_custom_layout.addRow("", self.color_picker_button)

        self.params_custom_group.setLayout(self.params_custom_layout)
        layout.addWidget(self.params_custom_group)

        # Generate button
        self.generate_custom_button = QPushButton("Generate Composition")
        self.generate_custom_button.setObjectName("generateButton")
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
        elif index == 4:  # Custom
            self.current_pattern = self.custom_combo.currentText()
            if self.dimension_combo.currentText() == "3D":
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

    def on_2d_pattern_changed(self, pattern_name):
        """Handle 2D pattern selection change."""
        self.current_pattern = pattern_name
        self.title_label.setText(f"Sacred Geometry Explorer - {pattern_name}")

        # Show/hide pattern-specific parameters
        if pattern_name == "Regular Polygon":
            self.sides_spin.show()
            self.rotation_2d_spin.show()
            self.rotation_2d_slider.show()
        else:
            self.sides_spin.hide()
            self.rotation_2d_spin.hide()
            self.rotation_2d_slider.hide()

        # Update the UI
        self.generate_output()

    def on_3d_shape_changed(self, shape_name):
        """Handle 3D shape selection change."""
        self.current_pattern = shape_name
        self.title_label.setText(f"Sacred Geometry Explorer - {shape_name}")

        # Show/hide shape-specific parameters
        if shape_name == "Merkaba":
            self.rotation_3d_spin.show()
            self.rotation_3d_slider.show()
            self.major_radius_spin.hide()
            self.major_radius_slider.hide()
            self.minor_radius_spin.hide()
            self.minor_radius_slider.hide()
            self.layers_3d_spin.hide()
        elif shape_name == "Torus":
            self.rotation_3d_spin.hide()
            self.rotation_3d_slider.hide()
            self.major_radius_spin.show()
            self.major_radius_slider.show()
            self.minor_radius_spin.show()
            self.minor_radius_slider.show()
            self.layers_3d_spin.hide()
        elif shape_name == "Flower of Life 3D":
            self.rotation_3d_spin.hide()
            self.rotation_3d_slider.hide()
            self.major_radius_spin.hide()
            self.major_radius_slider.hide()
            self.minor_radius_spin.hide()
            self.minor_radius_slider.hide()
            self.layers_3d_spin.show()
        else:
            self.rotation_3d_spin.hide()
            self.rotation_3d_slider.hide()
            self.major_radius_spin.hide()
            self.major_radius_slider.hide()
            self.minor_radius_spin.hide()
            self.minor_radius_slider.hide()
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
            self.angle_slider.show()
            self.length_factor_spin.show()
            self.length_factor_slider.show()
            self.turns_spin.hide()
            self.turns_slider.hide()
            self.max_iter_spin.hide()
            self.max_iter_slider.hide()
            self.julia_c_real_spin.hide()
            self.julia_c_real_slider.hide()
            self.julia_c_imag_spin.hide()
            self.julia_c_imag_slider.hide()
        elif fractal_name == "Sacred Spiral":
            self.angle_spin.hide()
            self.angle_slider.hide()
            self.length_factor_spin.hide()
            self.length_factor_slider.hide()
            self.turns_spin.show()
            self.turns_slider.show()
            self.max_iter_spin.hide()
            self.max_iter_slider.hide()
            self.julia_c_real_spin.hide()
            self.julia_c_real_slider.hide()
            self.julia_c_imag_spin.hide()
            self.julia_c_imag_slider.hide()
        elif fractal_name in ["Mandelbrot Set", "Julia Set"]:
            self.angle_spin.hide()
            self.angle_slider.hide()
            self.length_factor_spin.hide()
            self.length_factor_slider.hide()
            self.turns_spin.hide()
            self.turns_slider.hide()
            self.max_iter_spin.show()
            self.max_iter_slider.show()
            if fractal_name == "Julia Set":
                self.julia_c_real_spin.show()
                self.julia_c_real_slider.show()
                self.julia_c_imag_spin.show()
                self.julia_c_imag_slider.show()
            else:
                self.julia_c_real_spin.hide()
                self.julia_c_real_slider.hide()
                self.julia_c_imag_spin.hide()
                self.julia_c_imag_slider.hide()
        else:
            self.angle_spin.hide()
            self.angle_slider.hide()
            self.length_factor_spin.hide()
            self.length_factor_slider.hide()
            self.turns_spin.hide()
            self.turns_slider.hide()
            self.max_iter_spin.hide()
            self.max_iter_slider.hide()
            self.julia_c_real_spin.hide()
            self.julia_c_real_slider.hide()
            self.julia_c_imag_spin.hide()
            self.julia_c_imag_slider.hide()

        # Update the UI
        self.generate_output()

    def on_animation_changed(self, animation_name):
        """Handle animation selection change."""
        self.current_pattern = animation_name
        self.title_label.setText(f"Sacred Geometry Explorer - {animation_name}")

    def on_custom_changed(self, custom_name):
        """Handle custom pattern selection change."""
        self.current_pattern = custom_name
        self.title_label.setText(f"Sacred Geometry Explorer - {custom_name}")

        # Update the UI based on 2D/3D selection
        if self.dimension_combo.currentText() == "3D":
            self.canvas.set_3d_axes()
            self.rotation_group.show()
            self.export_button.show()
        else:
            self.canvas.set_2d_axes()
            self.rotation_group.hide()
            self.export_button.hide()

        # Generate the output
        self.generate_custom_output()

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

    def pick_custom_colors(self):
        """Open color picker dialog for custom colors."""
        color = QColorDialog.getColor(QColor(255, 215, 0), self, "Select Custom Color")
        if color.isValid():
            # Store the selected color
            self.custom_color = color
            self.status_bar.showMessage(f"Custom color selected: RGB({color.red()}, {color.green()}, {color.blue()})")

    def open_gallery(self):
        """Open the gallery of saved outputs."""
        QMessageBox.information(self, "Gallery", "Gallery feature coming soon!")

    def open_settings(self):
        """Open settings dialog."""
        QMessageBox.information(self, "Settings", "Settings feature coming soon!")

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

    def export_output(self):
        """Export the current 3D shape to a file."""
        if self.current_category != "3D Shapes" and not (self.current_category == "Custom" and self.dimension_combo.currentText() == "3D"):
            QMessageBox.warning(self, "Export Error", "Only 3D shapes can be exported.")
            return

        # Get the export file path
        filepath, _ = QFileDialog.getSaveFileName(
            self, "Export 3D Model", f"outputs/3d/{self.current_pattern.lower().replace(' ', '_')}.obj",
            "OBJ Files (*.obj);;STL Files (*.stl);;All Files (*)"
        )

        if filepath:
            try:
                # Export the 3D model
                QMessageBox.information(self, "Export",
                                      f"3D model export to {filepath} will be implemented in a future update.")
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
            elif self.current_category == "Custom":
                self.generate_custom_output()

            self.canvas.draw()
            self.status_bar.showMessage(f"Generated {self.current_pattern}")
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Error generating output: {str(e)}")
            self.status_bar.showMessage("Error generating output")

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

        # Apply material settings
        if material == "metallic":
            # Enhance the metallic appearance
            alpha = min(0.9, alpha + 0.1)
            # Use a custom metallic color scheme if available
        elif material == "glass":
            # Enhance the glass appearance
            alpha = min(0.7, alpha)
            # Use a custom glass color scheme if available
        elif material == "crystal":
            # Enhance the crystal appearance
            alpha = min(0.8, alpha)
            # Use a custom crystal color scheme if available

        # Apply lighting settings
        light_intensity = self.light_intensity_spin.value()
        light_angle = self.light_angle_spin.value() * np.pi / 180

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
