#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Graphical User Interface for the Sacred Geometry package.

This module provides a simple entry point to launch the GUI application.
"""

import sys
import os
import importlib.util

def check_dependencies():
    """Check if required dependencies are installed."""
    required_packages = ['PyQt5', 'matplotlib', 'numpy']
    missing_packages = []
    
    for package in required_packages:
        if importlib.util.find_spec(package) is None:
            missing_packages.append(package)
    
    return missing_packages

def main():
    """Main entry point for the GUI."""
    # Check dependencies
    missing_packages = check_dependencies()
    if missing_packages:
        print("Error: Missing required dependencies:")
        for package in missing_packages:
            print(f"  - {package}")
        print("\nPlease install the missing dependencies with:")
        print(f"pip install {' '.join(missing_packages)}")
        return 1
    
    # Import the GUI module
    try:
        # First try to import the enhanced GUI
        try:
            from sacred_geometry.gui.enhanced_sacred_geometry_gui import SacredGeometryApp
            gui_type = "enhanced"
        except ImportError:
            # Fall back to the basic GUI
            from sacred_geometry.gui.sacred_geometry_gui import SacredGeometryApp
            gui_type = "basic"
        
        # Create output directories if they don't exist
        output_dirs = {
            '2d': 'outputs/2d',
            '3d': 'outputs/3d',
            'fractals': 'outputs/fractals',
            'animations': 'outputs/animations',
            'compositions': 'outputs/compositions'
        }
        
        for directory in output_dirs.values():
            os.makedirs(directory, exist_ok=True)
        
        # Launch the GUI
        from PyQt5.QtWidgets import QApplication
        app = QApplication(sys.argv)
        window = SacredGeometryApp()
        window.show()
        print(f"Launched {gui_type} Sacred Geometry GUI")
        return app.exec_()
    
    except ImportError as e:
        # If the GUI modules are not found, try to launch the standalone GUI
        print(f"Error importing GUI modules: {e}")
        print("Trying to launch standalone GUI...")
        
        try:
            # Check if the standalone GUI file exists
            standalone_gui = "esoteric_sacred_geometry_gui.py"
            if os.path.exists(standalone_gui):
                print(f"Launching standalone GUI: {standalone_gui}")
                # Use exec to run the standalone GUI
                import subprocess
                result = subprocess.call([sys.executable, standalone_gui])
                return result
            else:
                print(f"Standalone GUI file not found: {standalone_gui}")
                return 1
        except Exception as e:
            print(f"Error launching standalone GUI: {e}")
            return 1

if __name__ == "__main__":
    sys.exit(main())
