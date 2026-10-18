# Lesson 01 — Introduction to Artificial Intelligence

This lesson combines the detailed [A-X theory notes](../lessons/01_introduction_to_artificial_intelligence.md) with executable Jupyter practice. Each notebook uses Python 3.13.14 in the `Python 3 (AI Mastery)` kernel metadata, synthetic deterministic inputs, and saved outputs from a successful local execution. Plots are embedded in notebook outputs.

## Notebook sequence

| Notebook | Purpose |
|---|---|
| [02 Beginner Examples](02_Beginner_Examples.ipynb) | Explicit threshold rule versus a tiny centroid learner |
| [03 Intermediate Examples](03_Intermediate_Examples.ipynb) | Training summaries, held-out examples, and error metrics |
| [04 Advanced Examples](04_Advanced_Examples.ipynb) | Threshold tradeoffs, error types, and human approval boundaries |
| [05 Real-World Applications](05_Real_World_Applications.ipynb) | Synthetic network telemetry and read-only triage |
| [06 Practice Exercises](06_Practice_Exercises.ipynb) | Independent beginner-to-advanced challenges |
| [07 Exercise Solutions](07_Exercise_Solutions.ipynb) | Worked solutions; open only after attempting the exercises |
| [08 Common Errors and Debugging](08_Common_Errors_and_Debugging.ipynb) | Invalid input, missing model state, and evaluation mistakes |

Each notebook includes Sections A-J: introduction, beginner explanation, first code example, intermediate and advanced examples, real-world application, visualization, debugging, exercises, and summary/knowledge check. Explanations follow code cells and distinguish the saved actual output from broader claims.

## Run or re-run

From the course root:

```powershell
python -m pip install -e ".[notebooks]"
python -m nbclient --version
python shared_utils\build_intro_notebooks.py
```

The builder executes all notebook cells and rewrites the `.ipynb` files with actual outputs. It requires the optional `notebooks` dependencies in `pyproject.toml`; do not claim execution if the command fails. In VS Code, open a notebook and choose the Python 3.13 environment containing the notebook extra.

The examples are educational, not validated network diagnostics. They use no external service, credentials, customer data, or live device access, and do not perform configuration writes.
