"""
Memento
When to use: When you need to capture and restore an object's internal state without
violating encapsulation. Useful for implementing undo/redo, snapshots, or checkpoint/
rollback mechanisms.
Real-world examples: Git staging/index (tree objects as snapshots), database
transactions (ROLLBACK/CREATE SAVEPOINT), Ctrl+Z in editors, game save states,
virtual machine snapshots, document version history.
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any
from copy import deepcopy
import time


@dataclass
class DocumentSnapshot:
    content: str
    cursor_position: int
    timestamp: float
    label: str = ""

    def __str__(self) -> str:
        dt = time.strftime("%H:%M:%S", time.localtime(self.timestamp))
        return f"[{dt}] '{self.content[:30]}...' cursor={self.cursor_position}"


@dataclass
class TextDocument:
    content: str = ""
    cursor_position: int = 0

    def insert(self, pos: int, text: str) -> None:
        self.content = self.content[:pos] + text + self.content[pos:]
        self.cursor_position = pos + len(text)

    def delete(self, pos: int, length: int) -> None:
        self.content = self.content[:pos] + self.content[pos + length:]
        self.cursor_position = pos

    def type_at_cursor(self, text: str) -> None:
        self.insert(self.cursor_position, text)

    def backspace(self) -> None:
        if self.cursor_position > 0 and self.content:
            self.content = (
                self.content[:self.cursor_position - 1] +
                self.content[self.cursor_position:]
            )
            self.cursor_position -= 1

    def move_cursor(self, pos: int) -> None:
        self.cursor_position = max(0, min(len(self.content), pos))

    def save_snapshot(self, label: str = "") -> DocumentSnapshot:
        return DocumentSnapshot(
            content=deepcopy(self.content),
            cursor_position=self.cursor_position,
            timestamp=time.time(),
            label=label,
        )

    def restore(self, snapshot: DocumentSnapshot) -> None:
        self.content = deepcopy(snapshot.content)
        self.cursor_position = snapshot.cursor_position

    def __str__(self) -> str:
        if not self.content:
            return "<empty>"
        return self.content


@dataclass
class History:
    _snapshots: list[DocumentSnapshot] = field(default_factory=list)
    _current: int = -1

    def push(self, snapshot: DocumentSnapshot) -> None:
        self._snapshots = self._snapshots[:self._current + 1]
        self._snapshots.append(snapshot)
        self._current = len(self._snapshots) - 1

    def undo(self) -> DocumentSnapshot | None:
        if self._current > 0:
            self._current -= 1
            return self._snapshots[self._current]
        return None

    def redo(self) -> DocumentSnapshot | None:
        if self._current < len(self._snapshots) - 1:
            self._current += 1
            return self._snapshots[self._current]
        return None

    @property
    def can_undo(self) -> bool:
        return self._current > 0

    @property
    def can_redo(self) -> bool:
        return self._current < len(self._snapshots) - 1


@dataclass
class EditorWithHistory:
    document: TextDocument = field(default_factory=TextDocument)
    history: History = field(default_factory=History)

    def _checkpoint(self, label: str = "") -> None:
        self.history.push(self.document.save_snapshot(label))

    def type_text(self, text: str) -> None:
        self._checkpoint(f"type '{text}'")
        self.document.type_at_cursor(text)

    def delete_backward(self) -> None:
        self._checkpoint("backspace")
        self.document.backspace()

    def move_cursor(self, pos: int) -> None:
        self.document.move_cursor(pos)

    def undo(self) -> bool:
        snap = self.history.undo()
        if snap:
            self.document.restore(snap)
            return True
        return False

    def redo(self) -> bool:
        snap = self.history.redo()
        if snap:
            self.document.restore(snap)
            return True
        return False


if __name__ == "__main__":
    print("=== Text Editor with Memento Snapshots ===\n")

    editor = EditorWithHistory()

    editor.type_text("Hello")
    print(f"  Document: \"{editor.document}\"  (cursor at {editor.document.cursor_position})")

    editor.type_text(", World!")
    print(f"  Document: \"{editor.document}\"  (cursor at {editor.document.cursor_position})")

    editor.move_cursor(5)
    editor.type_text(" Python")
    print(f"  Document: \"{editor.document}\"  (cursor at {editor.document.cursor_position})")

    print("\n  --- Undo ---")
    editor.undo()
    print(f"  After undo: \"{editor.document}\"")

    editor.undo()
    print(f"  After undo: \"{editor.document}\"")

    print("\n  --- Redo ---")
    editor.redo()
    print(f"  After redo: \"{editor.document}\"")

    print(f"\n  Total snapshots captured: {len(editor.history._snapshots)}")
    for i, snap in enumerate(editor.history._snapshots):
        dt = time.strftime("%H:%M:%S", time.localtime(snap.timestamp))
        print(f"    {i}: [{dt}] \"{snap.content}\"")
