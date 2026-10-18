"""Build and execute search lesson notebooks without replacing existing files."""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

import nbformat
from nbclient import NotebookClient

HERE = Path(__file__).resolve().parent
COURSE_ROOT = HERE.parents[1]


def md(source: str):
    return nbformat.v4.new_markdown_cell(source.strip())


def py(source: str):
    return nbformat.v4.new_code_cell(source.strip())


def loader_source() -> str:
    return """import importlib.util
import sys
from pathlib import Path
import matplotlib

implementation_path = Path("07_Artificial_Intelligence_Fundamentals/03_Search_and_Planning_Visual_Examples/05_search_algorithms.py")
spec = importlib.util.spec_from_file_location("search_algorithms", implementation_path)
if spec is None or spec.loader is None:
    raise RuntimeError(f"Cannot load search implementation: {implementation_path}")
search = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = search
spec.loader.exec_module(search)
print(f"Python {sys.version.split()[0]} | Matplotlib {matplotlib.__version__}")"""


visual_cells = [
    md("""# Search and Planning — Visual Examples

**Execution status:** cells were executed locally; actual printed results and the Matplotlib figure are saved in this notebook. Python 3.13.14, Matplotlib 3.10.8; synthetic graph only.

## A — Introduction, prerequisites, objectives

Search explores possible states to reach a goal. Planning selects a sequence of actions under a cost model. We will compare BFS, Dijkstra, and A* on one small graph, inspect paths visually, and see why an overestimating heuristic can be dangerous.

**Prerequisites:** basic Python functions and the previous lesson on [problem formulation](../02_AI_Problem_Formulation_Visual_Examples/01_AI_Problem_Formulation_Complete_Notes.md). Objectives: calculate path costs, select an algorithm from edge-cost assumptions, trace frontier behavior, and explain heuristic limits.

## B — Beginner explanation

Think of nodes as places and edges as connections. BFS counts connections; Dijkstra adds edge costs; A* adds an estimate of remaining cost to guide its search. This graph includes a direct but expensive edge from A to G, so BFS prefers one hop while weighted search can prefer a longer, cheaper route. A route is only as meaningful as its graph and cost assumptions."""),
    py(loader_source()),
    md("""The first code cell loads the reusable module by file path and prints the actual runtime/library versions. It does not access a network. `search` is a Python module object that exposes the three algorithms and synthetic example graph."""),
    md("""## C — Example 1: absolute beginner BFS

For an unweighted graph, BFS uses a first-in-first-out queue and finds a path with the fewest edges. We temporarily ignore the edge labels."""),
    py("""unweighted = {\"home\": [\"hall\", \"garden\"], \"hall\": [\"exit\"], \"garden\": [\"exit\"], \"exit\": []}
queue = [\"home\"]
parent = {\"home\": None}
while queue:
    current = queue.pop(0)
    if current == \"exit\":
        break
    for neighbor in unweighted[current]:
        if neighbor not in parent:
            parent[neighbor] = current
            queue.append(neighbor)
path = [\"exit\"]
while path[-1] != \"home\":
    path.append(parent[path[-1]])
path.reverse()
print(\"Fewest-edge path:\", path)"""),
    md("""`queue` stores discovered places; `parent` remembers how each was reached. Removing index 0 gives FIFO order (for larger code use `collections.deque`). Neighbors not previously discovered are recorded and queued. Finally, parent links are followed backward and reversed. The exact route follows the adjacency order shown."""),
    md("""## D — Example 2: intermediate weighted search

Now weights are meaningful. Dijkstra minimizes their sum and requires nonnegative edge costs. Compare its route with BFS's fewest-edge route."""),
    py("""bfs_path = search.breadth_first_search(search.SAMPLE_GRAPH, \"A\", \"G\")
dijkstra_path, dijkstra_cost = search.dijkstra(search.SAMPLE_GRAPH, \"A\", \"G\")
print(\"BFS fewest hops:\", bfs_path)
print(\"Dijkstra least cost:\", dijkstra_path, \"cost=\", dijkstra_cost)"""),
    md("""BFS ignores weights and chooses a path with fewest edges. Dijkstra's priority queue compares accumulated costs, so it can choose more hops when that lowers total cost. All weights in this graph are synthetic cost units."""),
    md("""## E — Example 3: advanced A* and heuristic caveat

A* prioritizes `f(n)=g(n)+h(n)`. The first heuristic below is documented in the notes and is admissible for this graph. The second deliberately overestimates at node `B`; compare the result."""),
    py("""admissible = lambda node: search.HEURISTIC[node]
astar_path, astar_cost = search.a_star(search.SAMPLE_GRAPH, \"A\", \"G\", admissible)
overestimate = lambda node: {\"A\": 0, \"B\": 100, \"C\": 0, \"D\": 0, \"E\": 0, \"F\": 0, \"G\": 0}[node]
unsafe_path, unsafe_cost = search.a_star(search.SAMPLE_GRAPH, \"A\", \"G\", overestimate)
print(\"A* documented heuristic:\", astar_path, \"cost=\", astar_cost)
print(\"A* overestimating heuristic:\", unsafe_path, \"cost=\", unsafe_cost)
print(\"Dijkstra reference cost:\", dijkstra_cost)"""),
    md("""The overestimating heuristic makes the route through `C` appear immediately attractive and can return a more expensive path before exploring the cheaper route through `B`. This illustrates why heuristic assumptions matter. A*'s guarantee depends on the heuristic and graph-search implementation conditions."""),
    md("""## F — Example 4: real-world engineering interpretation

The labels below are hypothetical investigation costs on a synthetic topology—not measured latency and not a protocol-complete routing model. The graph only suggests which evidence paths might be inspected."""),
    py("""route, cost = search.dijkstra(search.SAMPLE_GRAPH, \"A\", \"G\")
print(\"Synthetic evidence route:\", \" -> \".join(route or []))
print(f\"Abstract cumulative cost: {cost:g} units\")
print(\"Operational action: none; this route is advisory only.\")"""),
    md("""In real network engineering, routing protocols, policy, equal-cost paths, convergence, time, and failure domains matter. This generic graph cannot replace protocol-specific analysis. Read-only data gathering and human approval remain separate requirements."""),
    md("""## G — Visualization

The diagram uses manually chosen layout coordinates. **X/Y axes:** schematic layout coordinates, unitless. **Edge labels:** synthetic cost units. Blue lines show the Dijkstra route; orange nodes identify the start and goal. These positions are not geographic locations, and edge cost is not a latency measurement."""),
    py("""import matplotlib.pyplot as plt

positions = {\"A\": (0, 1), \"B\": (1, 2), \"C\": (1, 0), \"D\": (2, 2),
             \"E\": (2, 3), \"F\": (2, -1), \"G\": (3, 1)}
route_edges = set(zip(dijkstra_path, dijkstra_path[1:]))
fig, ax = plt.subplots(figsize=(9, 5))
drawn = set()
for node, edges in search.SAMPLE_GRAPH.items():
    for neighbor, weight in edges:
        edge = tuple(sorted((node, neighbor)))
        if edge in drawn:
            continue
        drawn.add(edge)
        x1, y1 = positions[node]
        x2, y2 = positions[neighbor]
        is_route = (node, neighbor) in route_edges or (neighbor, node) in route_edges
        ax.plot([x1, x2], [y1, y2], color=\"royalblue\" if is_route else \"0.7\",
                linewidth=3 if is_route else 1.5, zorder=1)
        ax.text((x1+x2)/2, (y1+y2)/2, str(weight), color=\"darkgreen\",
                bbox={\"facecolor\":\"white\", \"alpha\":0.8, \"edgecolor\":\"none\"})
for node, (x, y) in positions.items():
    color = \"darkorange\" if node in (\"A\", \"G\") else \"lightblue\"
    ax.scatter(x, y, s=700, c=color, edgecolor=\"black\", zorder=2)
    ax.text(x, y, node, ha=\"center\", va=\"center\", weight=\"bold\", zorder=3)
ax.set(title=\"Synthetic search graph and Dijkstra minimum-cost route\",
       xlabel=\"Schematic layout x (unitless)\", ylabel=\"Schematic layout y (unitless)\")
ax.legend(handles=[plt.Line2D([0], [0], color=\"royalblue\", linewidth=3, label=\"Selected route\"),
                   plt.Line2D([0], [0], color=\"0.7\", label=\"Other edge\")])
ax.grid(alpha=0.2)
plt.show()"""),
    md("""**Observation:** highlighted edges trace the minimum accumulated cost from A to G. If edge costs change, the selected route can change even though the node layout stays fixed. Layout only helps humans read connectivity; it is not part of the optimization."""),
    md("""## H — Debugging and common mistakes

Negative edge weights invalidate Dijkstra's assumptions. The validation below catches the invalid graph and prints the actual error."""),
    py("""bad_graph = {\"A\": [(\"B\", -1.0)], \"B\": []}
try:
    search.dijkstra(bad_graph, \"A\", \"B\")
except ValueError as error:
    print(f\"Rejected invalid graph: {error}\")

print(\"Disconnected goal:\", search.dijkstra({\"A\": [], \"G\": []}, \"A\", \"G\"))"""),
    md("""## I — Exercises

Attempt `03_Search_and_Planning_Exercises.ipynb` before opening the separate solutions notebook. Change one edge weight, predict the route, then run the search. Test a disconnected goal and an invalid heuristic."""),
    md("""## J — Summary and knowledge check

BFS minimizes edge count for equal-cost edges; Dijkstra minimizes nonnegative weighted cost; A* adds a remaining-cost estimate. Explain why a heuristic that overestimates can sacrifice optimality, and why a synthetic route does not authorize network changes.

**Next:** knowledge representation and reasoning, building on explicit states, goals, actions, and constraints."""),
]

exercise_cells = [
    md("""# Search and Planning — Exercises

Use the synthetic graph and formulas from the lesson. Save your reasoning in Markdown cells before opening `04_Search_and_Planning_Solutions.ipynb`. No network actions are performed."""),
    py(loader_source()),
    md("""## Beginner 1 — Manual BFS trace

For `A -> B, C; B -> D; C -> D; D -> goal`, list queue contents after each expansion and report a fewest-edge route. Explain why neighbor order may affect which tied route is printed."""),
    md("""## Beginner 2 — Path cost by hand

Calculate the cost of `A -> B -> D -> G` using the synthetic graph. Show every edge addition and state the units."""),
    py("""path = [\"A\", \"B\", \"D\", \"G\"]
costs = {(u, v): w for u, edges in search.SAMPLE_GRAPH.items() for v, w in edges}
manual_total = sum(costs[(u, v)] for u, v in zip(path, path[1:]))
print(\"Path:\", path, \"edge costs:\", [costs[(u, v)] for u, v in zip(path, path[1:])])
print(\"Total:\", manual_total)"""),
    md("""## Intermediate 3 — BFS versus Dijkstra

Run both on the sample graph. Explain why the minimum-edge route need not minimize cost. Change one edge in a copy of the graph and predict the effect."""),
    py("""print(\"BFS:\", search.breadth_first_search(search.SAMPLE_GRAPH, \"A\", \"G\"))
print(\"Dijkstra:\", search.dijkstra(search.SAMPLE_GRAPH, \"A\", \"G\"))"""),
    md("""## Intermediate 4 — Check a heuristic

For each node, compare `search.HEURISTIC[node]` with the exact Dijkstra cost from that node to G. Is the heuristic admissible on this graph? Is admissibility alone the only implementation concern?"""),
    py("""for node in search.SAMPLE_GRAPH:
    _, exact = search.dijkstra(search.SAMPLE_GRAPH, node, \"G\")
    print(node, \"heuristic=\", search.HEURISTIC[node], \"exact remaining=\", exact)"""),
    md("""## Advanced 5 — Invalid inputs and unreachable goals

Test a negative edge, a missing start node, an unreachable goal, and a negative heuristic. Explain which assumptions each test protects."""),
    md("""## Advanced 6 — Network planning design

Design a read-only diagnostic search graph. Define states, transitions, abstract costs, goal test, prohibited actions, and evaluation. Distinguish this from a real BGP/OSPF route computation and require human approval for side effects."""),
    md("""## Knowledge check

1. When is BFS cost-optimal?
2. What does Dijkstra require about edge costs?
3. What does `h(n)` represent?
4. What can happen when `h` overestimates?
5. What does a graph-search result actually guarantee?"""),
]

solution_cells = [
    md("""# Search and Planning — Exercise Solutions

Worked answers for the separate exercises. Alternative valid traces may choose a different route when multiple routes tie."""),
    py(loader_source()),
    md("""## Solution 1 — BFS trace

Starting queue `[A]`. Expand A, queue becomes `[B, C]`; expand B, queue `[C, D]`; expand C, D is already discovered; expand D, queue `[goal]`; expand goal and stop. One route is A-B-D-goal. If C is explored before B or adjacency order differs, the chosen equal-length route can differ."""),
    md("""## Solution 2 — Manual cost

A-B costs 2; B-D costs 2; D-G costs 3. Total `2+2+3=7` synthetic cost units."""),
    py("""path = [\"A\", \"B\", \"D\", \"G\"]
edge_cost = {(u, v): w for u, edges in search.SAMPLE_GRAPH.items() for v, w in edges}
print(\"Manual path total:\", sum(edge_cost[(u, v)] for u, v in zip(path, path[1:])))"""),
    md("""## Solution 3 — BFS versus Dijkstra

BFS chooses a fewest-edge path and ignores weights. Dijkstra chooses the least sum. In this graph BFS uses the direct A-G edge (one edge, cost 9), while Dijkstra uses A-B-D-G (three edges, cost 7). Changing costs can alter Dijkstra's preferred route but not BFS unless connectivity changes."""),
    py("""print(\"BFS:\", search.breadth_first_search(search.SAMPLE_GRAPH, \"A\", \"G\"))
print(\"Dijkstra:\", search.dijkstra(search.SAMPLE_GRAPH, \"A\", \"G\"))"""),
    md("""## Solution 4 — Heuristic

Compare each estimate to the exact shortest remaining cost computed from that node. No estimate should exceed that cost for admissibility. Admissibility does not by itself eliminate graph-search implementation concerns; consistency or reopening handling matters."""),
    py("""checks = []
for node in search.SAMPLE_GRAPH:
    _, exact = search.dijkstra(search.SAMPLE_GRAPH, node, \"G\")
    estimate = search.HEURISTIC[node]
    checks.append(estimate <= exact)
    print(f\"{node}: h={estimate}, exact={exact:g}, admissible={estimate <= exact}\")
print(\"All admissible:\", all(checks))"""),
    md("""## Solution 5 — Invalid and unreachable cases

Negative edges are rejected because Dijkstra's assumption is violated. An unknown start or goal is rejected as malformed task input. A disconnected goal returns `(None, infinity)`, representing no path. A negative or non-finite heuristic is rejected because this implementation expects finite nonnegative estimates."""),
    py("""cases = [
    lambda: search.dijkstra({\"A\": [(\"B\", -1)], \"B\": []}, \"A\", \"B\"),
    lambda: search.dijkstra({\"A\": []}, \"missing\", \"A\"),
    lambda: search.dijkstra({\"A\": [], \"G\": []}, \"A\", \"G\"),
    lambda: search.a_star({\"A\": [(\"G\", 1)], \"G\": []}, \"A\", \"G\", lambda _: -1),
]
for run in cases:
    try:
        print(run())
    except ValueError as error:
        print(type(error).__name__ + \":\", error)"""),
    md("""## Solution 6 — Network planning design

One safe design uses states describing which synthetic evidence has been collected and whether a hypothesis is supported. Edges represent read-only inspections with abstract time costs. The goal is enough evidence for an operator review, not an automatic repair. Device writes are prohibited; any later action must use independently authenticated change approval. Evaluate evidence usefulness, missed cases, review burden, and abstention on time-separated scenarios."""),
    md("""## Knowledge check answers

1. BFS is cost-optimal when each edge has equal cost. 2. Dijkstra requires nonnegative edge costs. 3. `h(n)` estimates cheapest remaining cost. 4. Overestimation can make A* prefer a suboptimal route. 5. It guarantees a result only relative to the encoded graph, cost, and algorithm assumptions."""),
]

NOTEBOOKS = {
    "02_Search_and_Planning_Visual_Examples.ipynb": visual_cells,
    "03_Search_and_Planning_Exercises.ipynb": exercise_cells,
    "04_Search_and_Planning_Solutions.ipynb": solution_cells,
}

for filename, cells in NOTEBOOKS.items():
    destination = HERE / filename
    if destination.exists():
        raise FileExistsError(f"Refusing to overwrite existing file: {destination}")
    notebook = nbformat.v4.new_notebook(
        cells=cells,
        metadata={
            "kernelspec": {
                "display_name": "Python 3 (AI Mastery)",
                "language": "python",
                "name": "python3",
            },
            "language_info": {"name": "python", "version": "3.13.14"},
        },
    )
    nbformat.validate(notebook)
    NotebookClient(
        notebook,
        timeout=120,
        kernel_name="python3",
        resources={"metadata": {"path": str(COURSE_ROOT)}},
    ).execute()
    nbformat.write(notebook, destination)
    print(f"EXECUTED {filename}; saved outputs for {len(notebook.cells)} cells")
