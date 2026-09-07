"""Behavior tests for Python cyclomatic-complexity analysis."""

from __future__ import annotations

from textwrap import dedent

from crapcheck.complexity import FunctionComplexity, analyze_complexity


def source(text: str) -> str:
    """Normalize an indented source fixture without shifting its first line."""
    return dedent(text).lstrip()


def test_discovers_functions_async_functions_and_methods() -> None:
    analyzed = analyze_complexity(
        source(
            """
            def constant():
                return 1

            async def choose(flag):
                if flag:
                    return 1
                return 0

            class Calculator:
                def classify(self, value):
                    if value > 0 and value < 10:
                        return "small"
                    elif value == 0:
                        return "zero"
                    return "other"
            """
        )
    )

    assert analyzed == [
        FunctionComplexity("constant", 1, 2, 1),
        FunctionComplexity("choose", 4, 7, 2),
        FunctionComplexity("Calculator.classify", 10, 15, 4),
    ]


def test_counts_loops_exception_handlers_and_ternary_expressions() -> None:
    analyzed = analyze_complexity(
        source(
            """
            def process(items):
                for item in items:
                    while item.pending:
                        item.advance()
                try:
                    result = items[0]
                except IndexError:
                    result = None
                return result if result is not None else "empty"
            """
        )
    )

    assert analyzed == [FunctionComplexity("process", 1, 9, 5)]


def test_counts_each_decision_in_a_boolean_expression() -> None:
    analyzed = analyze_complexity(
        source(
            """
            def all_enabled(a, b, c):
                if a and b and c:
                    return True
                return False
            """
        )
    )

    assert analyzed == [FunctionComplexity("all_enabled", 1, 4, 4)]


def test_nested_function_decisions_do_not_inflate_the_outer_function() -> None:
    analyzed = analyze_complexity(
        source(
            """
            def outer(flag):
                def inner(value):
                    if value:
                        return 1
                    return 0

                if flag:
                    return inner(flag)
                return 0
            """
        )
    )

    assert analyzed == [
        FunctionComplexity("outer", 1, 9, 2),
        FunctionComplexity("outer.inner", 2, 5, 2),
    ]


def test_counts_each_comprehension_generator_and_filter() -> None:
    assert analyze_complexity(
        source(
            """
            def comprehension(items):
                return [y for item in items if item for y in item if y]
            """
        )
    ) == [FunctionComplexity("comprehension", 1, 2, 5)]


def test_counts_nondefault_match_cases() -> None:
    assert analyze_complexity(
        source(
            """
            def pattern(value, ready):
                match value:
                    case 0:
                        return "zero"
                    case 1 | 2 if ready:
                        return "ready"
                    case _:
                        return "other"
            """
        )
    ) == [FunctionComplexity("pattern", 1, 8, 3)]


def test_counts_assertions() -> None:
    assert analyze_complexity(
        source(
            """
            def assertion(value):
                assert value
                return value
            """
        )
    ) == [FunctionComplexity("assertion", 1, 3, 2)]


def test_counts_lambda_body_decisions_in_the_enclosing_function() -> None:
    assert analyze_complexity(
        source(
            """
            def lambda_holder(items):
                predicate = lambda item: item > 0 and item < 10
                return [item for item in items if predicate(item)]
            """
        )
    ) == [FunctionComplexity("lambda_holder", 1, 3, 4)]
