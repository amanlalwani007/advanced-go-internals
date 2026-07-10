"""
Composite Pattern
When to use: When you need to treat individual objects and compositions of objects uniformly. Use when clients should ignore the difference between compositions of objects and individual objects, or when you have a tree structure with part-whole hierarchies.

Real-world examples:
- File system explorers (files and directories)
- DOM tree in web browsers (elements and text nodes)
- UI widget trees (containers and leaf widgets)
- Scene graphs in game engines
- Organizational hierarchy charts
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional
import fnmatch


class FileSystemComponent(ABC):
    @property
    @abstractmethod
    def name(self) -> str:
        pass

    @abstractmethod
    def get_size(self) -> int:
        pass

    @abstractmethod
    def display(self, indent: str = "") -> str:
        pass

    @abstractmethod
    def search(self, pattern: str) -> list["FileSystemComponent"]:
        pass


@dataclass
class File(FileSystemComponent):
    _name: str
    _size: int
    _created: datetime = field(default_factory=datetime.now)
    _extension: str = ""

    def __post_init__(self):
        if "." in self._name:
            self._extension = self._name.rsplit(".", 1)[1]

    @property
    def name(self) -> str:
        return self._name

    def get_size(self) -> int:
        return self._size

    def display(self, indent: str = "") -> str:
        size_str = self._format_size(self._size)
        line = f"{indent}[File] {self._name} ({size_str})"
        print(line)
        return line

    def search(self, pattern: str) -> list[FileSystemComponent]:
        if fnmatch.fnmatch(self._name.lower(), pattern.lower()):
            return [self]
        return []

    @staticmethod
    def _format_size(bytes_: int) -> str:
        if bytes_ < 1024:
            return f"{bytes_} B"
        elif bytes_ < 1024 ** 2:
            return f"{bytes_ / 1024:.1f} KB"
        elif bytes_ < 1024 ** 3:
            return f"{bytes_ / 1024 ** 2:.1f} MB"
        else:
            return f"{bytes_ / 1024 ** 3:.1f} GB"


@dataclass
class Directory(FileSystemComponent):
    _name: str
    _children: list[FileSystemComponent] = field(default_factory=list)

    @property
    def name(self) -> str:
        return self._name

    def add(self, component: FileSystemComponent) -> None:
        self._children.append(component)

    def remove(self, component: FileSystemComponent) -> bool:
        if component in self._children:
            self._children.remove(component)
            return True
        return False

    def get_child(self, name: str) -> Optional[FileSystemComponent]:
        for child in self._children:
            if child.name == name:
                return child
        return None

    def get_size(self) -> int:
        return sum(child.get_size() for child in self._children)

    def display(self, indent: str = "") -> str:
        line = f"{indent}[Dir] {self._name}/ ({self._format_size(self.get_size())})"
        print(line)
        for child in self._children:
            child.display(indent + "  ")
        return line

    def search(self, pattern: str) -> list[FileSystemComponent]:
        results = []
        if fnmatch.fnmatch(self._name.lower(), pattern.lower()):
            results.append(self)
        for child in self._children:
            results.extend(child.search(pattern))
        return results

    def count_files(self) -> int:
        count = 0
        for child in self._children:
            if isinstance(child, File):
                count += 1
            elif isinstance(child, Directory):
                count += child.count_files()
        return count

    def find_duplicates_by_name(self) -> dict[str, list[str]]:
        name_map: dict[str, list[str]] = {}
        self._build_name_map(name_map, "")
        return {k: v for k, v in name_map.items() if len(v) > 1}

    def _build_name_map(self, name_map: dict[str, list[str]], path: str) -> None:
        current_path = f"{path}/{self._name}" if path else self._name
        for child in self._children:
            child_path = f"{current_path}/{child.name}"
            if isinstance(child, File):
                name_map.setdefault(child.name, []).append(child_path)
            elif isinstance(child, Directory):
                name_map.setdefault(child.name, []).append(child_path)
                child._build_name_map(name_map, current_path)

    @staticmethod
    def _format_size(bytes_: int) -> str:
        if bytes_ < 1024:
            return f"{bytes_} B"
        elif bytes_ < 1024 ** 2:
            return f"{bytes_ / 1024:.1f} KB"
        elif bytes_ < 1024 ** 3:
            return f"{bytes_ / 1024 ** 2:.1f} MB"
        else:
            return f"{bytes_ / 1024 ** 3:.1f} GB"


def build_sample_filesystem() -> Directory:
    root = Directory("home")

    docs = Directory("documents")
    docs.add(File("resume.pdf", 245_000))
    docs.add(File("cover_letter.pdf", 120_000))
    docs.add(File("notes.txt", 4_200))

    projects = Directory("projects")
    web = Directory("web-app")
    web.add(File("index.html", 3_500))
    web.add(File("style.css", 12_000))
    web.add(File("app.js", 45_000))
    web.add(File("package.json", 800))
    projects.add(web)

    api = Directory("api-service")
    api.add(File("main.py", 8_000))
    api.add(File("routes.py", 15_000))
    api.add(File("models.py", 22_000))
    api.add(File("requirements.txt", 400))
    api.add(File("Dockerfile", 1_200))
    projects.add(api)

    media = Directory("media")
    media.add(File("vacation_photo.jpg", 3_200_000))
    media.add(File("family_video.mp4", 128_000_000))
    media.add(File("podcast_episode.mp3", 64_000_000))

    downloads = Directory("downloads")
    downloads.add(File("ubuntu-24.04.iso", 4_800_000_000))
    downloads.add(File("python-3.12-installer.exe", 25_000_000))

    root.add(docs)
    root.add(projects)
    root.add(media)
    root.add(downloads)

    return root


if __name__ == "__main__":
    fs = build_sample_filesystem()

    print("=== File System Tree ===")
    fs.display()

    print(f"\nTotal size: {Directory._format_size(fs.get_size())}")
    print(f"Total files: {fs.count_files()}")

    print("\n=== Searching for '*.py' ===")
    for comp in fs.search("*.py"):
        print(f"  Found: {comp.name}")

    print("\n=== Searching for 'Dockerfile' ===")
    for comp in fs.search("Dockerfile"):
        print(f"  Found: {comp.name}")

    print("\n=== Duplicate file names ===")
    dups = fs.find_duplicates_by_name()
    if dups:
        for name, paths in dups.items():
            print(f"  '{name}' appears {len(paths)} times:")
            for p in paths:
                print(f"    - {p}")
    else:
        print("  No duplicates found.")

    print("\n=== Removing 'notes.txt' ===")
    docs = fs.get_child("documents")
    if isinstance(docs, Directory):
        notes = docs.get_child("notes.txt")
        if isinstance(notes, File):
            docs.remove(notes)
            print(f"  Removed. Directory 'documents' size now: {Directory._format_size(docs.get_size())}")

    print("\n=== Updated tree ===")
    fs.display()
