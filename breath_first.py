

from collections import deque
from main import GRAPH


def bfs(graph, start, goal):
    if start == goal:
        print(f"Start is the same as goal: {start}")
        return

    queue = deque([(start, [start])])
    seen = {start}          # mark when enqueued

    while queue:
        current_city, path = queue.popleft()

        if current_city == goal:
            print("Path found:", " -> ".join(path))
            return

        for neighbor in graph[current_city]:
            if neighbor not in seen:
                seen.add(neighbor)  # prevent duplicate enqueues
                queue.append((neighbor, path + [neighbor]))

    print("No path found from", start, "to", goal)