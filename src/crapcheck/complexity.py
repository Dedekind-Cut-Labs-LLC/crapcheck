"""Function discovery and cyclomatic-complexity analysis."""

from __future__ import annotations

import ast
from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class FunctionComplexity:
    """Cyclomatic complexity and source extent for one named function."""

    name: str
    line: int
    end_line: int
    complexity: int


class _DecisionCounter(ast.NodeVisitor):
    """Count decisions within one function, excluding nested scopes."""

    def __init__(self) -> None:
        self.complexity = 1

    def visit_If(self, node: ast.If) -> None:
        self.complexity += 1
        self.generic_visit(node)

    def visit_For(self, node: ast.For) -> None:
        self.complexity += 1
        self.generic_visit(node)

    def visit_AsyncFor(self, node: ast.AsyncFor) -> None:
        self.complexity += 1
        self.generic_visit(node)

    def visit_While(self, node: ast.While) -> None:
        self.complexity += 1
        self.generic_visit(node)

    def visit_ExceptHandler(self, node: ast.ExceptHandler) -> None:
        self.complexity += 1
        self.generic_visit(node)

    def visit_IfExp(self, node: ast.IfExp) -> None:
        self.complexity += 1
        self.generic_visit(node)

    def visit_BoolOp(self, node: ast.BoolOp) -> None:
        self.complexity += len(node.values) - 1
        self.generic_visit(node)

    def visit_comprehension(self, node: ast.comprehension) -> None:
        self.complexity += 1 + len(node.ifs)
        self.generic_visit(node)

    def visit_Match(self, node: ast.Match) -> None:
        self.complexity += sum(
            not (
                isinstance(case.pattern, ast.MatchAs)
                and case.pattern.pattern is None
                and case.guard is None
            )
            for case in node.cases
        )
        self.generic_visit(node)

    def visit_Assert(self, node: ast.Assert) -> None:
        self.complexity += 1
        self.generic_visit(node)

    def visit_FunctionDef(self, node: ast.FunctionDef) -> None:
        return None

    def visit_AsyncFunctionDef(self, node: ast.AsyncFunctionDef) -> None:
        return None

    def visit_Lambda(self, node: ast.Lambda) -> None:
        self.generic_visit(node)

    def visit_ClassDef(self, node: ast.ClassDef) -> None:
        return None


_FunctionNode = ast.FunctionDef | ast.AsyncFunctionDef


class _FunctionCollector(ast.NodeVisitor):
    """Collect named functions with scope-qualified names."""

    def __init__(self) -> None:
        self.scope: list[str] = []
        self.functions: list[FunctionComplexity] = []

    def visit_ClassDef(self, node: ast.ClassDef) -> None:
        self.scope.append(node.name)
        try:
            for statement in node.body:
                self.visit(statement)
        finally:
            self.scope.pop()

    def visit_FunctionDef(self, node: ast.FunctionDef) -> None:
        self._visit_function(node)

    def visit_AsyncFunctionDef(self, node: ast.AsyncFunctionDef) -> None:
        self._visit_function(node)

    def _visit_function(self, node: _FunctionNode) -> None:
        counter = _DecisionCounter()
        for statement in node.body:
            counter.visit(statement)

        qualified_name = ".".join((*self.scope, node.name))
        end_line = node.end_lineno if node.end_lineno is not None else node.lineno
        self.functions.append(
            FunctionComplexity(qualified_name, node.lineno, end_line, counter.complexity)
        )

        self.scope.append(node.name)
        try:
            for statement in node.body:
                self.visit(statement)
        finally:
            self.scope.pop()


def analyze_complexity(source: str) -> list[FunctionComplexity]:
    """Return source-ordered complexity results for named functions in Python source."""
    tree = ast.parse(source)
    collector = _FunctionCollector()
    collector.visit(tree)
    return collector.functions
