from app import Testing  # bring the Testing class from app.py into this file

def test_relationship():
    t = Testing([[1, 2], [2, 3]])  # create an object with a simple 2-edge graph

    # check that node 1 points to node 2
    assert t.relationship[1] == [2]

    # check that node 2 points to node 3
    assert t.relationship[2] == [3]

    # check that node 3 has no outgoing edges (it's a dead end)
    assert t.relationship[3] == []


# ── Category Partition Tests ────────────────────────────────────────────────
# Each test corresponds to one row in the readme partition table.
# [I, T, L, E, N] = [INIT count, TERM count, Loop type, Back-edges, Node count]


# Case 1: Empty list → Error
# [I=-, T=-, L=-, E=0, N=-]  Input: []
# An empty edge list has no graph at all. No paths of any kind should exist.
def test_case1_empty_list():
    t = Testing([])
    result = t.find_paths()
    assert result[0] == []   # no simple paths
    assert result[1] == []   # no prime paths


# Case 2: Simple chain, no loops
# [I=1, T=1, L=None, E=0, N=1]  Input: [[INIT,N],[N,TERM]]
# One source, one sink, one middle node. Only one maximal path exists.
def test_case2_single_init_term_no_loop():
    t = Testing([[1, 2], [2, 3]])
    _, prime_paths = t.find_paths()
    assert "123!" in prime_paths


# Case 3: Self-loop on the middle node
# [I=1, T=1, L=Self, E>0, N=1]  Input: [[INIT,N],[N,N],[N,TERM]]
# The middle node loops on itself. Prime paths must include both the
# self-loop cycle and the maximal path from init to term.
def test_case3_self_loop():
    t = Testing([[1, 2], [2, 2], [2, 3]])
    _, prime_paths = t.find_paths()
    assert "22*"  in prime_paths   # self-loop  2→2
    assert "123!" in prime_paths   # init→N→term


# Case 4: Circuit (multi-node cycle)
# [I=1, T=1, L=Circuit, E>0, N>1]  Input: [[1,2],[2,3],[3,4],[4,5],[5,3],[3,6]]
# Nodes 3→4→5 form a circuit back to 3. Prime paths must include at least
# one loop path and at least one terminating path that reaches node 6.
def test_case4_circuit():
    t = Testing([[1, 2], [2, 3], [3, 4], [4, 5], [5, 3], [3, 6]])
    _, prime_paths = t.find_paths()
    assert any(p.endswith("*") for p in prime_paths)                  # circuit loop
    assert any(p.endswith("!") and "6" in p for p in prime_paths)     # path reaches term


# Case 5: Self-loop only, no init or term node → Error
# [I=0, T=0, L=Self, E>0, N=1]  Input: [[N,N]]
# The single node loops on itself. It is neither a source nor a sink, so
# no valid traversal exists. There must be no terminating prime paths.
def test_case5_no_init_no_term():
    t = Testing([[1, 1]])
    _, prime_paths = t.find_paths()
    assert not any(p.endswith("!") for p in prime_paths)   # no reachable terminal node


# Case 6: Multiple initial nodes, one terminal node
# [I>1, T=1, L=None, E=0, N>1]  Input: [[INIT1,N],[INIT2,N],[N,TERM]]
# Two independent source nodes both feed into the same path. A prime path
# must exist for each init node so both starting points are exercised.
def test_case6_multiple_init():
    t = Testing([[1, 3], [2, 3], [3, 4]])
    _, prime_paths = t.find_paths()
    assert "134!" in prime_paths   # path from init node 1
    assert "234!" in prime_paths   # path from init node 2


# Case 7: One initial node, multiple terminal nodes
# [I=1, T>1, L=None, E=0, N>1]  Input: [[INIT,N],[N,TERM1],[N,TERM2]]
# The path branches into two separate sinks. A prime path must reach
# each terminal node so both ending points are exercised.
def test_case7_multiple_term():
    t = Testing([[1, 2], [2, 3], [2, 4]])
    _, prime_paths = t.find_paths()
    assert "123!" in prime_paths   # path to terminal node 3
    assert "124!" in prime_paths   # path to terminal node 4


# Case 8: Multiple inits, multiple terms, and a circuit
# [I>1, T>1, L=Circuit, E>0, N>1]  Input: [[1,3],[2,4],[3,4],[4,3],[3,5],[4,6]]
# Nodes 3 and 4 form a two-node circuit. Nodes 1 and 2 are separate sources;
# nodes 5 and 6 are separate sinks. Prime paths must cover all four concerns.
def test_case8_multi_init_multi_term_circuit():
    t = Testing([[1, 3], [2, 4], [3, 4], [4, 3], [3, 5], [4, 6]])
    _, prime_paths = t.find_paths()
    assert any(p.endswith("*") for p in prime_paths)                   # 3→4→3 or 4→3→4 circuit
    assert any(p.startswith("1") and p.endswith("!") for p in prime_paths)  # path from init 1
    assert any(p.startswith("2") and p.endswith("!") for p in prime_paths)  # path from init 2
    assert any(p.endswith("!") and "5" in p for p in prime_paths)     # path reaches term 5
    assert any(p.endswith("!") and "6" in p for p in prime_paths)     # path reaches term 6
