"""
** Observer Pattern (Interview Important)
When to use: When one object (subject) needs to notify many other objects (observers)
about state changes without being coupled to them. Establishes a one-to-many
dependency.
Real-world examples: Django signals (post_save, pre_delete), Kafka pub-sub systems,
RxPY reactive streams, JavaScript EventTarget/addEventListener, GUIs event listeners
(button.click), WebSocket broadcast, Celery task result backends.
"""

from __future__ import annotations
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Protocol
import time


class Observer(Protocol):
    def update(self, symbol: str, old_price: float, new_price: float) -> None:
        ...


@dataclass
class Investor:
    name: str
    portfolio: dict[str, int] = field(default_factory=dict)

    def update(self, symbol: str, old_price: float, new_price: float) -> None:
        change = new_price - old_price
        pct = ((new_price - old_price) / old_price) * 100
        direction = "+" if change >= 0 else "-"
        if symbol in self.portfolio:
            impact = self.portfolio[symbol] * change
            print(f"  [{self.name}] {direction} {symbol}: ${old_price:.2f} -> ${new_price:.2f} "
                  f"({pct:+.2f}%) | Portfolio impact: ${impact:+.2f}")
        else:
            print(f"  [{self.name}] {direction} {symbol}: ${old_price:.2f} -> ${new_price:.2f} "
                  f"({pct:+.2f}%)")


class TradingBot:
    def __init__(self, name: str, threshold_pct: float = 5.0) -> None:
        self.name = name
        self.threshold_pct = threshold_pct

    def update(self, symbol: str, old_price: float, new_price: float) -> None:
        pct = ((new_price - old_price) / old_price) * 100
        if abs(pct) >= self.threshold_pct:
            action = "BUY" if pct > 0 else "SELL"
            print(f"  ** [{self.name}] ALERT: {action} {symbol} -- moved {pct:+.2f}%")

    def __repr__(self) -> str:
        return f"TradingBot('{self.name}')"


@dataclass
class Stock:
    symbol: str
    _price: float = 0.0
    _observers: list = field(default_factory=list)

    def attach(self, observer: Observer) -> None:
        if observer not in self._observers:
            self._observers.append(observer)

    def detach(self, observer: Observer) -> None:
        self._observers.remove(observer)

    @property
    def price(self) -> float:
        return self._price

    @price.setter
    def price(self, new_price: float) -> None:
        old_price = self._price
        if old_price == new_price:
            return
        self._price = new_price
        self._notify_all(old_price, new_price)

    def _notify_all(self, old_price: float, new_price: float) -> None:
        for obs in self._observers:
            obs.update(self.symbol, old_price, new_price)


@dataclass
class StockMarket:
    stocks: dict[str, Stock] = field(default_factory=dict)

    def add_stock(self, symbol: str, initial_price: float = 100.0) -> Stock:
        stock = Stock(symbol, initial_price)
        self.stocks[symbol] = stock
        return stock

    def update_price(self, symbol: str, new_price: float) -> None:
        if symbol not in self.stocks:
            raise KeyError(f"Unknown stock: {symbol}")
        stock = self.stocks[symbol]
        stock.price = new_price

    def get_stock(self, symbol: str) -> Stock:
        return self.stocks[symbol]


if __name__ == "__main__":
    print("=== Stock Market Observer System ===\n")

    market = StockMarket()
    aapl = market.add_stock("AAPL", 150.00)
    googl = market.add_stock("GOOGL", 2800.00)
    tsla = market.add_stock("TSLA", 700.00)

    alice = Investor("Alice", {"AAPL": 50, "TSLA": 10})
    bob = Investor("Bob", {"GOOGL": 5})
    bot = TradingBot("AlphaBot", threshold_pct=3.0)

    aapl.attach(alice)
    aapl.attach(bot)
    googl.attach(bob)
    googl.attach(bot)
    tsla.attach(alice)
    tsla.attach(bot)

    print("  --- Price Update 1: AAPL rises ---")
    market.update_price("AAPL", 155.50)
    print()

    print("  --- Price Update 2: GOOGL drops ---")
    market.update_price("GOOGL", 2720.00)
    print()

    print("  --- Price Update 3: TSLA surges ---")
    market.update_price("TSLA", 750.00)
    print()

    print("  --- Bob unsubscribes from GOOGL ---")
    googl.detach(bob)
    market.update_price("GOOGL", 2680.00)
    print()

    print("  Observer count per stock:")
    for sym, stock in market.stocks.items():
        print(f"    {sym}: {len(stock._observers)} observer(s)")

