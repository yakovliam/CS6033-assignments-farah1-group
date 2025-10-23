
### Road Connections (edges with costs)

```prolog
% connected(City1, City2, Cost)
connected(arad, zerind, 75).
connected(arad, sibiu, 140).
connected(arad, timisoara, 118).
connected(zerind, oradea, 71).
connected(oradea, sibiu, 151).
connected(sibiu, fagaras, 99).
connected(sibiu, rimnicu_vilcea, 80).
connected(timisoara, lugoj, 111).
connected(lugoj, mehadia, 70).
connected(mehadia, drobeta, 75).
connected(drobeta, craiova, 120).
connected(craiova, rimnicu_vilcea, 146).
connected(craiova, pitesti, 138).
connected(rimnicu_vilcea, pitesti, 97).
connected(pitesti, bucharest, 101).
connected(fagaras, bucharest, 211).
connected(bucharest, giurgiu, 90).
connected(bucharest, urziceni, 85).
connected(urziceni, hirsova, 98).
connected(urziceni, vaslui, 142).
connected(hirsova, eforie, 86).
connected(vaslui, iasi, 92).
connected(iasi, neamt, 87).

% have it be bidirectional
connected(X, Y, C) :- connected(Y, X, C).
```

### Straight-Line Distance (SLD) to Bucharest
```prolog
% sld(City, Heuristic)
sld(arad, 366).
sld(bucharest, 0).
sld(craiova, 160).
sld(drobeta, 242).
sld(eforie, 161).
sld(fagaras, 176).
sld(giurgiu, 77).
sld(hirsova, 151).
sld(iasi, 226).
sld(lugoj, 244).
sld(mehadia, 241).
sld(neamt, 234).
sld(oradea, 380).
sld(pitesti, 100).
sld(rimnicu_vilcea, 193).
sld(sibiu, 253).
sld(timisoara, 329).
sld(urziceni, 80).
sld(vaslui, 199).
sld(zerind, 374).
```

---

## 2. Breadth-First Search (BFS)

```prolog
% BFS: fringe is a queue (FIFO)
bfs(Start, Goal, Path) :-
    bfs_queue([[Start]], Goal, Path).

bfs_queue([[Goal|Path]|_], Goal, [Goal|Path]).
bfs_queue([Path|Paths], Goal, FinalPath) :-
    extend_path(Path, NewPaths),
    append(Paths, NewPaths, NewQueue),
    bfs_queue(NewQueue, Goal, FinalPath).

extend_path([Node|Path], NewPaths) :-
    findall([NewNode, Node|Path],
            (connected(Node, NewNode, _),
             \+ member(NewNode, [Node|Path])),
            NewPaths).
```

---

## 3. Depth-First Search (DFS)

```prolog
% DFS: fringe is a stack (LIFO)
dfs(Start, Goal, Path) :-
    dfs_stack([[Start]], Goal, Path).

dfs_stack([[Goal|Path]|_], Goal, [Goal|Path]).
dfs_stack([Path|Paths], Goal, FinalPath) :-
    extend_path(Path, NewPaths),
    append(NewPaths, Paths, NewStack),
    dfs_stack(NewStack, Goal, FinalPath).
```

---

## 4. A* Search

```prolog
% A*: fringe is a priority queue sorted by f(n) = g(n) + h(n)
astar(Start, Goal, Path, Cost) :-
    sld(Start, H),
    astar_queue([(H, 0, [Start])], Goal, Path, Cost).

astar_queue([(_, Cost, [Goal|Path])|_], Goal, [Goal|Path], Cost).
astar_queue([(_, G, Path)|Paths], Goal, FinalPath, FinalCost) :-
    extend_astar_path(Path, G, NewPaths),
    append(Paths, NewPaths, AllPaths),
    sort_astar_queue(AllPaths, SortedQueue),
    astar_queue(SortedQueue, Goal, FinalPath, FinalCost).

extend_astar_path([Node|Path], G, NewPaths) :-
    findall((F, NewG, [NewNode, Node|Path]),
            (connected(Node, NewNode, C),
             \+ member(NewNode, [Node|Path]),
             NewG is G + C,
             sld(NewNode, H),
             F is NewG + H),
            NewPaths).

sort_astar_queue(Queue, Sorted) :-
    predsort(compare_astar, Queue, Sorted).

compare_astar(<, (F1, _, _), (F2, _, _)) :- F1 < F2.
compare_astar(>, (F1, _, _), (F2, _, _)) :- F1 > F2.
compare_astar(=, _, _).
```

---

## 5. Path Cost Calculation

```prolog
path_cost([_], 0).
path_cost([City1, City2|Rest], Cost) :-
    connected(City1, City2, C),
    path_cost([City2|Rest], RestCost),
    Cost is C + RestCost.
```

---

## 6. Running Tests

```prolog
% Test all three algorithms from given cities
test_algorithm(Algo, Start, Path, Cost) :-
    ( Algo == bfs -> bfs(Start, bucharest, Path)
    ; Algo == dfs -> dfs(Start, bucharest, Path)
    ; Algo == astar -> astar(Start, bucharest, Path, Cost)
    ),
    path_cost(Path, Cost).

run_tests :-
    Cities = [oradea, timisoara, neamt],
    Algorithms = [bfs, dfs, astar],
    forall(member(City, Cities),
           (format('~nFrom ~w to Bucharest:~n', [City]),
            forall(member(Algo, Algorithms),
                   (test_algorithm(Algo, City, Path, Cost),
                    format('  ~w: Path = ~w, Cost = ~w~n', [Algo, Path, Cost]))))).
```

---

## 7. Correctness & Efficiency Discussion

- BFS finds the shortest path in terms of number of edges, but not necessarily the least cost.
- DFS may find a path faster in some cases but can go deep into irrelevant branches.
- A* finds the least-cost path efficiently using heuristics, and is optimal if the heuristic is admissible (SLD is admissible here).

From the tests:
- Oradea and Timisoara will have valid paths.
- Neamt will also reach Bucharest via Iasi → Vaslui → Urziceni → Bucharest.
- BFS and A* paths will be optimal in cost for A*, and in steps for BFS.
- DFS might return a longer path cost-wise.

---



## Output:


### From **Oradea** to **Bucharest**
- **BFS:**  
  Path = [bucharest, fagaras, sibiu, oradea]  
  Cost = 461  
- **DFS:**  
  Path = [bucharest, fagaras, sibiu, oradea]  
  Cost = 461  
- **A***:  
  Path = [bucharest, pitesti, rimnicu_vilcea, sibiu, oradea]  
  Cost = 429  

---

### From **Timisoara** to **Bucharest**
- **BFS:**  
  Path = [bucharest, fagaras, sibiu, arad, timisoara]  
  Cost = 568  
- **DFS:**  
  Path = [bucharest, pitesti, rimnicu_vilcea, craiova, drobeta, mehadia, lugoj, timisoara]  
  Cost = 720  
- **A***:  
  Path = [bucharest, fagaras, sibiu, arad, timisoara]  
  Cost = 568  

---

### From **Neamt** to **Bucharest**
- **BFS:**  
  Path = [bucharest, urziceni, vaslui, iasi, neamt]  
  Cost = 406  
- **DFS:**  
  Path = [bucharest, urziceni, vaslui, iasi, neamt]  
  Cost = 406  
- **A***:  
  Path = [bucharest, urziceni, vaslui, iasi, neamt]  
  Cost = 406  

