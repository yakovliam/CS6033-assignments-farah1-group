import heapq

def a_star_search(graph, start, goal, heuristic):
    """
    A* Search.
    Expands the node with the lowest f(n) = g(n) + h(n).
    Returns the path from start to goal or [] if no path exists.
    """
    frontier = [(heuristic(start, goal), 0, start, [start])]  # (f, g, node, path)
    visited = {}

    while frontier:
        f, g, current, path = heapq.heappop(frontier)

        if current == goal:
            return path

        if current in visited and visited[current] <= g:
            continue
        visited[current] = g

        for neighbor, cost in graph.get(current, []):
            g_new = g + cost
            f_new = g_new + heuristic(neighbor, goal)
            heapq.heappush(frontier, (f_new, g_new, neighbor, path + [neighbor]))

    return []

