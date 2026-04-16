import pytest

# Updated Testing class with validation and path-finding logic
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
            if t not in self.relationship:
                self.relationship[t] = []

    def get_relationship(self):
        return self.relationship

    def find_paths(self):
        # Input validation expected by tests
        if not self.edges:
            raise ValueError("Must be non empty")

        has_init = any(u == "INIT" for u, v in self.edges)
        has_term = any(v == "TERM" for u, v in self.edges)
        if not has_init or not has_term:
            raise ValueError("INIT and TERM must not be zero")

        if self.simple_paths:
            return [self.simple_paths, self.prime_paths]

        for start_node in self.relationship.keys():
            visited = set()
            self.dfs_simple_paths(start_node, "", visited)

        self.find_prime_paths()
        return [self.simple_paths, self.prime_paths]

    def dfs_simple_paths(self, node, current_path, visited):
        current_path += str(node)
        visited.add(node)

        if node not in self.relationship or not self.relationship[node]:
            self.simple_paths.append(current_path + "!")
            return
        else:
            self.simple_paths.append(current_path)
            for neighbor in self.relationship[node]:
                if neighbor not in visited:
                    self.dfs_simple_paths(neighbor, current_path, visited.copy())
                else:
                    if str(neighbor) == current_path[0]:
                        self.simple_paths.append(current_path + str(neighbor) + "*")
                    else:
                        if str(neighbor) != current_path[-1]:
                            self.simple_paths[-1] = current_path + "!"

    def find_prime_paths(self):
        for sp in self.simple_paths:
            if sp and sp[-1] == "*":
                self.prime_paths.append(sp)

        terminating = []
        for path in self.simple_paths:
            if path and path[-1] == "!":
                terminating.append(path)

        for i in range(len(terminating)):
            curr = terminating[i][:-1]
            found = False
            for j in range(len(terminating)):
                check = terminating[j][:-1]
                if i != j and len(curr) < len(check):
                    if check.find(curr) != -1:
                        found = True
                        break
            if not found:
                self.prime_paths.append(curr + "!")


# --- Tests -------------------------------------------------

def test_empty_list_raises():
    with pytest.raises(ValueError) as exc:
        Testing([]).find_paths()
    assert str(exc.value) == "Must be non empty"


def test_missing_init_or_term_raises():
    # missing INIT
    with pytest.raises(ValueError) as exc:
        Testing([["1", "2"], ["2", "3"], ["3", "TERM"]]).find_paths()
    assert str(exc.value) == "INIT and TERM must not be zero"

    # missing TERM
    with pytest.raises(ValueError) as exc:
        Testing([["INIT", "1"], ["1", "2"]]).find_paths()
    assert str(exc.value) == "INIT and TERM must not be zero"


def test_simple_init_term_path():
    t = Testing([["INIT", "1"], ["1", "TERM"]])
    simple, prime = t.find_paths()
    assert any(p.endswith("!") for p in simple)
    assert any(p.endswith("!") for p in prime)


def test_self_loop():
    t = Testing([["INIT", "N"], ["N", "N"], ["N", "TERM"]])
    simple, prime = t.find_paths()
    # expect at least one terminating simple path and a prime terminating path
    assert any(p.endswith("!") for p in simple)
    assert any(p.endswith("!") for p in prime)


def test_disconnected_graph_raises():
    # graph with no INIT/TERM reachable
    with pytest.raises(ValueError):
        Testing([["N", "N"]]).find_paths()


def test_cycle_with_term():
    t = Testing([["INIT", "N1"], ["N1", "N2"], ["N2", "N3"], ["N3", "N4"], ["N4", "N2"], ["N2", "TERM"]])
    simple, prime = t.find_paths()
    assert len(prime) >= 1


def test_multiple_inits_and_terms():
    t = Testing([["INIT", "N1"], ["N1", "N3"], ["INIT", "N2"], ["N2", "N3"], ["N3", "TERM"]])
    simple, prime = t.find_paths()
    assert any(p.endswith("!") for p in simple)


def test_branching_terms():
    t = Testing([["INIT", "N1"], ["N1", "N2"], ["N2", "N4"], ["N1", "N3"], ["N3", "TERM"], ["N4", "TERM"]])
    simple, prime = t.find_paths()
    assert any(p.endswith("!") for p in simple)
