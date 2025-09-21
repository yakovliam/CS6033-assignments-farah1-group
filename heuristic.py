# Straight-line distances (SLD) to Bucharest
sld_to_bucharest = {
    "Arad": 366,
    "Bucharest": 0,
    "Craiova": 160,
    "Dobreta": 242,
    "Eforie": 161,
    "Fagaras": 176,
    "Giurgiu": 77,
    "Hirsova": 151,
    "Iasi": 226,
    "Lugoj": 244,
    "Mehadia": 241,
    "Neamt": 234,
    "Oradea": 380,
    "Pitesti": 100,
    "Rimnicu Vilcea": 193,
    "Sibiu": 253,
    "Timisoara": 329,
    "Urziceni": 80,
    "Vaslui": 199,
    "Zerind": 374
}

def heuristic(city, goal):
    """
    Returns an estimated distance from `city` to `goal`.

    If goal == Bucharest -> uses known SLD values.
    Otherwise -> uses a simple triangle inequality approximation:
                 h(city, goal) = |h(city, Bucharest) - h(goal, Bucharest)|
    """
    if goal == "Bucharest":
        return sld_to_bucharest.get(city, float("inf"))

    # If goal is not Bucharest, approximate using triangle inequality
    h_city = sld_to_bucharest.get(city, float("inf"))
    h_goal = sld_to_bucharest.get(goal, float("inf"))

    # Simple absolute difference heuristic (always admissible)
    return abs(h_city - h_goal)

# Example adjacency list snippet
graph = {
    "Arad": [("Zerind", 75), ("Sibiu", 140), ("Timisoara", 118)],
    "Zerind": [("Arad", 75), ("Oradea", 71)],
    "Sibiu": [("Arad", 140), ("Oradea", 151), ("Fagaras", 99), ("Rimnicu Vilcea", 80)],
    # ... add the rest
}

# Run Best-First Search
path_greedy = best_first_search(graph, "Arad", "Bucharest", heuristic)
print("Best-First Path:", path_greedy)

# Run A* Search
path_astar = a_star_search(graph, "Arad", "Bucharest", heuristic)
print("A* Path:", path_astar)

