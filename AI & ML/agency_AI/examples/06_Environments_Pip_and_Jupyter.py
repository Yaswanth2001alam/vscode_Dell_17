"""
Virtual environments, pip, and Jupyter.

Level: Beginner.
Run this file with the course virtual environment's Python.
Examples are offline, CPU-sized, and use local synthetic data.
See the matching notebook for full explanations, assumptions, and exercises.
"""

# %% Worked example: Inspect the active learning environment
# Verify interpreter and package discovery without changing your machine.
# Step 1: Read sys.executable to identify the actual kernel interpreter.
# Step 2: Compare virtual-environment prefixes.
# Step 3: Query package versions without running pip.
# Step 4: Assert NumPy is installed before later numerical lessons.
if __name__ == "__main__":
    import importlib.metadata
    import sys

    packages = ["numpy", "pandas", "scikit-learn", "torch"]
    versions = {name: importlib.metadata.version(name) for name in packages}
    assert all(versions.values())
    print("Python:", sys.version.split()[0])
    print("Virtual environment:", sys.prefix != sys.base_prefix)
    print("Packages:", versions)
