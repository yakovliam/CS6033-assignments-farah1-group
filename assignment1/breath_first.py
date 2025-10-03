import time
from collections import deque
from typing import Dict, List, Tuple, Optional

Graph = Dict[str, Dict[str, float]]

def bfs(
    graph: Graph,
    start: str,
    goal: str,
    *,
    return_metrics: bool = False
) -> List[str] | Tuple[List[str], dict]:
    """
    Breadth-First Search with optional metrics.
    Returns path or (path, metrics) if return_metrics=True.
    """
    t0 = time.perf_counter()

    if start == goal:
        t1 = time.perf_counter()
        if return_metrics:
            return [start], {
                "found": True,
                "expanded": 0,
                "visited": 1,      # start only
                "enqueued": 1,     # start
                "max_frontier": 1, # queue size
                "time_sec": t1 - t0,
            }
        return [start]

    queue = deque([(start, [start])])
    seen = {start}

    # metrics
    expanded = 0
    enqueued = 1
    max_frontier = 1

    while queue:
        max_frontier = max(max_frontier, len(queue))
        current_city, path = queue.popleft()
        expanded += 1  

        if current_city == goal:
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

        
        for neighbor in graph.get(current_city, {}).keys():
            if neighbor not in seen:
                seen.add(neighbor)
                queue.append((neighbor, path + [neighbor]))
                enqueued += 1


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
