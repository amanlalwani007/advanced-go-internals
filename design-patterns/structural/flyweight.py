"""
Flyweight Pattern
When to use: When you need to support a large number of fine-grained objects efficiently by sharing common state. Use when memory savings are important and objects share repeated intrinsic state that can be extracted.

Real-world examples:
- String interning in Python/Java (repeated strings share memory)
- Java Integer cache (-128 to 127)
- Game engine particle systems (shared texture/shader, unique position)
- Word processor character formatting (shared font/style, unique position)
- Browser DOM node pooling
"""

from dataclasses import dataclass, field
from typing import Optional
import sys


@dataclass(frozen=True)
class CharacterStyle:
    font_family: str
    font_size: int
    bold: bool
    italic: bool
    underline: bool
    color: str
    background_color: Optional[str] = None

    def render_start(self) -> str:
        parts = [
            f"font-family: '{self.font_family}'",
            f"font-size: {self.font_size}px",
            f"font-weight: {'bold' if self.bold else 'normal'}",
            f"font-style: {'italic' if self.italic else 'normal'}",
            f"text-decoration: {'underline' if self.underline else 'none'}",
            f"color: {self.color}",
        ]
        if self.background_color:
            parts.append(f"background-color: {self.background_color}")
        return f"<span style=\"{'; '.join(parts)}\">"

    def render_end(self) -> str:
        return "</span>"


class StyleFactory:
    _cache: dict[tuple, CharacterStyle] = {}

    def get_style(
        self,
        font_family: str,
        font_size: int,
        bold: bool = False,
        italic: bool = False,
        underline: bool = False,
        color: str = "#000000",
        background_color: Optional[str] = None,
    ) -> CharacterStyle:
        key = (font_family, font_size, bold, italic, underline, color, background_color)
        if key not in self._cache:
            self._cache[key] = CharacterStyle(
                font_family=font_family,
                font_size=font_size,
                bold=bold,
                italic=italic,
                underline=underline,
                color=color,
                background_color=background_color,
            )
            print(f"  [StyleFactory] Created new style: {font_family} {font_size}px {'B' if bold else ''}{'I' if italic else ''}{'U' if underline else ''} {color}")
        return self._cache[key]

    @property
    def cache_size(self) -> int:
        return len(self._cache)

    def clear(self) -> None:
        self._cache.clear()


@dataclass
class Character:
    char: str
    style: CharacterStyle
    position_x: float
    position_y: float

    def render_html(self) -> str:
        return f"{self.style.render_start()}{self.char}{self.style.render_end()}"

    def render_ansi(self) -> str:
        result = ""
        if self.style.bold:
            result += "\033[1m"
        if self.style.italic:
            result += "\033[3m"
        if self.style.underline:
            result += "\033[4m"
        color_map = {
            "#000000": "\033[30m",
            "#ff0000": "\033[31m",
            "#00ff00": "\033[32m",
            "#ffff00": "\033[33m",
            "#0000ff": "\033[34m",
            "#ff00ff": "\033[35m",
            "#00ffff": "\033[36m",
            "#ffffff": "\033[37m",
            "#333333": "\033[90m",
            "#cc0000": "\033[91m",
        }
        result += color_map.get(self.style.color.lower(), "\033[0m")
        result += self.char
        result += "\033[0m"
        return result


class FormattedText:
    def __init__(self):
        self._characters: list[Character] = []
        self._factory = StyleFactory()
        self._cursor_x = 0.0
        self._cursor_y = 0.0

    def add_text(
        self,
        text: str,
        font_family: str = "Arial",
        font_size: int = 14,
        bold: bool = False,
        italic: bool = False,
        underline: bool = False,
        color: str = "#000000",
        background_color: Optional[str] = None,
    ) -> None:
        style = self._factory.get_style(font_family, font_size, bold, italic, underline, color, background_color)
        for ch in text:
            self._characters.append(Character(
                char=ch,
                style=style,
                position_x=self._cursor_x,
                position_y=self._cursor_y,
            ))
            self._cursor_x += font_size * 0.6

    def newline(self, font_size: int = 14) -> None:
        self._cursor_x = 0.0
        self._cursor_y += font_size * 1.5

    def render_html(self) -> str:
        parts = ["<!DOCTYPE html><html><body>"]
        current_style: Optional[CharacterStyle] = None
        for char in self._characters:
            if char.style != current_style:
                if current_style:
                    parts.append("</span>")
                parts.append(char.style.render_start())
                current_style = char.style
            parts.append(char.char)
        if current_style:
            parts.append("</span>")
        parts.append("</body></html>")
        return "".join(parts)

    def render_plain(self) -> str:
        return "".join(c.char for c in self._characters)

    def render_ansi(self) -> str:
        result = []
        current_style: Optional[CharacterStyle] = None
        for char in self._characters:
            if char.style != current_style:
                if current_style:
                    result.append("\033[0m")
                current_style = char.style
            result.append(char.render_ansi())
        if current_style:
            result.append("\033[0m")
        return "".join(result)

    def search(self, keyword: str) -> list[tuple[int, int, str]]:
        results = []
        text = self.render_plain()
        start = 0
        while True:
            pos = text.find(keyword, start)
            if pos == -1:
                break
            context_start = max(0, pos - 10)
            context_end = min(len(text), pos + len(keyword) + 10)
            context = text[context_start:context_end]
            results.append((pos, pos + len(keyword), context))
            start = pos + 1
        return results

    @property
    def character_count(self) -> int:
        return len(self._characters)

    @property
    def unique_styles(self) -> int:
        return self._factory.cache_size

    def memory_report(self) -> str:
        char_size = sys.getsizeof(self._characters) + len(self._characters) * 120
        style_entries = sum(sys.getsizeof(v) for v in self._factory._cache.values())
        style_keys = sum(sys.getsizeof(k) for k in self._factory._cache.keys())
        style_overhead = sys.getsizeof(self._factory._cache)
        total = char_size + style_entries + style_keys + style_overhead
        savings = 0
        if self.unique_styles > 0:
            without_flyweight = char_size + (self.character_count * (style_entries // self.unique_styles + style_keys // self.unique_styles))
            savings = without_flyweight - total
            savings_pct = (savings / without_flyweight) * 100 if without_flyweight > 0 else 0
        else:
            savings_pct = 0

        return (
            f"Characters: {self.character_count}\n"
            f"Unique styles: {self.unique_styles}\n"
            f"Total memory estimate: {total:,} bytes\n"
            f"Estimated memory saved: {savings:,} bytes ({savings_pct:.1f}% reduction)"
        )


def generate_large_document() -> FormattedText:
    doc = FormattedText()

    doc.add_text("The Flyweight Pattern in Text Rendering\n", "Georgia", 28, bold=True, color="#1a1a2e")
    doc.newline(28)

    doc.add_text("Introduction\n", "Georgia", 22, bold=True, color="#16213e")
    doc.newline(22)

    body_text = (
        "The Flyweight pattern is a structural design pattern that allows programs "
        "to support vast quantities of objects by sharing common parts of their state. "
        "Instead of storing redundant data in each object, the extrinsic state "
        "(position, context) is kept separate from the intrinsic state (style, formatting) "
        "which is shared across many objects through a factory."
    )
    doc.add_text(body_text, "Georgia", 14, color="#333333")
    doc.newline(14)
    doc.newline(14)

    doc.add_text("How It Works\n", "Georgia", 22, bold=True, color="#16213e")
    doc.newline(22)

    doc.add_text("In this example, every ", "Georgia", 14, color="#333333")
    doc.add_text("character", "Georgia", 14, bold=True, italic=True, color="#e94560")
    doc.add_text(" in the document stores a reference to a shared ", "Georgia", 14, color="#333333")
    doc.add_text("CharacterStyle", "Courier New", 14, bold=True, color="#0f3460")
    doc.add_text(" object rather than duplicating font family, size, weight, and color for every single glyph.", "Georgia", 14, color="#333333")
    doc.newline(14)
    doc.newline(14)

    doc.add_text("Performance Benefits\n", "Georgia", 22, bold=True, color="#16213e")
    doc.newline(22)

    doc.add_text("For a document with ", "Georgia", 14, color="#333333")
    doc.add_text("100,000 characters", "Georgia", 14, bold=True, color="#e94560")
    doc.add_text(" and only 5-10 unique style combinations, memory usage drops by over 90% compared to storing full style data per character.", "Georgia", 14, color="#333333")
    doc.newline(14)
    doc.newline(14)

    doc.add_text("Code Example:\n", "Courier New", 16, bold=True, color="#0f3460")
    doc.newline(16)

    doc.add_text("style = factory.get_style('Arial', 14, bold=True, color='#333')\nchar = Character('A', style, x=10.0, y=20.0)", "Courier New", 13, color="#2d4059")
    doc.newline(13)
    doc.newline(13)

    doc.add_text("Common Use Cases:\n", "Georgia", 18, bold=True, color="#16213e")
    doc.newline(18)
    doc.add_text("  - Text editors and word processors\n", "Georgia", 14, color="#333333")
    doc.add_text("  - Game engines (particle systems, tile maps)\n", "Georgia", 14, color="#333333")
    doc.add_text("  - GUI widget theming engines\n", "Georgia", 14, color="#333333")
    doc.add_text("  - Caching and connection pooling\n", "Georgia", 14, color="#333333")
    doc.add_text("  - String interning in compilers and runtimes\n", "Georgia", 14, color="#333333")

    return doc


if __name__ == "__main__":
    print("=== Flyweight Pattern: Document Rendering ===\n")

    doc = generate_large_document()

    print("--- Plain Text Preview (first 200 chars) ---")
    print(doc.render_plain()[:200])
    print()

    print("--- Searching for 'Flyweight' ---")
    for start, end, ctx in doc.search("Flyweight"):
        print(f"  Position {start}-{end}: ...{ctx}...")
    print()

    print("--- Memory Report ---")
    print(doc.memory_report())
    print()

    print("--- Creating a large document to demonstrate scaling ---")
    large_doc = FormattedText()
    for i in range(1000):
        large_doc.add_text(f"Line {i}: This is sample text with ", "Arial", 12, color="#333333")
        large_doc.add_text("mixed formatting ", "Arial", 12, bold=True, italic=True, color="#e94560")
        large_doc.add_text("for demonstration.\n", "Arial", 12, color="#333333")

    print(large_doc.memory_report())
    print()

    print("--- Searching large document ---")
    for start, end, ctx in large_doc.search("mixed formatting"):
        print(f"  Found at {start}: ...{ctx}...")
        break
