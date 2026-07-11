"""
Visitor
When to use: When you need to perform operations on elements of a complex object
structure without changing the element classes. Lets you define new operations
without modifying the elements.
Real-world examples: Python AST module (ast.NodeVisitor), compiler design (IR
passes), directory traversal (os.walk), code analysis tools (linters, formatters),
serialization/export operations (HTML/XML/Markdown renderers for same data model).
"""

from __future__ import annotations
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any


class ASTVisitor(ABC):
    @abstractmethod
    def visit_variable(self, node: VariableNode) -> Any:
        ...

    @abstractmethod
    def visit_function(self, node: FunctionNode) -> Any:
        ...

    @abstractmethod
    def visit_class(self, node: ClassNode) -> Any:
        ...

    @abstractmethod
    def visit_module(self, node: ModuleNode) -> Any:
        ...


class ASTNode(ABC):
    @abstractmethod
    def accept(self, visitor: ASTVisitor) -> Any:
        ...


@dataclass
class VariableNode(ASTNode):
    name: str
    type_hint: str | None = None
    is_constant: bool = False
    line: int = 0

    def accept(self, visitor: ASTVisitor) -> Any:
        return visitor.visit_variable(self)


@dataclass
class FunctionNode(ASTNode):
    name: str
    params: list[tuple[str, str | None]] = field(default_factory=list)
    return_type: str | None = None
    line_count: int = 0
    decorators: list[str] = field(default_factory=list)
    line: int = 0

    def accept(self, visitor: ASTVisitor) -> Any:
        return visitor.visit_function(self)


@dataclass
class ClassNode(ASTNode):
    name: str
    bases: list[str] = field(default_factory=list)
    methods: list[FunctionNode] = field(default_factory=list)
    attributes: list[VariableNode] = field(default_factory=list)
    line: int = 0

    def accept(self, visitor: ASTVisitor) -> Any:
        return visitor.visit_class(self)


@dataclass
class ModuleNode(ASTNode):
    name: str
    variables: list[VariableNode] = field(default_factory=list)
    functions: list[FunctionNode] = field(default_factory=list)
    classes: list[ClassNode] = field(default_factory=list)
    imports: list[str] = field(default_factory=list)

    def accept(self, visitor: ASTVisitor) -> Any:
        return visitor.visit_module(self)


class LinterVisitor(ASTVisitor):
    def __init__(self) -> None:
        self.issues: list[str] = []

    def visit_variable(self, node: VariableNode) -> None:
        if not node.type_hint and not node.is_constant:
            self.issues.append(f"  LINT L{node.line}: Variable '{node.name}' missing type hint")
        if node.is_constant and not node.name.isupper():
            self.issues.append(f"  LINT L{node.line}: Constant '{node.name}' should be UPPER_CASE")

    def visit_function(self, node: FunctionNode) -> None:
        if not node.return_type:
            self.issues.append(f"  LINT L{node.line}: Function '{node.name}' missing return type")
        if node.line_count > 50:
            self.issues.append(f"  LINT L{node.line}: Function '{node.name}' is {node.line_count} lines (max 50)")
        for name, hint in node.params:
            if not hint:
                self.issues.append(f"  LINT L{node.line}: Parameter '{name}' in '{node.name}' missing type hint")

    def visit_class(self, node: ClassNode) -> None:
        if not node.bases:
            self.issues.append(f"  LINT L{node.line}: Class '{node.name}' has no base classes")

    def visit_module(self, node: ModuleNode) -> None:
        if not node.imports:
            self.issues.append(f"  LINT: Module '{node.name}' has no imports (possibly dead code?")
        for child in node.variables + node.functions + node.classes:
            child.accept(self)


class ComplexityAnalyzer(ASTVisitor):
    def __init__(self) -> None:
        self.complexity: dict[str, int] = {}

    def visit_variable(self, node: VariableNode) -> None:
        pass

    def visit_function(self, node: FunctionNode) -> None:
        score = 1
        score += len(node.params)
        score += len(node.decorators)
        if node.line_count > 20:
            score += 1
        self.complexity[f"function:{node.name}"] = score

    def visit_class(self, node: ClassNode) -> None:
        score = len(node.methods) + len(node.bases)
        self.complexity[f"class:{node.name}"] = score

    def visit_module(self, node: ModuleNode) -> None:
        for child in node.variables + node.functions + node.classes:
            child.accept(self)


class DocumentationGenerator(ASTVisitor):
    def __init__(self) -> None:
        self.docs: list[str] = []

    def visit_variable(self, node: VariableNode) -> None:
        hint = f": {node.type_hint}" if node.type_hint else ""
        const = " (constant)" if node.is_constant else ""
        self.docs.append(f"  - `{node.name}`{hint}{const}")

    def visit_function(self, node: FunctionNode) -> None:
        params = ", ".join(
            f"{name}: {hint}" if hint else name
            for name, hint in node.params
        )
        ret = f" -> {node.return_type}" if node.return_type else ""
        self.docs.append(f"  - `def {node.name}({params}){ret}` — {node.line_count} lines")

    def visit_class(self, node: ClassNode) -> None:
        bases = f"({', '.join(node.bases)})" if node.bases else ""
        self.docs.append(f"  - `class {node.name}{bases}` — {len(node.methods)} methods, {len(node.attributes)} attributes")
        for attr in node.attributes:
            attr.accept(self)
        for method in node.methods:
            method.accept(self)

    def visit_module(self, node: ModuleNode) -> None:
        self.docs.append(f"# Module: {node.name}")
        self.docs.append(f"  Imports: {len(node.imports)}")
        if node.variables:
            self.docs.append("  ## Variables")
        for v in node.variables:
            v.accept(self)
        if node.functions:
            self.docs.append("  ## Functions")
        for f in node.functions:
            f.accept(self)
        if node.classes:
            self.docs.append("  ## Classes")
        for c in node.classes:
            c.accept(self)


def build_sample_ast() -> ModuleNode:
    return ModuleNode(
        name="payment_service",
        imports=["os", "json", "requests"],
        variables=[
            VariableNode("API_KEY", type_hint="str", line=1),
            VariableNode("max_retries", type_hint=None, line=2),
            VariableNode("DEFAULT_TIMEOUT", type_hint="float", is_constant=True, line=3),
        ],
        functions=[
            FunctionNode(
                "process_payment",
                params=[("user_id", "int"), ("amount", "float"), ("currency", None)],
                return_type="bool",
                line_count=45,
                decorators=["@log_execution"],
                line=5,
            ),
            FunctionNode(
                "_validate",
                params=[("data", None)],
                return_type=None,
                line_count=8,
                line=55,
            ),
        ],
        classes=[
            ClassNode(
                "RefundProcessor",
                bases=["BaseProcessor"],
                methods=[
                    FunctionNode("refund", [("txn_id", "str")], "bool", 30, line=70),
                    FunctionNode("_notify", [("user", "str")], line_count=12, line=80),
                ],
                attributes=[
                    VariableNode("retry_limit", type_hint="int", line=60),
                ],
                line=58,
            ),
            ClassNode(
                "TransactionLogger",
                bases=[],
                methods=[
                    FunctionNode("log", [("event", "str")], "None", 15, line=90),
                ],
                line=85,
            ),
        ],
    )


if __name__ == "__main__":
    print("=== Code Analysis Tool (Visitor Pattern) ===\n")

    ast = build_sample_ast()

    linter = LinterVisitor()
    ast.accept(linter)
    print("  Linting Results:")
    for issue in linter.issues:
        print(issue)

    print()
    analyzer = ComplexityAnalyzer()
    ast.accept(analyzer)
    print("  Complexity Scores:")
    for name, score in sorted(analyzer.complexity.items()):
        bar = "#" * min(score, 20)
        print(f"    {name:40s} {score:2d} {bar}")

    print()
    doc_gen = DocumentationGenerator()
    ast.accept(doc_gen)
    print("  Generated Documentation:")
    for line in doc_gen.docs:
        print(f"    {line}")
