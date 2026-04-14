ReadMe for app.py

Test Cases:
1) []-> An error/invalid case
2) [[Init,Node],[Node,Term]]-> For a graph with in input size of 1
3) [[Init,Node],[Node,Self-loop],[Self-loop,Term]]-> Traversal of 1,5,5,7
4) [[Init,Node],[Node,Node],[Node,Node],[Node,Loop]]-> 
        Traversal of cycle (2,3,4,2),(3,4,2,3),(4,2,3,4)
5) [[Init,node],[node,node],[node,term]]-> 5,5* (cycle)

