% Farah1 Group Implementation
% author: Jacob Cohen
% Group: Chris Farah, Jacob Cohen, Eric Braverman, Sujal Choukse

% Define the blocks in our world
blocks([a, b, c, d]).

% Generic block predicate
block(X) :-
    blocks(BLOCKS),
    member(X, BLOCKS).

% Start state: a on b, b on table, c on d, c clear, a clear, d on table
start([[on, a, b], [on, b, "table"], [on, c, d], [clear, c], [clear, a], [on, d, "table"]]).

% Goal state: d on a, a on c, c on b, b on table, d clear
goal([[on, d, a], [on, a, c], [on, c, b], [on, b, "table"], [clear, d]]).

% notequal predicate using cut-fail combination
notequal(X, X) :- !, fail.
notequal(_, _).

% substitute predicate - replaces element E with E1 in list OLD to produce NEW
substitute(X, Y, [X|T], [Y|T]).
substitute(X, Y, [H|T], [H|T1]) :-
    substitute(X, Y, T, T1).

% Rule 2: Move clear block X from block Y onto clear block Z
move(X, Y, Z, S1, S2) :-
    member([clear, X], S1),
    member([on, X, Y], S1), 
    block(Y),
    member([clear, Z], S1), 
    notequal(X, Z),
    substitute([on, X, Y], [on, X, Z], S1, INT),
    substitute([clear, Z], [clear, Y], INT, S2).

% Rule 3: Move clear block X from block Y onto table
move_table_from_block(X, Y, S1, S2) :-
    member([clear, X], S1),
    member([on, X, Y], S1),
    block(Y),
    substitute([on, X, Y], [on, X, "table"], S1, INT),
    substitute([clear, X], [clear, Y], INT, S2).

% Rule 4: Move clear block X from table onto clear block Y
move_table_to_block(X, Y, S1, S2) :-
    member([clear, X], S1),
    member([on, X, "table"], S1),
    member([clear, Y], S1),
    block(Y),
    notequal(X, Y),
    substitute([on, X, "table"], [on, X, Y], S1, INT),
    substitute([clear, Y], [clear, X], INT, S2).

% Generic move predicate that handles all three move types
move(S1, S2) :-
    move(X, Y, Z, S1, S2).
move(S1, S2) :-
    move_table_from_block(X, Y, S1, S2).
move(S1, S2) :-
    move_table_to_block(X, Y, S1, S2).

% Path predicate - there is a path from S1 to S2 if there's a move
path(S1, S2) :-
    move(S1, S2).

% Connect predicate - symmetric version of path
connect(S1, S2) :-
    path(S1, S2).
connect(S1, S2) :-
    path(S2, S1).

% Check if a state has not been visited (considering permutations)
notYetVisited(State, PathSoFar) :-
    \+ (permutation(State, PermutedState), member(PermutedState, PathSoFar)).

% Depth-first search implementation
depthFirst(X, [X], _) :- 
    goal(X).

depthFirst(X, [X|Ypath], VISITED) :- 
    connect(X, Y),
    notYetVisited(Y, VISITED),
    depthFirst(Y, Ypath, [Y|VISITED]).

% Wrapper predicate to start the search
solve(Path) :-
    start(StartState),
    depthFirst(StartState, Path, [StartState]).

% Helper predicate to display a state nicely
display_state(State) :-
    format('State: ~n'),
    member(Constraint, State),
    format('  ~w~n', [Constraint]),
    fail.
display_state(_).

% Display solution path
display_solution([]).
display_solution([State|Rest]) :-
    display_state(State),
    (Rest = [] -> format('=== GOAL REACHED ===~n~n'); 
     format('  |~n  v~n~n')),
    display_solution(Rest).

% Test with different initial and goal states for verification
test_start([[on, a, "table"], [on, b, "table"], [on, c, "table"], 
            [clear, a], [clear, b], [clear, c]]).
test_goal([[on, a, b], [on, b, c], [on, c, "table"], 
           [clear, a]]).

% Test solver
test_solve(Path) :-
    test_start(Start),
    test_goal(Goal),
    retractall(start(_)),
    retractall(goal(_)),
    assert(start(Start)),
    assert(goal(Goal)),
    solve(Path).
