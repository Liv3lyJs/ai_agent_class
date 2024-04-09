:- writeln('Prolog file loaded successfully.').
main(List, IndexL):-
	nb_couleurs(List, NbCouleurs),
	ask_questions(List, NbCouleurs,IndexNum),
	index_conv(IndexNum,IndexL).
	
%---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
nb_couleurs(List, Count):-
    nb_couleurs(List, -1, Count).
nb_couleurs([], Count, Count).
nb_couleurs([''|_], Count, Count).
nb_couleurs([_|Rest], Acc, Count) :-
    NewAcc is Acc + 1,
    nb_couleurs(Rest, NewAcc, Count).

%---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
ask_questions([Handle,First,Second,Third|_], 3, IndexNum) :-
	firstQ3([Handle,First,Second,Third], IndexNum);
	secondQ3([Handle,First,Second,Third], IndexNum);
	thirdQ3([Handle,First,Second,Third], IndexNum);
    IndexNum is 2.

ask_questions([Handle,First,Second,Third,Fourth|_], 4, IndexNum):-
    firstQ4([Handle,First,Second,Third,Fourth], IndexNum);
    secondQ4([Handle,First,Second,Third,Fourth], IndexNum);
    thirdQ4([Handle,First,Second,Third,Fourth], IndexNum);
    fourthQ4([Handle,First,Second,Third,Fourth], IndexNum);
    IndexNum is 2.
ask_questions([Handle,First,Second,Third,Fourth,Fifth|_], 5, IndexNum):-
    firstQ5([Handle,First,Second,Third,Fourth,Fifth], IndexNum);
    secondQ5([Handle,First,Second,Third,Fourth,Fifth], IndexNum);
    thirdQ4([Handle,First,Second,Third,Fourth,Fifth], IndexNum);
    IndexNum is 1.
ask_questions(List, 6, IndexNum):-
    firstQ6(List, IndexNum);
    secondQ6(List, IndexNum);
    thirdQ6(List, IndexNum);
    IndexNum is 4.
%---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
firstQ3(List, IndexNum):-
	not(contains_color(List, 'red')),
	IndexNum is 2.
%---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
secondQ3(List,IndexNum):-
	last_color(List, 'white'),
	IndexNum is 3.
%---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
thirdQ3(List, IndexNum):-
	minimum_occurrence_color(List,'blue',2),
    last_occurrence(List, 'blue', IndexNum).
%---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
firstQ4(List, IndexNum):-
    minimum_occurrence_color(List,'red',2),
    serrure_color(List, 'silver'),
    last_occurrence(List, 'red', IndexNum).
%---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
secondQ4(List, IndexNum):-
    last_color(List,'yellow'),
    not(contains_color(List, 'red')),
    IndexNum is 1.
%---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
thirdQ4(List, IndexNum):-
    count_color(List, 'blue', 1),
    IndexNum is 1.
%---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
fourthQ4(List, IndexNum):-
    minimum_occurrence_color(List,'yellow',2),
    IndexNum is 4.
%---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------  
firstQ5(List, IndexNum):-
    last_color(List,'black'),
    serrure_color(List, 'gold'),
    IndexNum is 4.
%---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------  
secondQ5(List, IndexNum):-
    count_color(List, 'red', 1),
    minimum_occurrence_color(List, 'yellow', 2),
    IndexNum is 1.
%---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------  
thirdQ5(List, IndexNum):-
    not(contains_color(List, 'black')),
    IndexNum is 2.
%---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------  

firstQ6(List, IndexNum):-
	not(contains_color(List, 'yellow')),
    serrure_color(List, 'bronze'),
	IndexNum is 3.
%---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
secondQ6(List, IndexNum):-
	count_color(List, 'yellow', 1),
    minimum_occurrence_color(List,'white',2),
	IndexNum is 4.
%---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
thirdQ6(List, IndexNum):-
	not(contains_color(List, 'red')),
	IndexNum is 6.
%---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
% P'red'ICATES CALLED BY QUESTIONS :
%---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
last_color([_|Rest],Color):-
    last_color(Rest,Color).
last_color([Color],Color).

%---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
serrure_color([First|_],Color):-
    First = Color.
%---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
last_occurrence(List, Value, Index) :-
    last_occurrence_helper(List, Value, 1, 0, Index).

last_occurrence_helper([], _, _, Index, Index).
last_occurrence_helper([H|T], Value, CurrentIndex, _, Index) :-
    H = Value,
    NextIndex is CurrentIndex + 1,
    last_occurrence_helper(T, Value, NextIndex, CurrentIndex, Index).
last_occurrence_helper([H|T], Value, CurrentIndex, LastIndex, Index) :-
    H \= Value,
    NextIndex is CurrentIndex + 1,
    last_occurrence_helper(T, Value, NextIndex, LastIndex, Index).

%---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
contains_color([], _) :-
    fail. 
contains_color([Color|_], Color).
contains_color([_|Rest], Color) :-
    contains_color(Rest, Color).

%---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
count_color([], _, 0).
count_color([Color],Color,1).
count_color([Color|Rest], Color, Count) :-
    count_color(Rest, Color, SubCount),
    Count is SubCount + 1.
count_color([OtherColor|Rest], Color, Count) :-
    Color \= OtherColor,
    count_color(Rest, Color, Count).

%---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
% Define a p'red'icate to check if there are at least N occurrences of a color
minimum_occurrence_color(List, Color, N) :-
    count_color(List, Color, Count),
    Count >= N.

%---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
index_conv(1, 'first').
index_conv(2, 'second').
index_conv(3, 'third').
index_conv(4, 'fourth').
index_conv(5, 'fifth').
index_conv(6, 'sixth').

	