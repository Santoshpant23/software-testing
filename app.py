class Testing:
    def __init__(self, edges) -> None:
        self.edges = edges
        self.simple_paths = []
        self.prime_paths = []
        self.relationship = {}
        self.make_relationship()
    
    def make_relationship(self):
        for edge in self.edges:
            f = edge[0]
            t = edge[1]
            if f not in self.relationship:
                self.relationship[f] = []
            self.relationship[f].append(t)
    
    def get_relationship(self):
        print(self.relationship)

    def find_paths(self):
        if self.simple_paths:
            return [self.simple_paths, self.prime_paths]
        else:
            # Find all simple paths using DFS
            for start_node in self.relationship.keys():
                visited = set()
                self.dfs_simple_paths(start_node, "", visited)
            
            # Find prime paths (maximal simple paths)
            self.find_prime_paths()
            return [self.simple_paths, self.prime_paths]
    
    def dfs_simple_paths(self, node, current_path, visited):
        """Find all simple paths (no repeated nodes) using DFS"""
        current_path += str(node)
        visited.add(node)
        
        self.simple_paths.append(current_path)
        # If node has no outgoing edges, it's a complete path
        if node not in self.relationship or not self.relationship[node]:
            return
        else:
            for neighbor in self.relationship[node]:
                if neighbor not in visited:
                    can_extend = True
                    self.dfs_simple_paths(neighbor, current_path, visited.copy())
                else:
                    # this is loop, must be prime path
                    self.prime_paths.append(current_path+str(neighbor))
            
            # If we can't extend further, this is an ending path
    
    def find_prime_paths(self):
        # Remove duplicates from simple_paths + the subsets, that is it :)
        unique_simple_paths = list(set(self.simple_paths))
        
        # cycle is already handled in simple paths:
        # now check if any given is subset of any other, else this is a prime path
        for i in range(len(self.simple_paths)):
            curr = self.simple_paths[i]
            found = False
            for j in range(len(self.simple_paths)):
                inner = self.simple_paths[j]
                if i != j and len(curr) < len(inner):
                    # now only check for subset
                    if inner.find(curr)!=-1:
                        # curr is a subset, so we just exit the loop
                        found = True
                        break
            if not found:
                self.prime_paths.append(curr)



    
    def return_paths(self):
        print(self.simple_paths, "<-- Simple Paths")
        print(self.prime_paths, "<-- Prime Paths")
        return
        


test = Testing([[1, 2], [2, 3], [2, 4], [4, 5], [5, 2]])
test.get_relationship()
test.find_paths()
test.return_paths()
