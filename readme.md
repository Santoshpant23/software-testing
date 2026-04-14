Continue filling out the readme 

Dependencies?



Criteria for the Graph Coverage Criteria App:

Relationship [Node, Edges]
How to represent that?

List of Lists -- 

Terminal Node 
[Node, $]


Initial Node 







Category Partition 
1 Input: Type List

Empty List OR
A List that meets the following criteria:

INIT: 0, 1, >1
TERM: 0, 1, >1
LOOPS: None, Self, Circuit
EDGE: 0, >0
NODE: 1, >1

Constraints:
If Edge = 0, Loop == None
If Node = 1, Term == 0 || Term == 1
If Node = 1, Init == 0 || Init == 1

Lists:
ADD HERE
[Empty List] 1) => Error
[I,T,L,E,N]  
[1,1,N,0,1]  2) [[INIT, N],[N, TERM]]
[1,1,S,>0,1]  3) [[INIT, N],[N,N] [N, TERM]]
[1,1,C,>0,>1] 4) [[INIT, N1],[N1,N2],[N2,N3],[N3,N4],[N4,N2],[N2, TERM]]
[0,0,S,>0,1]  5)[[N,N]] => Error
[1,1,C,>0,>1] 6)[[INIT, N1],[N1,N5],[N5,N5],[N5,N7],[N7,TERM]] - Duplicate

[0,0,N,0,0]
[0,0,S,1,1]
[1,1,N,0,1]
[1,0,C,>0,>1]
[>1,1,N,>0,1]
[>1,>1,N,>0,>1]

#Kacy Part

1) [1,1,N,>0,>1] : [[INIT, N1], [N2, TERM]]
2) [1,1,N,>0,>1] : [[INIT, N1], [N1, N2], [N3, TERM]] -> Error
3) [>1,1,N,>0,>1] : [[INIT, N1], [INIT, N2], [N1, TERM]] (this is because N2 cant come to TERM)
4) [1,0,S,>0,1] : [[INIT, N], [N, N]] (self-loop but without termination)
5) [1,0,C,>0,>1]: [[INIT, N1], [N1, N2], [N2, N1]] -> Error (Cycle but without term
6) [[INIT, N], [N, N]] -> Error (Infinite Self Loop)
7) [[INIT, A], [A, B], [C, D], [D, C]] -> Error (It is so disconnected I would say and without term)
   



