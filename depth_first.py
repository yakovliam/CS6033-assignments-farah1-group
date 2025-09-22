def depth_first_search(graph, start, goal):

    def iter_neighbors(node):
        nbrs = graph.get(node, {})
        if isinstance(nbrs, dict):
            return list(nbrs.keys())
        if isinstance(nbrs, (list, tuple)):
            if nbrs and isinstance(nbrs[0], tuple):
                return [n for (n, *_) in nbrs]
            return list(nbrs)
        return []

    stack = [(start, [start])]
    visited = set()

    while stack:
        node, path = stack.pop()
        if node in visited:
            continue
        visited.add(node)

        if node == goal:
            return path

        for nbr in reversed(iter_neighbors(node)):
            if nbr not in visited:
                stack.append((nbr, path + [nbr]))

    return []
