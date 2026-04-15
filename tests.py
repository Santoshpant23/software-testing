from app import Testing
import pytest


def check_graphs(result, truth):
    a = set(result)
    b = set(truth)
    return a == b


def test_empty_array():
    try:
        test = Testing([])
        result = test.find_paths()
        pytest.fail("Did not raise ValueError!")
    except ValueError as e:
        assert str(e) == "Must be non empty"

def test_no_head_array():
    try:
        test = Testing([["1", "2"], ["2", "3"], ["3", "TERM"]])
        result = test.find_paths()
        pytest.fail("Did not raise ValueError!")
    except ValueError as e:
        assert str(e) == "INIT and TERM must not be zero"


def test_no_terminal_array():
    try:
        test = Testing([["1", "2"], ["2", "3"], ["3", "TERM"]])
        result = test.find_paths()
        pytest.fail("Did not raise ValueError!")
    except ValueError as e:
        assert str(e) == "INIT and TERM must not be zero"

def test_one_element_only():
    try:
        test = Testing([["INIT", "1"], ["1", "TERM"]])
        result = test.find_paths()
        simple_paths = result[0]
        prime_paths = result[1]
        assert len(simple_paths) == 1
        assert len(prime_paths) == 1
    except ValueError as e:
        pytest.fail()


def test_one_element_self_looped():
    try:
        test = Testing([["INIT", "N"],["N","N"], ["N", "TERM"]])
        result = test.find_paths()
        # two simple paths should be there: ['N', 'N!'] and one prime path: ['N!']
        assert check_graphs(result[0], [['N'], ['N!']])
        assert check_graphs(result[1], [['N!']])
    except ValueError as e:
        pytest.fail()

def test_no_terminal_no_init_array():
    try:
        test = Testing([["N", "N"]])
        test.find_paths()
        pytest.fail("Should raise value error")
    except ValueError as e:
        assert str(e) == "INIT and TERM must not be zero"

def test_more_than_one_nodes():
    try:
        test = Testing([["INIT", "1"],["1","2"],["2","3"],["3","4"],["4","2"],["2", "TERM"]])
        # prime should be 
    except ValueError as e:
        pytest.fail()



