"""
** Chain of Responsibility Pattern (Interview Important)
When to use: When you have a request that needs to be processed by one of several handlers,
but the handler isn't known in advance. Each handler either processes the request or passes
it to the next handler in the chain.
Real-world examples: Django middleware stack, Express.js middleware, Python logging
levels (DEBUG -> INFO -> WARNING -> ERROR), Java Servlet Filters, ASP.NET Core
middleware pipeline.
"""

from __future__ import annotations
from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum, auto
import time


class Severity(Enum):
    LOW = auto()
    MEDIUM = auto()
    HIGH = auto()
    CRITICAL = auto()


@dataclass
class Ticket:
    id: int
    description: str
    severity: Severity
    error_code: str | None = None


class Handler(ABC):
    def __init__(self) -> None:
        self._next: Handler | None = None

    def set_next(self, handler: Handler) -> Handler:
        self._next = handler
        return handler

    @abstractmethod
    def can_handle(self, ticket: Ticket) -> bool:
        ...

    @abstractmethod
    def resolve(self, ticket: Ticket) -> str:
        ...

    def handle(self, ticket: Ticket) -> str:
        if self.can_handle(ticket):
            return self.resolve(ticket)
        if self._next is not None:
            return self._next.handle(ticket)
        raise RuntimeError(f"Ticket {ticket.id} ({ticket.description}) could not be resolved by any handler.")


class LevelOneSupport(Handler):
    def can_handle(self, ticket: Ticket) -> bool:
        return ticket.severity == Severity.LOW and ticket.error_code in ("AUTH_ERR", "NOT_FOUND")

    def resolve(self, ticket: Ticket) -> str:
        return f"[L1] Reset credentials / clear cache for ticket #{ticket.id}"


class LevelTwoSupport(Handler):
    def can_handle(self, ticket: Ticket) -> bool:
        return ticket.severity in (Severity.LOW, Severity.MEDIUM)

    def resolve(self, ticket: Ticket) -> str:
        return f"[L2] Restarted service / ran db migration for ticket #{ticket.id}"


class LevelThreeSupport(Handler):
    def can_handle(self, ticket: Ticket) -> bool:
        return ticket.severity in (Severity.LOW, Severity.MEDIUM, Severity.HIGH)

    def resolve(self, ticket: Ticket) -> str:
        return f"[L3] Hot-fix deployed to staging for ticket #{ticket.id}"


class ManagerHandler(Handler):
    def can_handle(self, ticket: Ticket) -> bool:
        return True

    def resolve(self, ticket: Ticket) -> str:
        if ticket.severity == Severity.CRITICAL:
            return f"[MGR] Escalated to VP of Engineering for ticket #{ticket.id}"
        return f"[MGR] Approved exception for ticket #{ticket.id}"


if __name__ == "__main__":
    l1 = LevelOneSupport()
    l2 = LevelTwoSupport()
    l3 = LevelThreeSupport()
    mgr = ManagerHandler()

    l1.set_next(l2).set_next(l3).set_next(mgr)

    tickets = [
        Ticket(1, "User cannot log in", Severity.LOW, "AUTH_ERR"),
        Ticket(2, "API returns 500 intermittently", Severity.MEDIUM),
        Ticket(3, "Payment gateway outage", Severity.CRITICAL),
        Ticket(4, "UI button misaligned", Severity.LOW),
        Ticket(5, "Memory leak in worker process", Severity.HIGH),
    ]

    print("=== Support Ticket Chain of Responsibility ===\n")
    for t in tickets:
        print(f"  Ticket #{t.id}: [{t.severity.name}] {t.description}")
        result = l1.handle(t)
        print(f"  => {result}\n")
        time.sleep(0.1)

