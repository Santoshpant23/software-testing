import ast
import itertools
from typing import Dict, List, Tuple, Set

def _normalize(expr: str) -> str:
    return expr.replace('&&', ' and ').replace('||', ' or ').replace('!', ' not ')

def _clauses_from_ast(tree) -> List[str]:
    names = {n.id for n in ast.walk(tree) if isinstance(n, ast.Name)}
    return sorted(names)

class LogicPredicate:
    def __init__(self, expr: str):
        if not expr:
            raise ValueError('Empty predicate')
        self.expr = expr
        try:
            self.ast = ast.parse(_normalize(expr), mode='eval')
        except SyntaxError as e:
            raise ValueError(f'Invalid predicate: {e}')
        self.clauses = _clauses_from_ast(self.ast)

    def evaluate(self, assignment: Dict[str, bool]) -> bool:
        code = compile(self.ast, '<expr>', 'eval')
        for n in ast.walk(self.ast):
            if isinstance(n, ast.Name) and n.id not in assignment:
                raise KeyError(f"Missing value for clause '{n.id}'")
        return bool(eval(code, {}, assignment))

    def truth_table(self) -> List[Tuple[Dict[str, bool], bool]]:
        table = []
        for bits in itertools.product([False, True], repeat=len(self.clauses)):
            asg = dict(zip(self.clauses, bits))
            val = self.evaluate(asg)
            table.append((asg, val))
        return table

def pc_tests(pred: LogicPredicate) -> List[Dict[str, bool]]:
    tt = pred.truth_table()
    true_row = next((asg for asg, v in tt if v), None)
    false_row = next((asg for asg, v in tt if not v), None)
    res = []
    if false_row is not None:
        res.append(false_row)
    if true_row is not None and true_row not in res:
        res.append(true_row)
    return res

def mcc_tests(pred: LogicPredicate) -> List[Dict[str, bool]]:
    return [asg for asg, _ in pred.truth_table()]


def cc_tests(pred: LogicPredicate) -> List[Dict[str, bool]]:
    tt = pred.truth_table()
    clause_values: Set[Tuple[str, bool]] = set()
    for c in pred.clauses:
        clause_values.add((c, True))
        clause_values.add((c, False))

    coverage = []  
    for asg, _ in tt:
        covered = set((c, asg[c]) for c in pred.clauses)
        coverage.append((asg, covered))

    remaining = set(clause_values)
    selected = []
    while remaining:
        best = max(coverage, key=lambda it: len(it[1] & remaining))
        if len(best[1] & remaining) == 0:
            break
        selected.append(best[0])
        remaining -= best[1]
    return selected

def gacc_tests(pred: LogicPredicate) -> List[Dict[str, bool]]:
    clauses = pred.clauses
    all_asgs = [dict(zip(clauses, bits)) for bits in itertools.product([False, True], repeat=len(clauses))]
    selected = []
    for major in clauses:
        pair = None
        for asg in all_asgs:
            a0 = dict(asg)
            a1 = dict(asg)
            a0[major] = False
            a1[major] = True
            try:
                v0 = pred.evaluate(a0)
                v1 = pred.evaluate(a1)
            except KeyError:
                continue
            if v0 != v1:
                pair = (a0, a1)
                break
        if pair:
            a0, a1 = pair
            if a0 not in selected:
                selected.append(a0)
            if a1 not in selected:
                selected.append(a1)
    return selected


class Testing:
    Use like:
      t = Testing('A && (B || !C)')
      t.get_clauses()
      t.find_tests()
      t.return_tests()
  
    def __init__(self, expr):
        self.expr = expr
        self.pred = None
        self.pc = []
        self.cc = []
        self.mcc = []
        self.gacc = []
        self.make_pred()

    def make_pred(self):
        self.pred = LogicPredicate(self.expr)

    def get_clauses(self):
        print('Clauses:', self.pred.clauses)

    def find_tests(self):
        if self.pc or self.cc or self.mcc or self.gacc:
            return [self.pc, self.cc, self.mcc, self.gacc]
        self.pc = pc_tests(self.pred)
        self.cc = cc_tests(self.pred)
        self.mcc = mcc_tests(self.pred)
        self.gacc = gacc_tests(self.pred)
        return [self.pc, self.cc, self.mcc, self.gacc]

    def return_tests(self):
        print('Predicate:', self.expr)
        print('PC tests:', self.pc)
        print('CC tests:', self.cc)
        print('MCC count:', len(self.mcc))
        print('GACC tests:', self.gacc)


if __name__ == '__main__':
    t = Testing('A && (B || !C)')
    t.get_clauses()
    t.find_tests()
    t.return_tests()
