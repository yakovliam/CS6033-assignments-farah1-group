import heapq
import time
from typing import Dict, List, Tuple, Callable

Graph = Dict[str, Dict[str, float]]
Heuristic = Callable[[str, str], float]

def a_star_search(
    graph: Graph,
    start: str,
    goal: str,
    heuristic: Heuristic,
    *,
    return_metrics: bool = False
) -> List[str] | Tuple[List[str], dict]:
    """
    A* Search.
    Expands node with the lowest f(n) = g(n) + h(n).
    Returns path or (path, metrics) if return_metrics=True.
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

    # heap items: (f, g, node, path)
    start_h = heuristic(start, goal)
    frontier: List[Tuple[float, float, str, List[str]]] = [(start_h, 0.0, start, [start])]
    g_score: Dict[str, float] = {start: 0.0}
    seen = set([start])  # for metrics only

    # metrics
    expanded = 0
    enqueued = 1
    max_frontier = 1

    while frontier:
        max_frontier = max(max_frontier, len(frontier))
        f, g, current, path = heapq.heappop(frontier)

        # If this entry is stale (we’ve since found a better g), skip it
        if g > g_score.get(current, float("inf")):
            continue

        expanded += 1
        if current == goal:
            t1 = time.perf_counter()
            if return_metrics:
                return path, {
                    "found": True,
                    "expanded": expanded,
                    "visited": len(seen),
                    "enqueued": enqueued,
                    "max_frontier": max_frontier,
                    "time_sec": t1 - t0,
                }
            return path

        # graph is {city: {neighbor: distance, ...}}
        for neighbor, cost in graph.get(current, {}).items():
            tentative_g = g + cost
            if tentative_g < g_score.get(neighbor, float("inf")):
                g_score[neighbor] = tentative_g
                seen.add(neighbor)
                new_path = path + [neighbor]
                f_new = tentative_g + heuristic(neighbor, goal)
                heapq.heappush(frontier, (f_new, tentative_g, neighbor, new_path))
                enqueued += 1

    # No path
    t1 = time.perf_counter()
    if return_metrics:
        return [], {
            "found": False,
            "expanded": expanded,
            "visited": len(seen),
            "enqueued": enqueued,
            "max_frontier": max_frontier,
            "time_sec": t1 - t0,
        }
    return []
