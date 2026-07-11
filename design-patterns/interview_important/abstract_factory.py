"""
** Abstract Factory Pattern (Interview Important)
When to use:
- When a system should be independent of how its products are created, composed, and represented
- When a system should be configured with one of multiple families of products
- When you want to enforce that products from the same family are used together

Real-world examples:
- Qt toolkit: QStyleFactory creates platform-specific GUI widgets
- Python db-api (PEP 249): Different database drivers implement the same connection/cursor interface
- tkinter.ttk: Themed widget sets across platforms (Windows/Classic/Alt)
- Pillow: ImagePlugin factories for different image formats (PNG/JPEG/GIF)
"""

from abc import ABC, abstractmethod
from typing import Protocol


class Button(ABC):
    @abstractmethod
    def render(self) -> str:
        ...

    @abstractmethod
    def on_click(self) -> str:
        ...


class Checkbox(ABC):
    @abstractmethod
    def render(self) -> str:
        ...

    @abstractmethod
    def toggle(self, checked: bool) -> str:
        ...


class Scrollbar(ABC):
    @abstractmethod
    def render(self) -> str:
        ...

    @abstractmethod
    def scroll_to(self, position: float) -> str:
        ...


class WindowsButton(Button):
    def render(self) -> str:
        return "[WinButton] Click me"

    def on_click(self) -> str:
        return "Windows button clicked - opening dialog"


class WindowsCheckbox(Checkbox):
    def render(self) -> str:
        return "[WinCheckbox]  [x] Accept terms"

    def toggle(self, checked: bool) -> str:
        state = "checked" if checked else "unchecked"
        return f"Windows checkbox is now {state}"


class WindowsScrollbar(Scrollbar):
    def render(self) -> str:
        return "[WinScrollbar] ##############"

    def scroll_to(self, position: float) -> str:
        return f"Windows scrollbar moved to {position:.0%}"


class MacButton(Button):
    def render(self) -> str:
        return "[MacButton] Click me"

    def on_click(self) -> str:
        return "macOS button clicked - opening sheet"


class MacCheckbox(Checkbox):
    def render(self) -> str:
        return "[MacCheckbox] [X] Accept terms"

    def toggle(self, checked: bool) -> str:
        state = "checked" if checked else "unchecked"
        return f"macOS checkbox is now {state}"


class MacScrollbar(Scrollbar):
    def render(self) -> str:
        return "[MacScrollbar] =============="

    def scroll_to(self, position: float) -> str:
        return f"macOS scrollbar moved to {position:.0%}"


class LinuxButton(Button):
    def render(self) -> str:
        return "[GnomeButton] << Click me >>"

    def on_click(self) -> str:
        return "Linux button clicked - emitting signal"


class LinuxCheckbox(Checkbox):
    def render(self) -> str:
        return "[GnomeCheckbox] [V] Accept terms"

    def toggle(self, checked: bool) -> str:
        state = "checked" if checked else "unchecked"
        return f"Linux checkbox is now {state}"


class LinuxScrollbar(Scrollbar):
    def render(self) -> str:
        return "[GnomeScrollbar] ========+----"

    def scroll_to(self, position: float) -> str:
        return f"Linux scrollbar moved to {position:.0%}"


class UIFactory(ABC):
    """Abstract factory — declares a family of product creation methods."""

    @abstractmethod
    def create_button(self) -> Button:
        ...

    @abstractmethod
    def create_checkbox(self) -> Checkbox:
        ...

    @abstractmethod
    def create_scrollbar(self) -> Scrollbar:
        ...


class WindowsFactory(UIFactory):
    def create_button(self) -> Button:
        return WindowsButton()

    def create_checkbox(self) -> Checkbox:
        return WindowsCheckbox()

    def create_scrollbar(self) -> Scrollbar:
        return WindowsScrollbar()


class MacFactory(UIFactory):
    def create_button(self) -> Button:
        return MacButton()

    def create_checkbox(self) -> Checkbox:
        return MacCheckbox()

    def create_scrollbar(self) -> Scrollbar:
        return MacScrollbar()


class LinuxFactory(UIFactory):
    def create_button(self) -> Button:
        return LinuxButton()

    def create_checkbox(self) -> Checkbox:
        return LinuxCheckbox()

    def create_scrollbar(self) -> Scrollbar:
        return LinuxScrollbar()


class Application:
    """Client code that uses the abstract factory to build a consistent UI."""

    def __init__(self, factory: UIFactory, window_title: str = "Untitled") -> None:
        self.factory = factory
        self.window_title = window_title
        self.button = factory.create_button()
        self.checkbox = factory.create_checkbox()
        self.scrollbar = factory.create_scrollbar()

    def render_ui(self) -> None:
        print(f"\n  === {self.window_title} ===")
        print(f"  Widgets ({type(self.factory).__name__}):")
        print(f"    {self.button.render()}")
        print(f"    {self.checkbox.render()}")
        print(f"    {self.scrollbar.render()}")

    def simulate_interaction(self) -> None:
        print(f"\n  Interactions:")
        print(f"    -> {self.button.on_click()}")
        print(f"    -> {self.checkbox.toggle(True)}")
        print(f"    -> {self.scrollbar.scroll_to(0.65)}")


if __name__ == "__main__":
    import sys

    platforms: dict[str, UIFactory] = {
        "windows": WindowsFactory(),
        "mac": MacFactory(),
        "linux": LinuxFactory(),
    }

    apps = {
        "windows": Application(platforms["windows"], "MyApp - Windows Build"),
        "mac": Application(platforms["mac"], "MyApp - macOS Build"),
        "linux": Application(platforms["linux"], "MyApp - Linux Build"),
    }

    for platform_name, app in apps.items():
        app.render_ui()
        app.simulate_interaction()

