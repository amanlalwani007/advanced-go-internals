"""
** Strategy Pattern (Interview Important)
When to use: When you have multiple algorithms for a task and want to select one at
runtime. The pattern defines a family of algorithms, encapsulates each one, and makes
them interchangeable.
Real-world examples: Django authentication backends (AUTHENTICATION_BACKENDS),
Python sorting (key= parameter), compression algorithms (ZIP/RAR/7z), payment
processors (Stripe/PayPal/Square), formatting/encoding strategies, route
calculation in maps (shortest/fastest/scenic).
"""

from __future__ import annotations
from abc import ABC, abstractmethod
from dataclasses import dataclass
import zipfile
import tarfile
import io
import time


class CompressionStrategy(ABC):
    extension: str = ""

    @abstractmethod
    def compress(self, files: dict[str, bytes]) -> bytes:
        ...

    @abstractmethod
    def decompress(self, data: bytes) -> dict[str, bytes]:
        ...


class ZipStrategy(CompressionStrategy):
    extension = ".zip"

    def compress(self, files: dict[str, bytes]) -> bytes:
        buf = io.BytesIO()
        with zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED) as zf:
            for name, content in files.items():
                zf.writestr(name, content)
        return buf.getvalue()

    def decompress(self, data: bytes) -> dict[str, bytes]:
        buf = io.BytesIO(data)
        result: dict[str, bytes] = {}
        with zipfile.ZipFile(buf, "r") as zf:
            for name in zf.namelist():
                result[name] = zf.read(name)
        return result


class TarStrategy(CompressionStrategy):
    extension = ".tar"

    def compress(self, files: dict[str, bytes]) -> bytes:
        buf = io.BytesIO()
        with tarfile.open(fileobj=buf, mode="w") as tf:
            for name, content in files.items():
                info = tarfile.TarInfo(name=name)
                info.size = len(content)
                tf.addfile(info, io.BytesIO(content))
        return buf.getvalue()

    def decompress(self, data: bytes) -> dict[str, bytes]:
        buf = io.BytesIO(data)
        result: dict[str, bytes] = {}
        with tarfile.open(fileobj=buf, mode="r") as tf:
            for member in tf.getmembers():
                if member.isfile():
                    f = tf.extractfile(member)
                    if f is not None:
                        result[member.name] = f.read()
        return result


class GzipTarStrategy(CompressionStrategy):
    extension = ".tar.gz"

    def compress(self, files: dict[str, bytes]) -> bytes:
        buf = io.BytesIO()
        with tarfile.open(fileobj=buf, mode="w:gz") as tf:
            for name, content in files.items():
                info = tarfile.TarInfo(name=name)
                info.size = len(content)
                tf.addfile(info, io.BytesIO(content))
        return buf.getvalue()

    def decompress(self, data: bytes) -> dict[str, bytes]:
        buf = io.BytesIO(data)
        result: dict[str, bytes] = {}
        with tarfile.open(fileobj=buf, mode="r:gz") as tf:
            for member in tf.getmembers():
                if member.isfile():
                    f = tf.extractfile(member)
                    if f is not None:
                        result[member.name] = f.read()
        return result


@dataclass
class Compressor:
    strategy: CompressionStrategy

    def set_strategy(self, strategy: CompressionStrategy) -> None:
        self.strategy = strategy

    def archive(self, files: dict[str, bytes]) -> bytes:
        return self.strategy.compress(files)

    def extract(self, data: bytes) -> dict[str, bytes]:
        return self.strategy.decompress(data)


if __name__ == "__main__":
    print("=== File Compression Strategy ===\n")

    sample_files = {
        "readme.txt": b"Hello, this is a sample file for compression testing.\n" * 100,
        "notes.md": b"## Design Patterns\n\nBehavioral patterns are about communication.\n" * 50,
        "config.json": b'{"version": 1, "debug": false, "max_retries": 3}\n' * 20,
    }

    print(f"  Original data: {sum(len(v) for v in sample_files):,} bytes across {len(sample_files)} files\n")

    strategies: list[CompressionStrategy] = [
        ZipStrategy(),
        TarStrategy(),
        GzipTarStrategy(),
    ]

    compressor = Compressor(strategies[0])

    for strategy in strategies:
        compressor.set_strategy(strategy)
        start = time.perf_counter()
        compressed = compressor.archive(sample_files)
        elapsed = time.perf_counter() - start
        ratio = len(compressed) / sum(len(v) for v in sample_files.values()) * 100

        extracted = compressor.extract(compressed)
        assert extracted == sample_files, "Round-trip failed!"

        print(f"  {strategy.extension:>8s}: {len(compressed):>8,} bytes ({ratio:5.1f}%) in {elapsed*1000:.1f}ms")

    print("\n  All strategies verified: round-trip compression/decompression OK")

