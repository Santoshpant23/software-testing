import pytest

from logic_coverage import LogicPredicate, pc_tests, cc_tests, mcc_tests

def has_true_and_false(pred, tests):
    vals = [pred.evaluate(t) for t in tests]
    return any(vals) and not all(vals)

def test_bcc_base_pc_A_and_B():
    # TB0: base choice - predicate A && B, criterion PC
    p = LogicPredicate('A && B')
    tests = pc_tests(p)
    # must include at least one assignment where predicate is true and one false
    assert has_true_and_false(p, tests)
    assert set(p.clauses) == {'A', 'B'}

def test_bcc_single_clause():
    # TB_pred_B2: single clause predicate
    p = LogicPredicate('A')
    tests = pc_tests(p)
    # Expect both True and False assignments for A
    assert len(tests) == 2
    vals = sorted([t['A'] for t in tests])
    assert vals == [False, True]

def test_bcc_three_clause_predicate():
    # TB_pred_B3: A && (B || C)
    p = LogicPredicate('A && (B || C)')
    tests = pc_tests(p)
    assert has_true_and_false(p, tests)
    assert set(p.clauses) == {'A', 'B', 'C'}

def test_bcc_cc_returns_clause_values():
    p = LogicPredicate('A && B')
    cc = cc_tests(p)
    seen = {('A', True): False, ('A', False): False, ('B', True): False, ('B', False): False}
    for t in cc:
        for c in ['A', 'B']:
            seen[(c, t[c])] = True
    assert all(seen.values())

def test_bcc_mcc_full_table():
    # TB_criterion_MCC: full truth table for A && B
    p = LogicPredicate('A && B')
    all_tests = mcc_tests(p)
    assert len(all_tests) == 4

def test_bcc_malformed_predicate_raises():
    with pytest.raises(ValueError):
        LogicPredicate('A &&& B')

def test_bcc_empty_predicate_raises():
    with pytest.raises(ValueError):
        LogicPredicate('')
