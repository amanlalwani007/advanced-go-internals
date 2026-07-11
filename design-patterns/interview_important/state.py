"""
** State Pattern (Interview Important)
When to use: When an object's behavior depends on its internal state and must change
at runtime. The pattern allows an object to alter its behavior when its internal state
changes, appearing to change its class.
Real-world examples: TCP connection states (LISTEN, SYN_SENT, ESTABLISHED, CLOSE_WAIT),
workflow engines (approval processes), game character states (idle, running, jumping,
attacking), order processing (pending -> paid -> shipped -> delivered), vending machines,
traffic lights.
"""

from __future__ import annotations
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from enum import Enum, auto



class Item(Enum):
    COLA = "Cola"
    CHIPS = "Chips"
    CANDY = "Candy"
    WATER = "Water"
    CHOCOLATE = "Chocolate"


@dataclass
class Product:
    item: Item
    quantity: int


class VendingMachineState(ABC):
    def __init__(self, machine: VendingMachine) -> None:
        self.machine = machine

    @abstractmethod
    def insert_coin(self, amount: float) -> str:
        ...

    @abstractmethod
    def select_item(self, item: Item) -> str:
        ...

    @abstractmethod
    def dispense(self) -> str:
        ...

    @abstractmethod
    def refund(self) -> str:
        ...


class IdleState(VendingMachineState):
    def insert_coin(self, amount: float) -> str:
        self.machine.balance = amount
        self.machine.set_state(self.machine.selecting_state)
        return f"Inserted ${amount:.2f}. Balance: ${self.machine.balance:.2f}"

    def select_item(self, item: Item) -> str:
        return "Insert coin first before selecting an item."

    def dispense(self) -> str:
        return "Insert coin first."

    def refund(self) -> str:
        return "No coins to refund."


class SelectingState(VendingMachineState):
    def insert_coin(self, amount: float) -> str:
        self.machine.balance += amount
        return f"Added ${amount:.2f}. Balance: ${self.machine.balance:.2f}"

    def select_item(self, item: Item) -> str:
        product = self.machine.inventory.get(item)
        if product is None:
            return f"Item '{item.value}' not found."
        if product.quantity == 0:
            self.machine.set_state(self.machine.out_of_stock_state)
            return f"{item.value} is out of stock."
        price = self.machine.prices.get(item, 0)
        if self.machine.balance < price:
            return f"Insufficient balance. {item.value} costs ${price:.2f}, inserted ${self.machine.balance:.2f}."
        self.machine.selected_item = item
        self.machine.set_state(self.machine.dispensing_state)
        return self.machine.dispense()

    def dispense(self) -> str:
        return "Select an item first."

    def refund(self) -> str:
        amount = self.machine.balance
        self.machine.balance = 0.0
        self.machine.selected_item = None
        self.machine.set_state(self.machine.idle_state)
        return f"Refunded ${amount:.2f}. Thank you."


class DispensingState(VendingMachineState):
    def insert_coin(self, amount: float) -> str:
        return "Please wait, dispensing your item."

    def select_item(self, item: Item) -> str:
        return "Please wait, dispensing your item."

    def dispense(self) -> str:
        item = self.machine.selected_item
        if item is None:
            self.machine.set_state(self.machine.idle_state)
            return "Nothing to dispense."
        product = self.machine.inventory.get(item)
        if product is None or product.quantity == 0:
            self.machine.set_state(self.machine.out_of_stock_state)
            return f"{item.value} is out of stock."
        price = self.machine.prices.get(item, 0)
        product.quantity -= 1
        change = self.machine.balance - price
        self.machine.balance = 0.0
        self.machine.selected_item = None
        self.machine.set_state(self.machine.idle_state)
        change_str = f" Change: ${change:.2f}" if change > 0 else ""
        return f"Dispensing {item.value}.{change_str} Enjoy!"

    def refund(self) -> str:
        return "Cannot refund during dispensing."


class OutOfStockState(VendingMachineState):
    def insert_coin(self, amount: float) -> str:
        self.machine.balance = amount
        return f"Inserted ${amount:.2f}, but machine is out of stock. Select refund."

    def select_item(self, item: Item) -> str:
        return "Machine is out of stock."

    def dispense(self) -> str:
        return "Machine is out of stock."

    def refund(self) -> str:
        amount = self.machine.balance
        self.machine.balance = 0.0
        self.machine.selected_item = None
        self.machine.set_state(self.machine.idle_state)
        return f"Refunded ${amount:.2f}. Sorry for the inconvenience."


@dataclass
class VendingMachine:
    inventory: dict[Item, Product] = field(default_factory=dict)
    prices: dict[Item, float] = field(default_factory=dict)
    balance: float = 0.0
    selected_item: Item | None = None

    def __post_init__(self) -> None:
        self.idle_state = IdleState(self)
        self.selecting_state = SelectingState(self)
        self.dispensing_state = DispensingState(self)
        self.out_of_stock_state = OutOfStockState(self)
        self._state: VendingMachineState = self.idle_state

    def set_state(self, state: VendingMachineState) -> None:
        self._state = state

    def add_product(self, item: Item, price: float, quantity: int) -> None:
        self.inventory[item] = Product(item, quantity)
        self.prices[item] = price

    def insert_coin(self, amount: float) -> str:
        return self._state.insert_coin(amount)

    def select_item(self, item: Item) -> str:
        return self._state.select_item(item)

    def dispense(self) -> str:
        return self._state.dispense()

    def refund(self) -> str:
        return self._state.refund()


if __name__ == "__main__":
    print("=== Vending Machine (State Pattern) ===\n")

    machine = VendingMachine()
    machine.add_product(Item.COLA, 1.50, 5)
    machine.add_product(Item.CHIPS, 1.25, 3)
    machine.add_product(Item.CANDY, 0.75, 0)
    machine.add_product(Item.WATER, 2.00, 2)
    machine.add_product(Item.CHOCOLATE, 2.50, 1)

    def act(action: str) -> None:
        print(f"  > {action}")
        print(f"  => {eval(action)}")

    act('machine.insert_coin(0.50)')
    print(f"     (State: {machine._state.__class__.__name__})")

    act('machine.select_item(Item.COLA)')
    print()

    act('machine.insert_coin(2.00)')
    act('machine.select_item(Item.COLA)')
    print()

    act('machine.select_item(Item.CHIPS)')
    print()

    act('machine.select_item(Item.CANDY)')
    print()

    print("  --- Check remaining inventory ---")
    for item, product in machine.inventory.items():
        print(f"    {item.value}: {product.quantity} left")

