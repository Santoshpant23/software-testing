### Continue filling out the readme 

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

Empty List OR A List that meets the following criteria:

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

[>1, 1, N, >0, >1]  7) [[INIT, N1], [N1, N3], [INIT, N2], [N2, N3], [N3, TERM]]  

[1, >1, N, >0, >1]   8)  [[INIT, N1], [N1, N2], [N2, N4], [N1, N3], [N3, TERM], [N4, TERM]]


