class Testing:
    def __init__(self, edges) -> None:
        self.edges = edges
        self.simple_paths = []
        self.prime_paths = []
        self.relationship = {}
        self.init = 0
        self.term = 0
        self.make_relationship()
    
    def make_relationship(self):
        for edge in self.edges:
            f = edge[0]
            t = edge[1]
            if f == "INIT":
                self.init+=1
            if t == "TERM":
                self.term+=1
            if f != "INIT":
                if f not in self.relationship:
                    self.relationship[f] = []
                self.relationship[f].append(t)
    
    def get_relationship(self):
        print(self.relationship)

    def find_paths(self):
        if len(self.relationship.keys()) == 0:
            raise ValueError("Must be non empty")
        elif self.init == 0 or self.term == 0:
            raise ValueError("INIT and TERM must not be zero")
        elif self.simple_paths:
            return [self.simple_paths, self.prime_paths]
        else:
            # Find all simple paths using DFS
            for start_node in self.relationship.keys():
                visited = set()
                self.dfs_simple_paths(start_node, "", visited)
            
            # Find prime paths (maximal simple paths)
            # print("Before prime paths this is already I have in list: ", self.prime_paths)
            self.find_prime_paths()
            
            return [self.simple_paths, self.prime_paths]
    
    def dfs_simple_paths(self, node, current_path, visited):
        """Find all simple paths (no repeated nodes) using DFS"""
        current_path += str(node)
        visited.add(node)
        
        # If node has no outgoing edges, it's a complete path
        if node not in self.relationship or not self.relationship[node]:
            self.simple_paths.append(current_path+"!")
            return
        else:
            self.simple_paths.append(current_path)
            for neighbor in self.relationship[node]:
                if neighbor not in visited and neighbor!= "TERM":
                    self.dfs_simple_paths(neighbor, current_path, visited.copy())
                elif neighbor not in visited and neighbor== "TERM":
                    self.simple_paths.append(current_path+"!")
                else:
                    # this is loop, must be prime path (if this matches the first element)
                    # print(neighbor, " is the neighbour and ", current_path, " is the path", current_path[0], " is the first index")
                    print(current_path[0] == neighbor)
                    if current_path[0] == neighbor:
                        # print("Inner loop worked")
                        # although they are not simple technically but they are loops, so we will regardless put them in simple loops
                        print("Should be a * mf: ", current_path+ neighbor +"*")
                        self.simple_paths.append(current_path+ neighbor +"*")
                        # self.prime_paths.append(current_path+str(neighbor))
                    else:
                        # self.simple_paths.append(current_path+"!")
                        if neighbor!= "TERM":
                            # print("Why am I on else: ", current_path, neighbor)
                            if neighbor != current_path[-1]:
                                # print("I have to change this in else: ", self.simple_paths[-1])
                                self.simple_paths[-1] = current_path + "!"
                            # self.simple_paths.append()
            
            # If we can't extend further, this is an ending path
    
    def find_prime_paths(self):
        for sp in self.simple_paths:
            if sp[-1]=="*":
                self.prime_paths.append(sp)
        terminating  = []
        for path in self.simple_paths:
            if path[-1]=="!":
                terminating.append(path)
        # print(terminatings)
        for i in range(len(terminating)):
            curr = terminating[i][:len(terminating[i])-1]
            found = False
            for j in range(len(terminating)):
                # print("checking ")
                check = terminating[j][:len(terminating[j])-1]
                if i!=j and len(curr) < len(check):
                    if check.find(curr)!=-1:
                        found = True
                        break
            if not found:
                self.prime_paths.append(curr+"!")      

        # pass



    
    def return_paths(self):
        print(self.simple_paths, "<-- Simple Paths")
        print(self.prime_paths, "<-- Prime Paths")
        print("summary: total simple paths: ", len(self.simple_paths), " total prime paths: ", len(self.prime_paths))
        return
        


# test = Testing([["INIT", "1"], ["1", "2"], ["1", "5"], ["2", "6"], ["2", "3"], ["4", "2"], ["3", "4"], ["6", "7"], ["5", "5"], ["5", "7"], ["7", "TERM"]])
test = Testing([["INIT", "1"],["1","2"],["2","3"],["3","4"],["4","2"],["2", "TERM"]])
test.get_relationship()
test.find_paths()
test.return_paths()
# print("157".find("15"))