"""
** Command Pattern (Interview Important)
When to use: When you need to parameterize objects with operations, queue or log
requests, or support undoable operations. Encapsulates a request as an object.
Real-world examples: Django migration operations (each migration is a command with
forwards/backwards), GUI Undo/Redo systems, transactional behaviors, job queues
(Celery tasks), database replication logs.
"""

from __future__ import annotations
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Protocol


class TextBuffer(Protocol):
    content: str


@dataclass
class Document:
    content: str = ""

    def insert(self, pos: int, text: str) -> None:
        self.content = self.content[:pos] + text + self.content[pos:]

    def delete(self, pos: int, length: int) -> str:
        deleted = self.content[pos:pos + length]
        self.content = self.content[:pos] + self.content[pos + length:]
        return deleted

    def __str__(self) -> str:
        return self.content


class Command(ABC):
    @abstractmethod
    def execute(self) -> None:
        ...

    @abstractmethod
    def undo(self) -> None:
        ...


@dataclass
class InsertTextCommand(Command):
    document: Document
    position: int
    text: str

    def execute(self) -> None:
        self.document.insert(self.position, self.text)

    def undo(self) -> None:
        self.document.delete(self.position, len(self.text))


@dataclass
class DeleteTextCommand(Command):
    document: Document
    position: int
    length: int
    _deleted_text: str = ""

    def execute(self) -> None:
        self._deleted_text = self.document.delete(self.position, self.length)

    def undo(self) -> None:
        self.document.insert(self.position, self._deleted_text)


@dataclass
class ReplaceTextCommand(Command):
    document: Document
    position: int
    length: int
    new_text: str
    _replaced_text: str = ""

    def execute(self) -> None:
        self._replaced_text = self.document.delete(self.position, self.length)
        self.document.insert(self.position, self.new_text)

    def undo(self) -> None:
        self.document.delete(self.position, len(self.new_text))
        self.document.insert(self.position, self._replaced_text)


@dataclass
class Editor:
    document: Document = field(default_factory=Document)
    _history: list[Command] = field(default_factory=list)
    _redo_stack: list[Command] = field(default_factory=list)

    def execute(self, command: Command) -> None:
        command.execute()
        self._history.append(command)
        self._redo_stack.clear()

    def undo(self) -> bool:
        if not self._history:
            return False
        cmd = self._history.pop()
        cmd.undo()
        self._redo_stack.append(cmd)
        return True

    def redo(self) -> bool:
        if not self._redo_stack:
            return False
        cmd = self._redo_stack.pop()
        cmd.execute()
        self._history.append(cmd)
        return True


if __name__ == "__main__":
    editor = Editor()

    print("=== Text Editor with Undo/Redo ===\n")

    cmd1 = InsertTextCommand(editor.document, 0, "Hello, World!")
    editor.execute(cmd1)
    print(f"  After insert:  \"{editor.document}\"")

    cmd2 = DeleteTextCommand(editor.document, 5, 7)
    editor.execute(cmd2)
    print(f"  After delete:  \"{editor.document}\"")

    cmd3 = InsertTextCommand(editor.document, 5, " Python")
    editor.execute(cmd3)
    print(f"  After insert:  \"{editor.document}\"")

    cmd4 = ReplaceTextCommand(editor.document, 0, 5, "Hi")
    editor.execute(cmd4)
    print(f"  After replace: \"{editor.document}\"\n")

    print("  --- Undo x2 ---")
    editor.undo()
    print(f"  After undo 1:  \"{editor.document}\"")
    editor.undo()
    print(f"  After undo 2:  \"{editor.document}\"")

    print("  --- Redo ---")
    editor.redo()
    print(f"  After redo 1:  \"{editor.document}\"\n")

    print("  Final document:", repr(editor.document.content))

