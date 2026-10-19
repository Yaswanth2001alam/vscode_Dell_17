"""Execute the reviewed notebook and export a report plus two figures.

Run from the project root:
    .\\.venv\\Scripts\\python.exe scripts\\export_demo.py reports\\variables-demo

The output directory must not exist. This is ordinary trusted local Python
execution, NOT sandboxed execution. Do not run notebooks you have not reviewed.
"""

import argparse
import base64
import sys
from pathlib import Path

import nbformat
from nbclient import NotebookClient


def export_demo(destination: Path) -> None:
    """Validate and execute bundled content using this exact Python interpreter."""
    root = Path(__file__).resolve().parents[1]
    destination = destination.resolve()
    if destination.exists():
        raise FileExistsError(f"Refusing to overwrite existing output: {destination}")
    source = root / "notebooks" / "beginner" / "01_variables.ipynb"
    notebook = nbformat.read(source, as_version=4)
    nbformat.validate(notebook)
    client = NotebookClient(
        notebook,
        timeout=90,
        kernel_name="python3",
        resources={"metadata": {"path": str(root)}},
    )
    manager = client.create_kernel_manager()
    manager.kernel_spec.argv = [
        sys.executable,
        "-m",
        "ipykernel_launcher",
        "-f",
        "{connection_file}",
    ]
    executed = client.execute()
    nbformat.validate(executed)
    figures = [
        output["data"]["image/png"]
        for cell in executed.cells
        if cell.cell_type == "code"
        for output in cell.outputs
        if "image/png" in output.get("data", {})
    ]
    if len(figures) != 2:
        raise ValueError(f"Expected two demonstration figures; found {len(figures)}.")
    destination.mkdir(parents=True, exist_ok=False)
    with (destination / "01_variables.executed.ipynb").open("x", encoding="utf-8") as stream:
        nbformat.write(executed, stream)
    for name, image in zip(("bindings.png", "direct-object-sizes.png"), figures, strict=True):
        with (destination / name).open("xb") as stream:
            stream.write(base64.b64decode(image, validate=True))
    print(f"Executed notebook and two explained figures saved to: {destination}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("destination", type=Path, help="New output directory; never overwritten")
    arguments = parser.parse_args()
    export_demo(arguments.destination)
