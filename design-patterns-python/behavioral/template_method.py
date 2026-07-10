"""
Template Method
When to use: When you want to define the skeleton of an algorithm in a base class,
letting subclasses override specific steps without changing the algorithm's structure.
Real-world examples: Django class-based views (get/post/put methods), pytest fixtures
(setup/teardown), data parsers (CSV/JSON/XML with same pipeline), build systems
(compile/link/package steps), machine learning pipelines (load/transform/train/evaluate).
"""

from __future__ import annotations
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
import csv
import json
import io
import time
from typing import Any


@dataclass
class AnalysisResult:
    row_count: int
    columns: list[str]
    sample: list[dict[str, Any]]
    warnings: list[str]


class DataMiner(ABC):
    def mine(self, source: str) -> AnalysisResult:
        self.open(source)
        try:
            raw_data = self.extract_data()
            cleaned = self.clean_data(raw_data)
            result = self.analyze(cleaned)
            return result
        finally:
            self.close()

    @abstractmethod
    def open(self, source: str) -> None:
        ...

    @abstractmethod
    def extract_data(self) -> list[dict[str, Any]]:
        ...

    def clean_data(self, data: list[dict[str, Any]]) -> list[dict[str, Any]]:
        if not data:
            return data
        cleaned: list[dict[str, Any]] = []
        for row in data:
            cleaned.append({k: v for k, v in row.items() if v is not None})
        return cleaned

    @abstractmethod
    def close(self) -> None:
        ...

    def analyze(self, data: list[dict[str, Any]]) -> AnalysisResult:
        if not data:
            return AnalysisResult(0, [], [], ["Empty dataset"])
        columns = list(data[0].keys())
        warnings: list[str] = []
        for i, row in enumerate(data):
            if len(row) != len(columns):
                warnings.append(f"Row {i} has {len(row)} fields, expected {len(columns)}")
        sample = data[:5]
        return AnalysisResult(len(data), columns, sample, warnings)


class CsvMiner(DataMiner):
    def __init__(self) -> None:
        self._file: io.TextIOBase | None = None

    def open(self, source: str) -> None:
        self._file = io.StringIO(source)

    def extract_data(self) -> list[dict[str, Any]]:
        if self._file is None:
            raise RuntimeError("File not opened")
        self._file.seek(0)
        reader = csv.DictReader(self._file)
        return list(reader)

    def close(self) -> None:
        if self._file is not None:
            self._file.close()
            self._file = None


class JsonMiner(DataMiner):
    def __init__(self) -> None:
        self._data: list[dict[str, Any]] = []

    def open(self, source: str) -> None:
        parsed = json.loads(source)
        if isinstance(parsed, list):
            self._data = parsed
        elif isinstance(parsed, dict):
            self._data = [parsed]
        else:
            self._data = []

    def extract_data(self) -> list[dict[str, Any]]:
        return self._data

    def close(self) -> None:
        self._data = []


class LogMiner(DataMiner):
    def __init__(self) -> None:
        self._lines: list[str] = []

    def open(self, source: str) -> None:
        self._lines = source.strip().split("\n")

    def extract_data(self) -> list[dict[str, Any]]:
        records: list[dict[str, Any]] = []
        for line in self._lines:
            if not line.strip():
                continue
            parts = line.split("|")
            if len(parts) >= 4:
                records.append({
                    "timestamp": parts[0].strip(),
                    "level": parts[1].strip(),
                    "module": parts[2].strip(),
                    "message": "|".join(parts[3:]).strip(),
                })
        return records

    def close(self) -> None:
        self._lines = []


def run_miner(miner: DataMiner, label: str, source: str) -> None:
    print(f"\n  --- {label} ---")
    start = time.perf_counter()
    result = miner.mine(source)
    elapsed = time.perf_counter() - start
    print(f"  Rows: {result.row_count}, Columns: {result.columns}")
    print(f"  Sample: {result.sample}")
    if result.warnings:
        print(f"  Warnings: {result.warnings}")
    print(f"  Time: {elapsed*1000:.2f}ms")


if __name__ == "__main__":
    print("=== Data Mining Framework (Template Method) ===\n")

    csv_data = (
        "name,age,city,email\n"
        "Alice,30,New York,alice@example.com\n"
        "Bob,25,London,\n"
        "Charlie,35,Paris,charlie@example.com\n"
        "Diana,28,Berlin,diana@example.com\n"
    )

    json_data = json.dumps([
        {"product": "Widget", "price": 9.99, "in_stock": True},
        {"product": "Gadget", "price": 24.99, "in_stock": False},
        {"product": "Doohickey", "price": 4.99, "in_stock": True},
    ])

    log_data = (
        "2024-01-15 10:30:00|ERROR|auth|Invalid login attempt from IP 192.168.1.100\n"
        "2024-01-15 10:31:00|INFO|db|Query completed in 42ms\n"
        "2024-01-15 10:32:00|WARN|cache|Cache miss for key user:1234\n"
        "2024-01-15 10:33:00|ERROR|payment|Payment processing failed: insufficient funds\n"
    )

    run_miner(CsvMiner(), "CSV Miner", csv_data)
    run_miner(JsonMiner(), "JSON Miner", json_data)
    run_miner(LogMiner(), "Log Miner", log_data)

    print("\n  All miners executed successfully via the same template.")
