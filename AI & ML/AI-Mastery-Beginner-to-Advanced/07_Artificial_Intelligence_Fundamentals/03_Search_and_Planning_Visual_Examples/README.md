# Search and Planning — Supplementary Lesson

This new lesson continues from [AI problem formulation](../02_AI_Problem_Formulation_Visual_Examples/01_AI_Problem_Formulation_Complete_Notes.md). It introduces state-space search with runnable Python implementations and saved visual notebook outputs. All network examples use a small synthetic topology and are read-only demonstrations.

## Learning sequence

1. [Complete notes](01_Search_and_Planning_Complete_Notes.md)
2. [Visual examples notebook](02_Search_and_Planning_Visual_Examples.ipynb)
3. [Practice exercises](03_Search_and_Planning_Exercises.ipynb)
4. [Separate solutions](04_Search_and_Planning_Solutions.ipynb)
5. [Reusable search implementation](05_search_algorithms.py)

The visual notebook compares breadth-first search, Dijkstra's uniform-cost search, and A* using the same weighted graph, then shows how an inadmissible heuristic can lose optimality. A route is only a proposed sequence through a synthetic graph; the code never configures or contacts routers.

## Execution

The three notebooks were executed with Python 3.13.14 and Matplotlib 3.10.8; outputs and figures are saved in the notebooks. Re-run from the course root:

```powershell
python -m pip install -e ".[notebooks]"
python 07_Artificial_Intelligence_Fundamentals\03_Search_and_Planning_Visual_Examples\build_search_notebooks.py
```

The builder refuses to overwrite any existing target notebook.
