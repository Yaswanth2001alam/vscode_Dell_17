"""Small graph-search algorithms for educational, read-only planning examples."""

from __future__ import annotations

from collections import deque
from heapq import heappop, heappush
from itertools import count
from math import isfinite
from typing import Callable, Mapping, Sequence

Graph = Mapping[str, Sequence[tuple[str, float]]]


def validate_graph(graph: Graph) -> None:
    """Validate finite, nonnegative edge costs and known neighbor nodes."""
    for node, edges in graph.items():
        if not isinstance(node, str) or not node:
            raise ValueError("graph node names must be non-empty strings")
        for neighbor, cost in edges:
            if neighbor not in graph:
                raise ValueError(f"neighbor {neighbor!r} is not a graph node")
            if not isfinite(cost) or cost < 0:
                raise ValueError("edge costs must be finite and non-negative")


def reconstruct_path(
    parents: Mapping[str, str | None], start: str, goal: str
) -> list[str] | None:
    """Reconstruct a path from predecessor links, or return None if unreachable."""
    if goal not in parents:
        return None
    path = [goal]
    while path[-1] != start:
        parent = parents.get(path[-1])
        if parent is None:
            return None
        path.append(parent)
    path.reverse()
    return path


def breadth_first_search(graph: Graph, start: str, goal: str) -> list[str] | None:
    """Find a path with the fewest edges; edge weights are intentionally ignored."""
    validate_graph(graph)
    if start not in graph or goal not in graph:
        raise ValueError("start and goal must be graph nodes")
    frontier = deque([start])
    parents: dict[str, str | None] = {start: None}
    while frontier:
        node = frontier.popleft()
        if node == goal:
            return reconstruct_path(parents, start, goal)
        for neighbor, _ in graph[node]:
            if neighbor not in parents:
                parents[neighbor] = node
                frontier.append(neighbor)
    return None


def dijkstra(
    graph: Graph, start: str, goal: str
) -> tuple[list[str] | None, float]:
    """Find a minimum-cost path when every edge has nonnegative cost."""
    validate_graph(graph)
    if start not in graph or goal not in graph:
        raise ValueError("start and goal must be graph nodes")
    sequence = count()
    frontier: list[tuple[float, int, str]] = [(0.0, next(sequence), start)]
    best_cost = {start: 0.0}
    parents: dict[str, str | None] = {start: None}
    while frontier:
        cost_so_far, _, node = heappop(frontier)
        if cost_so_far != best_cost.get(node):
            continue
        if node == goal:
            return reconstruct_path(parents, start, goal), cost_so_far
        for neighbor, edge_cost in graph[node]:
            candidate = cost_so_far + edge_cost
            if candidate < best_cost.get(neighbor, float("inf")):
                best_cost[neighbor] = candidate
                parents[neighbor] = node
                heappush(frontier, (candidate, next(sequence), neighbor))
    return None, float("inf")


def a_star(
    graph: Graph,
    start: str,
    goal: str,
    heuristic: Callable[[str], float],
) -> tuple[list[str] | None, float]:
    """Find a path prioritizing g+h; optimality needs a suitable heuristic."""
    validate_graph(graph)
    if start not in graph or goal not in graph:
        raise ValueError("start and goal must be graph nodes")

    def estimate(node: str) -> float:
        value = heuristic(node)
        if not isfinite(value) or value < 0:
            raise ValueError("heuristic values must be finite and non-negative")
        return value

    sequence = count()
    frontier: list[tuple[float, int, float, str]] = [
        (estimate(start), next(sequence), 0.0, start)
    ]
    best_cost = {start: 0.0}
    parents: dict[str, str | None] = {start: None}
    while frontier:
        _, _, cost_so_far, node = heappop(frontier)
        if cost_so_far != best_cost.get(node):
            continue
        if node == goal:
            return reconstruct_path(parents, start, goal), cost_so_far
        for neighbor, edge_cost in graph[node]:
            candidate = cost_so_far + edge_cost
            if candidate < best_cost.get(neighbor, float("inf")):
                best_cost[neighbor] = candidate
                parents[neighbor] = node
                priority = candidate + estimate(neighbor)
                heappush(
                    frontier, (priority, next(sequence), candidate, neighbor)
                )
    return None, float("inf")


SAMPLE_GRAPH: dict[str, list[tuple[str, float]]] = {
    "A": [("B", 2), ("C", 1), ("G", 9)],
    "B": [("A", 2), ("D", 2), ("E", 5)],
    "C": [("A", 1), ("D", 5), ("F", 7)],
    "D": [("B", 2), ("C", 5), ("G", 3)],
    "E": [("B", 5), ("G", 1)],
    "F": [("C", 7), ("G", 2)],
    "G": [("A", 9), ("D", 3), ("E", 1), ("F", 2)],
}

HEURISTIC = {"A": 5, "B": 4, "C": 6, "D": 2, "E": 1, "F": 2, "G": 0}


def main() -> None:
    bfs_path = breadth_first_search(SAMPLE_GRAPH, "A", "G")
    dijkstra_path, dijkstra_cost = dijkstra(SAMPLE_GRAPH, "A", "G")
    astar_path, astar_cost = a_star(
        SAMPLE_GRAPH, "A", "G", lambda node: HEURISTIC[node]
    )
    print("BFS fewest-edge route:", bfs_path)
    print(f"Dijkstra minimum-cost route: {dijkstra_path}, cost={dijkstra_cost:g}")
    print(f"A* route with documented heuristic: {astar_path}, cost={astar_cost:g}")
    print("Costs are synthetic; no network is contacted or changed.")


if __name__ == "__main__":
    main()
