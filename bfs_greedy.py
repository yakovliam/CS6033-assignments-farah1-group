import heapq
import time
from typing import Callable, Dict, List, Tuple, Any, Optional

Graph = Dict[str, Dict[str, float]]
Heuristic = Callable[[str, str], float]

def best_first_search(
    graph: Graph,
    start: str,
    goal: str,
    heuristic: Heuristic,
    *,
    return_metrics: bool = False
) -> List[str] | Tuple[List[str], dict]:
    """
    Greedy Best-First Search (GBFS).
    Expands the node with the lowest heuristic h(n) to the goal.

    Returns:
        path (list[str]) OR (path, metrics) if return_metrics=True
        If no path exists, path is [].
    """
    t0 = time.perf_counter()

    if start == goal:
        t1 = time.perf_counter()
        if return_metrics:
            return [start], {
                "found": True,
                "expanded": 0,
                "visited": 1,
                "enqueued": 1,
                "max_frontier": 1,
                "time_sec": t1 - t0,
            }
        return [start]

    frontier: List[Tuple[float, str, List[str]]] = [(heuristic(start, goal), start, [start])]
    visited = set()

    # Metrics
    expanded = 0          # times we pop from frontier and process neighbors
    enqueued = 1          # items pushed to frontier
    max_frontier = 1

    while frontier:
        max_frontier = max(max_frontier, len(frontier))
        _, current, path = heapq.heappop(frontier)

        if current in visited:
            continue
        visited.add(current)
        expanded += 1

        if current == goal:
            t1 = time.perf_counter()
            if return_metrics:
                return path, {
                    "found": True,
                    "expanded": expanded,
                    "visited": len(visited),
                    "enqueued": enqueued,
                    "max_frontier": max_frontier,
                    "time_sec": t1 - t0,
                }
            return path

        # graph is {city: {neighbor: distance, ...}, ...}
        for neighbor, _cost in graph.get(current, {}).items():
            if neighbor not in visited:
                heapq.heappush(frontier, (heuristic(neighbor, goal), neighbor, path + [neighbor]))
                enqueued += 1

    # No path
    t1 = time.perf_counter()
    if return_metrics:
        return [], {
            "found": False,
            "expanded": expanded,
            "visited": len(visited),
            "enqueued": enqueued,
            "max_frontier": max_frontier,
            "time_sec": t1 - t0,
        }
    return []
