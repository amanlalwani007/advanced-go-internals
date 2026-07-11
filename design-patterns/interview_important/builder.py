"""
** Builder Pattern (Interview Important)
When to use:
- When constructing an object requires many optional steps or configuration parameters
- When different representations of the same construction process are needed
- When the construction process should be independent of the parts that make up the object

Real-world examples:
- Django QuerySet: .filter().exclude().annotate().order_by() builds a SQL query incrementally
- SQLAlchemy: query.select(..).where(..).join(..).order_by(..) pattern
- Python's struct.Struct: .pack() and .unpack() incremental construction
- Marshmallow schema: Schema().load().dump() transformations
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Optional, Sequence


class SQLQuery:
    """The product — a complete SQL query string with its parameters."""

    def __init__(self) -> None:
        self._select_clause: str = ""
        self._from_clause: str = ""
        self._joins: list[str] = []
        self._where_clauses: list[str] = []
        self._group_by_clause: str = ""
        self._having_clauses: list[str] = []
        self._order_by_clause: str = ""
        self._limit_value: Optional[int] = None
        self._offset_value: Optional[int] = None
        self._params: list = []

    def add_param(self, value) -> int:
        self._params.append(value)
        return len(self._params)

    @property
    def query(self) -> str:
        parts = [f"SELECT {self._select_clause}"]
        if self._from_clause:
            parts.append(f"FROM {self._from_clause}")
        if self._joins:
            parts.extend(self._joins)
        if self._where_clauses:
            parts.append("WHERE " + " AND ".join(self._where_clauses))
        if self._group_by_clause:
            parts.append(f"GROUP BY {self._group_by_clause}")
        if self._having_clauses:
            parts.append("HAVING " + " AND ".join(self._having_clauses))
        if self._order_by_clause:
            parts.append(f"ORDER BY {self._order_by_clause}")
        if self._limit_value is not None:
            parts.append(f"LIMIT {self._limit_value}")
        if self._offset_value is not None:
            parts.append(f"OFFSET {self._offset_value}")
        return " ".join(parts)

    @property
    def params(self) -> tuple:
        return tuple(self._params)


class SQLQueryBuilder(ABC):
    """Builder interface — defines the steps to build a SQL query."""

    @abstractmethod
    def select(self, *columns: str) -> SQLQueryBuilder:
        ...

    @abstractmethod
    def from_table(self, table: str) -> SQLQueryBuilder:
        ...

    @abstractmethod
    def join(self, table: str, on: str, join_type: str = "INNER") -> SQLQueryBuilder:
        ...

    @abstractmethod
    def where(self, column: str, operator: str, value) -> SQLQueryBuilder:
        ...

    @abstractmethod
    def where_in(self, column: str, values: Sequence) -> SQLQueryBuilder:
        ...

    @abstractmethod
    def group_by(self, *columns: str) -> SQLQueryBuilder:
        ...

    @abstractmethod
    def having(self, condition: str, operator: str, value) -> SQLQueryBuilder:
        ...

    @abstractmethod
    def order_by(self, column: str, direction: str = "ASC") -> SQLQueryBuilder:
        ...

    @abstractmethod
    def limit(self, count: int) -> SQLQueryBuilder:
        ...

    @abstractmethod
    def offset(self, count: int) -> SQLQueryBuilder:
        ...

    @abstractmethod
    def build(self) -> SQLQuery:
        ...


class PostgresQueryBuilder(SQLQueryBuilder):
    """Concrete builder — builds PostgreSQL-compatible queries."""

    def __init__(self) -> None:
        self._query = SQLQuery()

    def reset(self) -> PostgresQueryBuilder:
        self._query = SQLQuery()
        return self

    def select(self, *columns: str) -> PostgresQueryBuilder:
        self._query._select_clause = ", ".join(columns) if columns else "*"
        return self

    def from_table(self, table: str) -> PostgresQueryBuilder:
        self._query._from_clause = table
        return self

    def join(self, table: str, on: str, join_type: str = "INNER") -> PostgresQueryBuilder:
        self._query._joins.append(f"{join_type.upper()} JOIN {table} ON {on}")
        return self

    def where(self, column: str, operator: str, value) -> PostgresQueryBuilder:
        idx = self._query.add_param(value)
        self._query._where_clauses.append(f"{column} {operator} ${idx}")
        return self

    def where_in(self, column: str, values: Sequence) -> PostgresQueryBuilder:
        idxs = []
        for v in values:
            idxs.append(f"${self._query.add_param(v)}")
        placeholders = ", ".join(idxs)
        self._query._where_clauses.append(f"{column} IN ({placeholders})")
        return self

    def group_by(self, *columns: str) -> PostgresQueryBuilder:
        self._query._group_by_clause = ", ".join(columns)
        return self

    def having(self, condition: str, operator: str, value) -> PostgresQueryBuilder:
        idx = self._query.add_param(value)
        self._query._having_clauses.append(f"{condition} {operator} ${idx}")
        return self

    def order_by(self, column: str, direction: str = "ASC") -> PostgresQueryBuilder:
        self._query._order_by_clause = f"{column} {direction.upper()}"
        return self

    def limit(self, count: int) -> PostgresQueryBuilder:
        self._query._limit_value = count
        return self

    def offset(self, count: int) -> PostgresQueryBuilder:
        self._query._offset_value = count
        return self

    def build(self) -> SQLQuery:
        result = self._query
        self._query = SQLQuery()
        return result


class SQLDirector:
    """Director — orchestrates complex query construction steps."""

    def __init__(self, builder: SQLQueryBuilder) -> None:
        self._builder = builder

    def build_user_report(self, user_ids: list[int]) -> SQLQuery:
        return (
            self._builder.select("u.id", "u.name", "COUNT(o.id) as order_count", "SUM(o.total) as total_spent")
            .from_table("users u")
            .join("orders o", "o.user_id = u.id")
            .where_in("u.id", user_ids)
            .where("o.status", "!=", "cancelled")
            .group_by("u.id", "u.name")
            .having("COUNT(o.id)", ">=", 1)
            .order_by("total_spent", "DESC")
            .limit(10)
            .build()
        )

    def build_audit_log(self, days_back: int, log_level: str) -> SQLQuery:
        return (
            self._builder.select("timestamp", "level", "module", "message")
            .from_table("audit_log")
            .where("timestamp", ">=", f"NOW() - INTERVAL '{days_back} days'")
            .where("level", "=", log_level)
            .order_by("timestamp", "DESC")
            .limit(100)
            .build()
        )


if __name__ == "__main__":
    builder = PostgresQueryBuilder()
    director = SQLDirector(builder)

    print("Query 1 — User Report:")
    q1 = director.build_user_report([101, 102, 105])
    print(f"  SQL:    {q1.query}")
    print(f"  Params: {q1.params}")
    print()

    print("Query 2 — Audit Log:")
    q2 = director.build_audit_log(30, "ERROR")
    print(f"  SQL:    {q2.query}")
    print(f"  Params: {q2.params}")
    print()

    print("Query 3 — Ad-hoc Search (no director):")
    q3 = (
        PostgresQueryBuilder()
        .select("p.title", "p.price", "c.name")
        .from_table("products p")
        .join("categories c", "c.id = p.category_id")
        .where("p.price", ">=", 50.0)
        .where("p.stock", ">", 0)
        .order_by("p.price", "ASC")
        .limit(20)
        .offset(0)
        .build()
    )
    print(f"  SQL:    {q3.query}")
    print(f"  Params: {q3.params}")

