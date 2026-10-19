"""Validate and execute only the bundled, reviewed demonstration notebook."""

import subprocess
import sys
from pathlib import Path

import nbformat

ROOT = Path(__file__).resolve().parents[1]
NOTEBOOK = ROOT / "notebooks" / "beginner" / "01_variables.ipynb"


def test_notebook_schema_execution_and_non_overwriting_export(tmp_path: Path) -> None:
    notebook = nbformat.read(NOTEBOOK, as_version=4)
    nbformat.validate(notebook)
    destination = tmp_path / "export"
    command = [sys.executable, str(ROOT / "scripts" / "export_demo.py"), str(destination)]
    result = subprocess.run(command, capture_output=True, text=True, timeout=120, check=False)
    assert result.returncode == 0, result.stdout + result.stderr
    executed = nbformat.read(destination / "01_variables.executed.ipynb", as_version=4)
    nbformat.validate(executed)
    for name in ("bindings.png", "direct-object-sizes.png"):
        assert (destination / name).read_bytes().startswith(b"\x89PNG\r\n\x1a\n")
    original_bytes = (destination / "01_variables.executed.ipynb").read_bytes()
    repeated = subprocess.run(command, capture_output=True, text=True, timeout=30, check=False)
    assert repeated.returncode != 0
    assert "Refusing to overwrite" in repeated.stderr
    assert (destination / "01_variables.executed.ipynb").read_bytes() == original_bytes
    code_cells = [cell for cell in executed.cells if cell.cell_type == "code"]
    assert all(cell.execution_count is not None for cell in code_cells)
    assert not any(output.output_type == "error" for cell in code_cells for output in cell.outputs)
    images = [
        output
        for cell in code_cells
        for output in cell.outputs
        if "image/png" in output.get("data", {})
    ]
    assert len(images) == 2
    assert any(sys.executable in output.get("text", "") for output in code_cells[0].outputs)
