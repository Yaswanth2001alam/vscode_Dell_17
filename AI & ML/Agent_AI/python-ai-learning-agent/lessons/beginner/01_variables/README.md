# Python Variables, Data Types, and Memory Fundamentals

Start with `notes.md`, run `examples.py`, then edit **a copy** of `exercises.py`.
Compare with `solutions.py` after trying all six exercises.

From the project directory, use the project interpreter:

```powershell
.\.venv\Scripts\python.exe -m python_learning_agent learn variables
.\.venv\Scripts\python.exe lessons\beginner\01_variables\examples.py
.\.venv\Scripts\python.exe -m python_learning_agent practice variables
.\.venv\Scripts\python.exe -m python_learning_agent quiz variables
.\.venv\Scripts\python.exe -m pytest tests\test_lesson.py
```

For the notebook, select `.venv\Scripts\python.exe` as the VS Code notebook
kernel and run `notebooks\beginner\01_variables.ipynb` from top to bottom.
The notebook contains assertions and a Matplotlib visualization.
The exact expected script output is in `notes.md`.

The exercise file deliberately raises `NotImplementedError` until you implement
the functions. The default tests check the supplied solutions, not your work.
To evaluate a reviewed exercise copy, use the explicit assessment command in the
project README. Executing that copy is local execution, not sandboxed execution.
