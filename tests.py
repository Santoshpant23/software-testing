from app import Testing
import pytest


def check_graphs(result, truth):
    return set(result) == set(truth)


# ----------------------------
# Error / validation tests
# ----------------------------

def test_empty_array():
    with pytest.raises(ValueError, match="Must be non empty"):
        test = Testing([])
        test.find_paths()


def test_no_init_array():
    with pytest.raises(ValueError, match="INIT and TERM must not be zero"):
        test = Testing([["1", "2"], ["2", "3"], ["3", "TERM"]])
        test.find_paths()


def test_no_terminal_array():
    with pytest.raises(ValueError, match="INIT and TERM must not be zero"):
        test = Testing([["INIT", "1"], ["1", "2"], ["2", "3"]])
        test.find_paths()


def test_no_terminal_no_init_array():
    with pytest.raises(ValueError, match="INIT and TERM must not be zero"):
        test = Testing([["N", "N"]])
        test.find_paths()


# ----------------------------
# Category partition tests
# ----------------------------

# [1,1,N,>0,1]
# [[INIT, N],[N, TERM]]
def test_one_element_only():
    test = Testing([["INIT", "1"], ["1", "TERM"]])
    result = test.find_paths()
    simple_paths = result[0]
    prime_paths = result[1]

    assert check_graphs(simple_paths, ["1", "1!"])
    assert check_graphs(prime_paths, ["1!"])


# [1,1,S,>0,1]
# [[INIT, N],[N,N],[N,TERM]]
def test_one_element_self_looped():
    test = Testing([["INIT", "N"], ["N", "N"], ["N", "TERM"]])
    result = test.find_paths()

    # Current code returns:
    # simple: ['N', 'NN*', 'N!']
    # prime:  ['NN*', 'N!']
    assert check_graphs(result[0], ["N", "NN*", "N!"])
    assert check_graphs(result[1], ["NN*", "N!"])


# [1,1,C,>0,>1]
# [[INIT, N1],[N1,N2],[N2,N3],[N3,N4],[N4,N2],[N2, TERM]]
def test_circuit_graph():
    test = Testing([
        ["INIT", "1"],
        ["1", "2"],
        ["2", "3"],
        ["3", "4"],
        ["4", "2"],
        ["2", "TERM"]
    ])
    result = test.find_paths()

    expected_simple = [
        "1", "12", "123", "1234!", "12!",
        "2", "23", "234", "2342*", "2!",
        "3", "34", "342", "3423*", "342!",
        "4", "42", "423", "4234*", "42!"
    ]
    expected_prime = ["2342*", "3423*", "4234*", "1234!", "342!"]

    assert check_graphs(result[0], expected_simple)
    assert check_graphs(result[1], expected_prime)


# [1,1,S,>0,>1] duplicate/self-loop style from readme case 6
# [[INIT, N1],[N1,N5],[N5,N5],[N5,N7],[N7,TERM]]
def test_self_loop_with_exit():
    test = Testing([
        ["INIT", "1"],
        ["1", "5"],
        ["5", "5"],
        ["5", "7"],
        ["7", "TERM"]
    ])
    result = test.find_paths()

    expected_simple = ["1", "15", "157", "157!", "5", "55*", "57", "57!", "7", "7!"]
    expected_prime = ["55*", "157!"]

    assert check_graphs(result[0], expected_simple)
    assert check_graphs(result[1], expected_prime)


# [>1,1,N,>0,>1]
# [[INIT, N1], [N1, N3], [INIT, N2], [N2, N3], [N3, TERM]]
def test_more_than_one_init():
    test = Testing([
        ["INIT", "1"],
        ["1", "3"],
        ["INIT", "2"],
        ["2", "3"],
        ["3", "TERM"]
    ])
    result = test.find_paths()

    expected_simple = ["1", "13", "13!", "2", "23", "23!", "3", "3!"]
    expected_prime = ["13!", "23!"]

    assert check_graphs(result[0], expected_simple)
    assert check_graphs(result[1], expected_prime)


# [1,>1,N,>0,>1]
# [[INIT, N1], [N1, N2], [N2, N4], [N1, N3], [N3, TERM], [N4, TERM]]
def test_more_than_one_terminal():
    test = Testing([
        ["INIT", "1"],
        ["1", "2"],
        ["2", "4"],
        ["1", "3"],
        ["3", "TERM"],
        ["4", "TERM"]
    ])
    result = test.find_paths()

    expected_simple = ["1", "12", "124", "124!", "13", "13!", "2", "24", "24!", "3", "3!", "4", "4!"]
    expected_prime = ["124!", "13!"]

    assert check_graphs(result[0], expected_simple)
    assert check_graphs(result[1], expected_prime)


# ----------------------------
# Relationship-specific tests
# ----------------------------

def test_relationship_for_simple_graph():
    test = Testing([["INIT", "1"], ["1", "2"], ["2", "TERM"]])
    assert test.relationship == {"1": ["2"], "2": ["TERM"]}


def test_relationship_multiple_inits():
    test = Testing([
        ["INIT", "1"],
        ["INIT", "2"],
        ["1", "3"],
        ["2", "3"],
        ["3", "TERM"]
    ])
    assert test.relationship == {
        "1": ["3"],
        "2": ["3"],
        "3": ["TERM"]
    }


# ----------------------------
# Behavior/caching tests
# ----------------------------

def test_find_paths_called_twice_same_result():
    test = Testing([["INIT", "1"], ["1", "2"], ["2", "TERM"]])

    first = test.find_paths()
    second = test.find_paths()

    assert first == second