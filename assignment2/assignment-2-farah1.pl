/* 
 * Farah1 Group
 * Jacob Cohen, Chris Farah, Eric Braverman, Sujal Choukse
 */

/* RANDOM LIST GENERATION */
:- dynamic(random_list/2).
:- dynamic(test_result/3).

/* Generate a random list of N elements between 1-1000 */
randomList(0, []) :- !.
randomList(N, [X|T]) :-
    N > 0,
    random(1, 1000, X),
    N1 is N - 1,
    randomList(N1, T).

/* Generate and store 50 random lists */
generate_test_lists :-
    retractall(random_list(_,_)),
    forall(
        between(1, 50, I),
        (
            random_between(5, 50, Length),
            randomList(Length, List),
            assertz(random_list(I, List)),
            format('Generated list ~w: ~w~n', [I, List])
        )
    ).

/* BUBBLE SORT */
swap([X, Y|T], [Y, X|T]) :- Y < X.
swap([H|T], [H|T1]) :- swap(T, T1).

bubbleSort(L, SL) :-
    swap(L, L1), !,
    bubbleSort(L1, SL).
bubbleSort(L, L).

/* INSERTION SORT */
ordered([]).
ordered([_]).
ordered([H1, H2|T]) :- H1 =< H2, ordered([H2|T]).

insert(X, [], [X]).
insert(E, [H|T], [E,H|T]) :- E =< H, !.
insert(E, [H|T], [H|T1]) :- insert(E, T, T1).

insertionSort([], []).
insertionSort([H|T], SORTED) :-
    insertionSort(T, T1),
    insert(H, T1, SORTED).

/* MERGE SORT */
intDiv(N, N1, R) :- R is div(N, N1).

split_in_half([], [], []).
split_in_half([X], [], [X]).
split_in_half(L, L1, L2) :-
    length(L, N),
    intDiv(N, 2, N1),
    length(L1, N1),
    append(L1, L2, L).

merge([], L, L).
merge(L, [], L).
merge([H1|T1], [H2|T2], [H1|T]) :-
    H1 =< H2,
    merge(T1, [H2|T2], T).
merge([H1|T1], [H2|T2], [H2|T]) :-
    H2 < H1,
    merge([H1|T1], T2, T).

mergeSort([], []).
mergeSort([X], [X]) :- !.
mergeSort(L, SL) :-
    split_in_half(L, L1, L2),
    mergeSort(L1, S1),
    mergeSort(L2, S2),
    merge(S1, S2, SL).

/* QUICK SORT */
split(_, [], [], []).
split(X, [H|T], [H|SMALL], BIG) :-
    H =< X,
    split(X, T, SMALL, BIG).
split(X, [H|T], SMALL, [H|BIG]) :-
    X < H,
    split(X, T, SMALL, BIG).

quickSort([], []).
quickSort([H|T], SORTED) :-
    split(H, T, SMALL, BIG),
    quickSort(SMALL, S),
    quickSort(BIG, B),
    append(S, [H|B], SORTED).

/* HYBRID SORT */
hybridSort(LIST, SMALLALG, _BIGALG, THRESHOLD, SLIST) :-
    length(LIST, N), N =< THRESHOLD,
    call(SMALLALG, LIST, SLIST).

hybridSort(LIST, SMALLALG, mergeSort, THRESHOLD, SLIST) :-
    length(LIST, N), N > THRESHOLD,
    split_in_half(LIST, L1, L2),
    hybridSort(L1, SMALLALG, mergeSort, THRESHOLD, S1),
    hybridSort(L2, SMALLALG, mergeSort, THRESHOLD, S2),
    merge(S1, S2, SLIST).

hybridSort(LIST, SMALLALG, quickSort, THRESHOLD, SLIST) :-
    length(LIST, N), N > THRESHOLD,
    LIST = [H|T],
    split(H, T, SMALL, BIG),
    hybridSort(SMALL, SMALLALG, quickSort, THRESHOLD, S),
    hybridSort(BIG, SMALLALG, quickSort, THRESHOLD, B),
    append(S, [H|B], SLIST).

/* TESTING - Hybrid helper predicates */
hybrid_bubble_merge(List, Sorted) :- hybridSort(List, bubbleSort, mergeSort, 10, Sorted).
hybrid_bubble_quick(List, Sorted) :- hybridSort(List, bubbleSort, quickSort, 10, Sorted).
hybrid_insertion_merge(List, Sorted) :- hybridSort(List, insertionSort, mergeSort, 10, Sorted).
hybrid_insertion_quick(List, Sorted) :- hybridSort(List, insertionSort, quickSort, 10, Sorted).

/* Run all tests successfully */
run_all_tests :-
    format('Starting tests...~n'),
    retractall(test_result(_,_,_)),
    generate_test_lists,
    forall(
        between(1, 50, ListNum),
        (
            random_list(ListNum, List),
            format('Testing list ~w (length: ~w)~n', [ListNum, length(List)]),
            test_algorithm(ListNum, List, bubbleSort),
            test_algorithm(ListNum, List, insertionSort),
            test_algorithm(ListNum, List, mergeSort),
            test_algorithm(ListNum, List, quickSort),
            test_algorithm(ListNum, List, hybrid_bubble_merge),
            test_algorithm(ListNum, List, hybrid_bubble_quick),
            test_algorithm(ListNum, List, hybrid_insertion_merge),
            test_algorithm(ListNum, List, hybrid_insertion_quick)
        )
    ),
    format('All tests completed!~n').

test_algorithm(ListNum, List, Algorithm) :-
    catch(
        (statistics(cputime, T0),
         call(Algorithm, List, Sorted),
         statistics(cputime, T1),
         Time is T1 - T0,
         assertz(test_result(ListNum, Algorithm, Time)),
         format('  ~w: ~6f seconds~n', [Algorithm, Time])),
        Error,
        (format('  ERROR in ~w: ~w~n', [Algorithm, Error]),
         assertz(test_result(ListNum, Algorithm, 0)))
    ).

/* Analyze results */
analyze_results :-
    format('~n=== PERFORMANCE ANALYSIS ===~n'),
    findall(Algorithm, test_result(_, Algorithm, _), Algorithms),
    sort(Algorithms, UniqueAlgorithms),
    forall(
        member(Alg, UniqueAlgorithms),
        (
            findall(Time, test_result(_, Alg, Time), Times),
            sum_list(Times, TotalTime),
            length(Times, Count),
            Average is TotalTime / Count,
            format('Algorithm ~w: Average time = ~6f seconds over ~d tests~n', [Alg, Average, Count])
        )
    ).

/* Quick test function */
quick_test :-
    format('Running quick test with sample list...~n'),
    SampleList = [3, 1, 4, 1, 5, 9, 2, 6, 5],
    format('Original list: ~w~n', [SampleList]),
    
    bubbleSort(SampleList, BSorted), format('BubbleSort: ~w~n', [BSorted]),
    insertionSort(SampleList, ISorted), format('InsertionSort: ~w~n', [ISorted]),
    mergeSort(SampleList, MSorted), format('MergeSort: ~w~n', [MSorted]),
    quickSort(SampleList, QSorted), format('QuickSort: ~w~n', [QSorted]),
    hybrid_bubble_merge(SampleList, HBM), format('Hybrid Bubble+Merge: ~w~n', [HBM]),
    hybrid_bubble_quick(SampleList, HBQ), format('Hybrid Bubble+Quick: ~w~n', [HBQ]),
    hybrid_insertion_merge(SampleList, HIM), format('Hybrid Insertion+Merge: ~w~n', [HIM]),
    hybrid_insertion_quick(SampleList, HIQ), format('Hybrid Insertion+Quick: ~w~n', [HIQ]).