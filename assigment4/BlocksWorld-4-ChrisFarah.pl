

blocks([a,b,c,d]).
block(X) :- blocks(BS), member(X, BS).

% START and GOAL facts 
start([
  [on,a,b],
  [on,b,table],
  [on,c,d],
  [clear,c],
  [clear,a],
  [on,d,table]
]).
goal([
  [on,d,a],
  [on,a,c],
  [on,c,b],
  [on,b,table],
  [clear,d]
]).

% Helpers 
notequal(X,X) :- !, fail.
notequal(_,_)  :- true.

% substitute one occurrence
substitute(X, Y, [X|T], [Y|T]) :- !.
substitute(X, Y, [H|T], [H|T1]) :- substitute(X, Y, T, T1).

% delete exactly one occurrence
delete_one(X, [X|T], T) :- !.
delete_one(X, [H|T], [H|T1]) :- delete_one(X, T, T1).

% add if absent
add_if_absent(E, L, L) :- member(E, L), !.
add_if_absent(E, L, [E|L]).

canonical(S, CS) :- sort(S, CS).

goal_true(S) :-
  goal(G),
  canonical(S, CS),
  canonical(G, CG),
  CS == CG.

notYetVisited(S, VisCanon) :-
  canonical(S, CS),
  \+ member(CS, VisCanon).

% Moves 
% Move X from block Y onto clear block Z
move_blk_to_blk(X, Y, Z, S1, S2) :-
  member([clear, X], S1),
  member([on, X, Y], S1), block(Y),
  member([clear, Z], S1), block(Z), notequal(X, Z),
  substitute([on, X, Y], [on, X, Z], S1, INT),
  substitute([clear, Z], [clear, Y], INT, S2).

% Move X from block Y onto table
move_blk_to_table(X, Y, S1, S2) :-
  member([clear, X], S1),
  member([on, X, Y], S1), block(Y),
  substitute([on, X, Y], [on, X, table], S1, INT1),
  add_if_absent([clear, Y], INT1, S2).

% Move X from table onto clear block Y
move_table_to_blk(X, Y, S1, S2) :-
  member([clear, X], S1),
  member([on, X, table], S1),
  member([clear, Y], S1), block(Y), notequal(X, Y),
  substitute([on, X, table], [on, X, Y], S1, INT1),
  delete_one([clear, Y], INT1, S2).

% Successors (no symmetry)
succ(S1, S2) :- move_blk_to_blk(_, _, _, S1, S2).
succ(S1, S2) :- move_blk_to_table(_, _,    S1, S2).
succ(S1, S2) :- move_table_to_blk(_, _,    S1, S2).

% DFS on canonical states 
depthFirst(S, [S], _) :- goal_true(S).
depthFirst(S, [S|Path], VisCanon) :-
  succ(S, S2),
  notYetVisited(S2, VisCanon),
  canonical(S2, C2),
  depthFirst(S2, Path, [C2|VisCanon]).

solve(Path) :-
  start(S0),
  canonical(S0, C0),
  depthFirst(S0, Path, [C0]).

% Pretty print
print_state([]) :- nl.
print_state([[on,A,B]|T]) :- format("on(~w,~w)~n",[A,B]), print_state(T).
print_state([[clear,A]|T]) :- format("clear(~w)~n",[A]),   print_state(T).
print_state([H|T])         :- format("~w~n",[H]),          print_state(T).

print_path([]).
print_path([S|T]) :-
  writeln('--- state ---'),
  print_state(S),
  print_path(T).