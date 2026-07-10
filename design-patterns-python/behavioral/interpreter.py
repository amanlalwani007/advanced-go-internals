"""
Interpreter
When to use: When you need to parse and evaluate expressions in a language (DSL),
especially when the grammar is simple and stable. The pattern defines a representation
for the grammar along with an interpreter that uses the representation.
Real-world examples: SQL parsers, regular expression engines, Jinja2/Django template
engines, mathematical expression evaluators, configuration language parsers
(YAML/TOML), HTML template expression syntax ({{ }}).
"""

from __future__ import annotations
from abc import ABC, abstractmethod
import re
from dataclasses import dataclass
from typing import Sequence


class ASTNode(ABC):
    @abstractmethod
    def evaluate(self, context: dict[str, int]) -> int:
        ...


@dataclass
class NumberNode(ASTNode):
    value: int

    def evaluate(self, context: dict[str, int]) -> int:
        return self.value


@dataclass
class VariableNode(ASTNode):
    name: str

    def evaluate(self, context: dict[str, int]) -> int:
        if self.name not in context:
            raise NameError(f"Undefined variable '{self.name}'")
        return context[self.name]


@dataclass
class BinaryOpNode(ASTNode):
    left: ASTNode
    right: ASTNode
    op: str

    def evaluate(self, context: dict[str, int]) -> int:
        lval = self.left.evaluate(context)
        rval = self.right.evaluate(context)
        if self.op == "+":
            return lval + rval
        elif self.op == "-":
            return lval - rval
        elif self.op == "*":
            return lval * rval
        elif self.op == "/":
            if rval == 0:
                raise ZeroDivisionError("Division by zero")
            return lval // rval
        raise ValueError(f"Unknown operator '{self.op}'")


@dataclass
class UnaryOpNode(ASTNode):
    operand: ASTNode
    op: str

    def evaluate(self, context: dict[str, int]) -> int:
        val = self.operand.evaluate(context)
        if self.op == "-":
            return -val
        elif self.op == "+":
            return val
        raise ValueError(f"Unknown unary operator '{self.op}'")


Token = tuple[str, str]


class Parser:
    def __init__(self, text: str) -> None:
        self.tokens: list[Token] = list(self._tokenize(text))
        self.pos: int = 0

    def _tokenize(self, text: str) -> list[Token]:
        token_spec = [
            ("NUMBER", r"\d+"),
            ("VARIABLE", r"[a-zA-Z_][a-zA-Z0-9_]*"),
            ("OP", r"[+\-*/]"),
            ("LPAREN", r"\("),
            ("RPAREN", r"\)"),
            ("SKIP", r"\s+"),
        ]
        tok_re = "|".join(f"(?P<{name}>{pattern})" for name, pattern in token_spec)
        tokens: list[Token] = []
        for m in re.finditer(tok_re, text):
            kind = m.lastgroup
            value = m.group()
            if kind is None or kind == "SKIP":
                continue
            tokens.append((kind, value))
        return tokens

    def _peek(self) -> str | None:
        if self.pos >= len(self.tokens):
            return None
        return self.tokens[self.pos][0]

    def _consume(self, expected: str | None = None) -> str:
        if self.pos >= len(self.tokens):
            raise SyntaxError("Unexpected end of expression")
        kind, value = self.tokens[self.pos]
        if expected is not None and kind != expected:
            raise SyntaxError(f"Expected {expected}, got {kind} ('{value}')")
        self.pos += 1
        return value

    def parse(self) -> ASTNode:
        node = self._parse_expr()
        if self.pos < len(self.tokens):
            raise SyntaxError(f"Unexpected token '{self.tokens[self.pos][1]}' after full parse")
        return node

    def _parse_expr(self) -> ASTNode:
        node = self._parse_term()
        while self._peek() == "OP" and self.tokens[self.pos][1] in ("+", "-"):
            op = self._consume("OP")
            right = self._parse_term()
            node = BinaryOpNode(node, right, op)
        return node

    def _parse_term(self) -> ASTNode:
        node = self._parse_factor()
        while self._peek() == "OP" and self.tokens[self.pos][1] in ("*", "/"):
            op = self._consume("OP")
            right = self._parse_factor()
            node = BinaryOpNode(node, right, op)
        return node

    def _parse_factor(self) -> ASTNode:
        if self._peek() == "OP" and self.tokens[self.pos][1] in ("+", "-"):
            op = self._consume("OP")
            operand = self._parse_factor()
            return UnaryOpNode(operand, op)
        if self._peek() == "LPAREN":
            self._consume("LPAREN")
            node = self._parse_expr()
            self._consume("RPAREN")
            return node
        if self._peek() == "NUMBER":
            val = self._consume("NUMBER")
            return NumberNode(int(val))
        if self._peek() == "VARIABLE":
            name = self._consume("VARIABLE")
            return VariableNode(name)
        raise SyntaxError(f"Unexpected token {self.tokens[self.pos] if self.pos < len(self.tokens) else 'EOF'}")


def interpret(expression: str, context: dict[str, int] | None = None) -> int:
    parser = Parser(expression)
    ast = parser.parse()
    return ast.evaluate(context or {})


if __name__ == "__main__":
    print("=== Mathematical Expression Interpreter ===\n")

    expressions = [
        ("5 + 3 * 2", {}),
        ("(5 + 3) * 2", {}),
        ("-10 + 15", {}),
        ("x * 2 + y", {"x": 7, "y": 3}),
        ("(a + b) * (c - d)", {"a": 10, "b": 5, "c": 20, "d": 8}),
        ("100 / 4 + 3 * 7", {}),
    ]

    for expr, ctx in expressions:
        try:
            result = interpret(expr, ctx)
            ctx_str = f"  context={{{', '.join(f'{k}={v}' for k, v in ctx.items())}}}" if ctx else ""
            print(f"  {expr} = {result}{ctx_str}")
        except (SyntaxError, NameError, ZeroDivisionError) as e:
            print(f"  {expr} => ERROR: {e}")
