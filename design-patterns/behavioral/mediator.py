"""
Mediator
When to use: When you want to reduce chaotic coupling between many objects that
need to communicate. The mediator centralizes external communications, keeping
participants loosely coupled.
Real-world examples: MVC architecture (Controller is the mediator), Django signals,
chat room systems, air traffic control, GUI dialog components (button/checkbox/text
communicate via dialog), event buses in microservices.
"""

from __future__ import annotations
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from enum import Enum, auto
import time


class EventType(Enum):
    TAKEOFF_REQUEST = auto()
    LANDING_REQUEST = auto()
    TAKEOFF_APPROVED = auto()
    LANDING_APPROVED = auto()
    TAKEOFF_COMPLETE = auto()
    LANDING_COMPLETE = auto()
    EMERGENCY = auto()
    POSITION_UPDATE = auto()


@dataclass
class Event:
    type: EventType
    sender: str
    data: str = ""


class Mediator(ABC):
    @abstractmethod
    def notify(self, sender: str, event: Event) -> None:
        ...


@dataclass
class Aircraft:
    callsign: str
    mediator: Mediator | None = None

    def takeoff_request(self) -> None:
        self._send(Event(EventType.TAKEOFF_REQUEST, self.callsign))

    def landing_request(self) -> None:
        self._send(Event(EventType.LANDING_REQUEST, self.callsign))

    def declare_emergency(self, reason: str) -> None:
        self._send(Event(EventType.EMERGENCY, self.callsign, reason))

    def _send(self, event: Event) -> None:
        if self.mediator:
            self.mediator.notify(self.callsign, event)

    def handle(self, event: Event) -> None:
        if event.type == EventType.TAKEOFF_APPROVED:
            print(f"  [{self.callsign}] Taking off now!")
            time.sleep(0.1)
            self._send(Event(EventType.TAKEOFF_COMPLETE, self.callsign))
        elif event.type == EventType.LANDING_APPROVED:
            print(f"  [{self.callsign}] Landing on runway {event.data}!")
            time.sleep(0.1)
            self._send(Event(EventType.LANDING_COMPLETE, self.callsign))
        elif event.type == EventType.EMERGENCY:
            print(f"  [{self.callsign}] !! EMERGENCY: {event.data} -- following protocol")
        else:
            print(f"  [{self.callsign}] Received: {event.type.name} from {event.sender}")


@dataclass
class Runway:
    identifier: str
    is_occupied: bool = False


@dataclass
class ControlTower(Mediator):
    aircraft: dict[str, Aircraft] = field(default_factory=dict)
    runways: list[Runway] = field(default_factory=list)
    _flight_log: list[str] = field(default_factory=list)

    def register_aircraft(self, *aircraft_list: Aircraft) -> None:
        for ac in aircraft_list:
            self.aircraft[ac.callsign] = ac
            ac.mediator = self

    def add_runway(self, runway: Runway) -> None:
        self.runways.append(runway)

    def _find_available_runway(self) -> Runway | None:
        for r in self.runways:
            if not r.is_occupied:
                return r
        return None

    def notify(self, sender: str, event: Event) -> None:
        entry = f"[ATC] {sender}: {event.type.name}"
        if event.data:
            entry += f" ({event.data})"
        self._flight_log.append(entry)
        print(f"  {entry}")

        if event.type == EventType.TAKEOFF_REQUEST:
            runway = self._find_available_runway()
            if runway:
                runway.is_occupied = True
                print(f"  [ATC] {sender} — cleared for takeoff on {runway.identifier}")
                self.aircraft[sender].handle(Event(EventType.TAKEOFF_APPROVED, "ATC"))
                runway.is_occupied = False
            else:
                print(f"  [ATC] {sender} — hold position, no runway available")

        elif event.type == EventType.LANDING_REQUEST:
            runway = self._find_available_runway()
            if runway:
                runway.is_occupied = True
                print(f"  [ATC] {sender} — cleared to land on {runway.identifier}")
                self.aircraft[sender].handle(
                    Event(EventType.LANDING_APPROVED, "ATC", runway.identifier)
                )
                runway.is_occupied = False
            else:
                print(f"  [ATC] {sender} — go around, no runway available")

        elif event.type in (EventType.TAKEOFF_COMPLETE, EventType.LANDING_COMPLETE):
            print(f"  [ATC] Roger {sender}, thank you.")

        elif event.type == EventType.EMERGENCY:
            print(f"  [ATC] ALL AIRCRAFT — emergency declared by {sender}")
            for callsign, ac in self.aircraft.items():
                if callsign != sender:
                    ac.handle(Event(EventType.EMERGENCY, sender, event.data))


if __name__ == "__main__":
    print("=== Air Traffic Control Mediator ===\n")

    tower = ControlTower()
    tower.add_runway(Runway("27L"))
    tower.add_runway(Runway("27R"))

    ba101 = Aircraft("BA101")
    af202 = Aircraft("AF202")
    lh303 = Aircraft("LH303")

    tower.register_aircraft(ba101, af202, lh303)

    print("  --- Landing Requests ---")
    ba101.landing_request()
    print()
    af202.landing_request()
    print()

    print("  --- Takeoff Request ---")
    lh303.takeoff_request()
    print()

    print("  --- Emergency ---")
    af202.declare_emergency("Engine fire, requesting immediate landing")
    print()

    print("\n  Flight log summary:")
    for entry in tower._flight_log:
        print(f"    {entry}")
