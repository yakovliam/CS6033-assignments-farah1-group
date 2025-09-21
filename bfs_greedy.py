import heapq

def best_first_search(graph, start, goal, heuristic):
    """
    Greedy Best-First Search.
    Expands the node with the lowest heuristic h(n).
    Returns the path from start to goal or [] if no path exists.
    """
    frontier = [(heuristic(start, goal), start, [start])]
    visited = set()

    while frontier:
        _, current, path = heapq.heappop(frontier)

        if current == goal:
            return path

        if current in visited:
            continue
        visited.add(current)

        for neighbor, cost in graph.get(current, []):
            if neighbor not in visited:
                heapq.heappush(frontier, (heuristic(neighbor, goal), neighbor, path + [neighbor]))

    return []

