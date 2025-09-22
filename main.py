import argparse
from collections import deque
import breath_first
import astar
import bfs_greedy
import depth_first
CITIES = [
    "Oradea","Zerind","Arad","Timisoara","Lugoj","Mehadia","Drobeta","Craiova",
    "Rimnicu Vilcea","Sibiu","Fagaras","Pitesti","Bucharest","Giurgiu",
    "Urziceni","Hirsova","Eforie","Vaslui","Iasi","Neamt"
]
ID_BY_NAME = {name: i for i, name in enumerate(CITIES)}

GRAPH = {name: {} for name in CITIES}

def add_road(a, b, d):
    GRAPH[a][b] = d
    GRAPH[b][a] = d 

add_road("Arad", "Zerind", 75)
add_road("Arad", "Sibiu", 140)
add_road("Arad", "Timisoara", 118)
add_road("Zerind", "Oradea", 71)
add_road("Oradea", "Sibiu", 151)
add_road("Timisoara", "Lugoj", 111)
add_road("Lugoj", "Mehadia", 70)
add_road("Mehadia", "Drobeta", 75)
add_road("Drobeta", "Craiova", 120)
add_road("Craiova", "Rimnicu Vilcea", 146)
add_road("Craiova", "Pitesti", 138)
add_road("Rimnicu Vilcea", "Sibiu", 80)
add_road("Rimnicu Vilcea", "Pitesti", 97)
add_road("Sibiu", "Fagaras", 99)
add_road("Fagaras", "Bucharest", 211)
add_road("Pitesti", "Bucharest", 101)
add_road("Bucharest", "Giurgiu", 90)
add_road("Bucharest", "Urziceni", 85)
add_road("Urziceni", "Hirsova", 98)
add_road("Hirsova", "Eforie", 86)
add_road("Urziceni", "Vaslui", 142)
add_road("Vaslui", "Iasi", 92)
add_road("Iasi", "Neamt", 87)

SLD_TO_BUCHAREST = {
    "Arad": 366, "Bucharest": 0, "Craiova": 160, "Drobeta": 242, "Eforie": 161,
    "Fagaras": 176, "Giurgiu": 77, "Hirsova": 151, "Iasi": 226, "Lugoj": 244,
    "Mehadia": 241, "Neamt": 234, "Oradea": 380, "Pitesti": 100, "Rimnicu Vilcea": 193,
    "Sibiu": 253, "Timisoara": 329, "Urziceni": 80, "Vaslui": 199, "Zerind": 374
}

def main():
    print("started")
    parser = argparse.ArgumentParser()
    parser.add_argument("start", choices=CITIES,  help="Starting city")
    parser.add_argument("goal", choices=CITIES, help="Goal city")
    parser.add_argument("algorithm", choices=["bfs", "a_star", "dfs","bfs_greedy"], help="Search algorithm to use")
    args = parser.parse_args()
    start = args.start
    goal = args.goal
    if args.algorithm == "bfs":
        print("Using BFS")
        #implement BFS
    if args.algorithm == "a_star":
        print("Using A*")
        #implement A*
    if args.algorithm == "dfs":
        print("Using DFS")
        path = depth_first.depth_first_search(GRAPH, start, goal)
        print("DFS path:", " -> ".join(path) if path else "No path")
    if args.algorithm == "bfs_greedy":
        print("Using BFS Greedy")
        #implement BFS with Greedy 

if __name__ == "__main__":
    main()

# Example usage:
# python3 main.py Arad Bucharest bfs
