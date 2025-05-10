"""
Main script to generate all sacred geometry outputs.
This script runs all the generator scripts to create a complete set of outputs.
"""
import os
import time
import subprocess
import sys

def print_header(text):
    """Print a formatted header."""
    print("\n" + "=" * 80)
    print(f" {text} ".center(80, "="))
    print("=" * 80 + "\n")

def run_script(script_name):
    """Run a Python script and measure execution time."""
    print_header(f"Running {script_name}")

    start_time = time.time()
    result = subprocess.run([sys.executable, script_name], capture_output=True, text=True)
    end_time = time.time()

    # Print output
    print(result.stdout)

    # Print errors if any
    if result.stderr:
        print("ERRORS:")
        print(result.stderr)

    print(f"\nCompleted in {end_time - start_time:.2f} seconds")
    return result.returncode == 0

def ensure_output_dirs():
    """Ensure all output directories exist."""
    output_dirs = [
        "outputs",
        "outputs/2d",
        "outputs/3d",
        "outputs/animations",
        "outputs/fractals",
        "outputs/compositions"
    ]

    for directory in output_dirs:
        os.makedirs(directory, exist_ok=True)
        print(f"Ensured directory exists: {directory}")

def main():
    """Main function to run all generator scripts."""
    print_header("SACRED GEOMETRY OUTPUT GENERATOR")

    # Ensure output directories exist
    ensure_output_dirs()

    # List of scripts to run
    scripts = [
        "generate_outputs.py",
        "generate_animations.py",
        "generate_compositions.py",
        "generate_custom.py"
    ]

    # Run each script
    success_count = 0
    for script in scripts:
        if run_script(script):
            success_count += 1

    # Print summary
    print_header("GENERATION SUMMARY")
    print(f"Successfully ran {success_count} out of {len(scripts)} scripts")

    if success_count == len(scripts):
        print("\nAll outputs generated successfully!")
        print("\nOutput directories:")
        for root, dirs, files in os.walk("outputs"):
            level = root.replace("outputs", "").count(os.sep)
            indent = " " * 4 * level
            print(f"{indent}{os.path.basename(root)}/")

            # Count files in this directory
            file_count = len(files)
            if file_count > 0:
                print(f"{indent}    ({file_count} files)")
    else:
        print("\nSome scripts failed. Check the output above for errors.")

if __name__ == "__main__":
    main()
