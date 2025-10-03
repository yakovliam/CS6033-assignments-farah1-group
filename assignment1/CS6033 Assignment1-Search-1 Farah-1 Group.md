# AI-I Assignment 1: Search

Instructor: Anca Ralescu  
Course: Artificial Intelligence

## Team Information

- Name(s): Jacob Cohen (cohen2jl), Chris Farah, Eric Braverman
- Contribution Statement: (e.g., All team members contributed in equal
  measure or Name A: 60%, Name B: 40%)

## Honor Statement

“In completing this assignment, all team members have followed the honor
pledge specified by the instructor for this course.”

## Bibliography

- List of sources used (or “None”).

# Report

## 1. Implementation Details

### 1.1 Data Representation

- How the Romanian road map was represented (adjacency matrix or
  adjacency list).
- Explanation of chosen representation and why.

### 1.2 Algorithms Implemented

- Breadth-First Search (BFS): description of queue strategy and
  expansion process.
- Depth-First Search (DFS): description of stack-like behavior.
- Best-First (Greedy): use of heuristic only.
- A\* Search: explanation of `f(n) = g(n) + h(n)` function.

### 1.3 Heuristic Functions

- Heuristic 1: Straight-Line Distance (SLD) to Bucharest (from
  textbook).
- Heuristic 2: SLD estimation for non-Bucharest goals using Triangle
  Inequality (Method 1).
- Heuristic 3: SLD estimation for non-Bucharest goals using Triangle
  Inequality (Method 2).
- Justification of admissibility/consistency or discussion of
  limitations.

## 2. Experimental Results

### 2.1 Correctness

- Table showing whether each algorithm successfully found paths between
  different start-goal pairs.
- Note cases where no path exists (empty result).

### 2.2 Efficiency

- Number of Cities Visited: for each algorithm.
- Execution Time: averaged across multiple runs.
- Space Usage: memory or fringe size if tracked.

Insert tables and/or graphs here.

## 3. Analysis and Comparison

### 3.1 Algorithm Comparison

- BFS vs DFS: differences in path length and nodes visited.
- Best-First vs A\*: effectiveness of heuristic use.

### 3.2 Heuristic Comparison

- Compare performance between the two triangle inequality heuristics.
- Discussion of accuracy, efficiency, and trade-offs.

### 3.3 Time & Space Complexity

- Theoretical complexity of each algorithm.
- Observed results compared to expected behavior.

## 4. Execution Instructions

- Programming language (Python/Matlab).
- Steps to run the code (e.g.,
  `python main.py ``start_city`` ``goal_city`).
- Required libraries or dependencies.

## Appendix (Optional)

- Sample outputs.
- Additional experiment results.
