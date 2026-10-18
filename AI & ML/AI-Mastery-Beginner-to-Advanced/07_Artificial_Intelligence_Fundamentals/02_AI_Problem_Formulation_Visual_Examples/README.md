# AI Problem Formulation — Supplementary Lesson

This is a new continuation lesson. It preserves the existing course files and teaches how to turn a vague request into a bounded, measurable, and safe computational task.

## Learning order

1. Read [complete notes](01_AI_Problem_Formulation_Complete_Notes.md).
2. Run the [visual examples notebook](02_AI_Problem_Formulation_Visual_Examples.ipynb).
3. Attempt the [practice notebook](03_AI_Problem_Formulation_Exercises.ipynb) before opening [solutions](04_AI_Problem_Formulation_Solutions.ipynb).
4. Review and modify the reusable [Python implementation](05_problem_formulation.py).

The notebooks have been executed locally with Python 3.13.14 and Matplotlib 3.10.8; actual printed outputs and figures are saved in the `.ipynb` files. They use only synthetic examples and do not connect to cloud services or network devices.

## Re-run notebooks

From the course root with the notebook optional dependencies installed:

```powershell
python -m pip install -e ".[notebooks]"
python 07_Artificial_Intelligence_Fundamentals\02_AI_Problem_Formulation_Visual_Examples\build_problem_formulation_notebooks.py
```

The builder refuses to replace an existing notebook. If a target notebook already exists, it stops and reports the conflict. Open the notebooks in VS Code using the project's Python 3 kernel.

## Safety scope

Network scenarios are synthetic. The reusable implementation ranks conceptual actions; it does not connect to a device, send commands, or perform a configuration change. The candidate `reset_interface` is explicitly disallowed unless a human approval flag is supplied, and no execution mechanism is provided.
