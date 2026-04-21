import pytest

from logic_coverage import LogicPredicate, pc_tests, cc_tests, mcc_tests, gacc_tests

def test_predicate_and_clauses():
    p = LogicPredicate('A && (B || !C)')
    assert set(p.clauses) == {'A', 'B', 'C'}

def test_truth_table_and_eval():
    p = LogicPredicate('A || B')
    tt = p.truth_table()
    assert len(tt) == 4
    mapping = {tuple(sorted(asg.items())): val for asg, val in tt}
    assert mapping[tuple(sorted({'A': False, 'B': False}.items()))] is False
    assert mapping[tuple(sorted({'A': True, 'B': False}.items()))] is True

def test_pc_cc_mcc_gacc():
    p = LogicPredicate('A && B')
    pc = pc_tests(p)
    cc = cc_tests(p)
    mcc = mcc_tests(p)
    gacc = gacc_tests(p)
    assert len(mcc) == 4
    assert any(isinstance(t, dict) for t in pc)
    assert any(isinstance(t, dict) for t in cc)
    assert isinstance(gacc, list)
