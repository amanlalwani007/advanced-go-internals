"""
Iterator
When to use: When you need to traverse a complex data structure or paginated resource
without exposing its internal representation. Provides a standard way to access elements
sequentially.
Real-world examples: Django QuerySet iteration (lazy evaluation), database cursors,
Python generators (yield), paginated REST API clients, file reading line-by-line
with readline(), network packet streams.
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Iterator, Any
import json
import time


@dataclass
class Post:
    id: int
    title: str
    body: str

    def __str__(self) -> str:
        return f"Post(id={self.id}, title='{self.title[:40]}...')"


class PostRepository:
    """Simulates a paginated database/API that returns pages of Posts."""

    def __init__(self, total_posts: int = 100, page_size: int = 10) -> None:
        self.total_posts = total_posts
        self.page_size = page_size
        self._data = [
            Post(
                id=i,
                title=f"Article about design pattern {i}",
                body=f"This is the body content for post number {i}. " * 5,
            )
            for i in range(1, total_posts + 1)
        ]

    def fetch_page(self, page: int) -> list[Post]:
        start = (page - 1) * self.page_size
        end = start + self.page_size
        time.sleep(0.05)
        return self._data[start:end]


class PaginatedIterator(Iterator[Post]):
    def __init__(self, repository: PostRepository) -> None:
        self._repo = repository
        self._page: int = 1
        self._index: int = 0
        self._buffer: list[Post] = []
        self._exhausted: bool = False

    def _load_next_page(self) -> None:
        if self._exhausted:
            return
        self._buffer = self._repo.fetch_page(self._page)
        self._page += 1
        self._index = 0
        if not self._buffer:
            self._exhausted = True

    def __next__(self) -> Post:
        if self._index >= len(self._buffer):
            if self._exhausted:
                raise StopIteration
            self._load_next_page()
            if not self._buffer:
                self._exhausted = True
                raise StopIteration
        post = self._buffer[self._index]
        self._index += 1
        return post

    def __iter__(self) -> Iterator[Post]:
        return self


class PostCollection:
    def __init__(self, repository: PostRepository) -> None:
        self._repo = repository

    def __iter__(self) -> Iterator[Post]:
        return PaginatedIterator(self._repo)


if __name__ == "__main__":
    print("=== Paginated API Iterator ===\n")

    repo = PostRepository(total_posts=37, page_size=10)
    collection = PostCollection(repo)

    count = 0
    for post in collection:
        count += 1
        print(f"  #{count:2d}: {post}")
        if count >= 15:
            break

    print(f"\n  Iterated through {count} posts (fetched pages on demand)")

    print("\n  --- Re-iterating from scratch ---")
    for post in collection:
        print(f"  First post again: {post.title}")
        break
