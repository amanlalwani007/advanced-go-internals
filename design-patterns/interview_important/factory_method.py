"""
** Factory Method Pattern (Interview Important)
When to use:
- When a class can't anticipate the class of objects it must create
- When a class wants its subclasses to specify the objects it creates
- When you want to localize the logic of which helper class to delegate to

Real-world examples:
- Django forms: FormSet uses factory methods to create individual forms
- Celery: Task class uses factory methods to create different task types (async, sync, chord, chain)
- Django model fields: Field class hierarchy with factory-like __new__ pattern
- Python's `concurrent.futures` uses Executor subclasses (ThreadPoolExecutor, ProcessPoolExecutor)
"""

from abc import ABC, abstractmethod
from typing import Dict, Any


class Transport(ABC):
    """Product interface — all transport types must implement delivery."""

    @abstractmethod
    def calculate_cost(self, distance_km: float, weight_kg: float) -> float:
        ...

    @abstractmethod
    def estimate_delivery(self, distance_km: float) -> str:
        ...

    @abstractmethod
    def get_tracking_link(self, shipment_id: str) -> str:
        ...


class Truck(Transport):
    ROAD_SPEED_KPH = 80
    COST_PER_KM = 12.0
    COST_PER_KG = 0.5

    def calculate_cost(self, distance_km: float, weight_kg: float) -> float:
        return distance_km * self.COST_PER_KM + weight_kg * self.COST_PER_KG

    def estimate_delivery(self, distance_km: float) -> str:
        hours = distance_km / self.ROAD_SPEED_KPH
        return f"~{hours:.1f} hours by road"

    def get_tracking_link(self, shipment_id: str) -> str:
        return f"https://track.logistics.com/truck/{shipment_id}"


class Ship(Transport):
    SEA_SPEED_KNOTS = 25
    COST_PER_KM = 8.0
    COST_PER_KG = 0.2

    def calculate_cost(self, distance_km: float, weight_kg: float) -> float:
        return distance_km * self.COST_PER_KM + weight_kg * self.COST_PER_KG

    def estimate_delivery(self, distance_km: float) -> str:
        hours = distance_km / (self.SEA_SPEED_KNOTS * 1.852)
        return f"~{hours:.1f} hours by sea"

    def get_tracking_link(self, shipment_id: str) -> str:
        return f"https://track.logistics.com/ship/{shipment_id}"


class Drone(Transport):
    AIR_SPEED_KPH = 120
    COST_PER_KM = 5.0
    COST_PER_KG = 2.0
    MAX_RANGE_KM = 50
    MAX_WEIGHT_KG = 5

    def calculate_cost(self, distance_km: float, weight_kg: float) -> float:
        if distance_km > self.MAX_RANGE_KM:
            raise ValueError(f"Drone range exceeded: {distance_km}km > {self.MAX_RANGE_KM}km")
        if weight_kg > self.MAX_WEIGHT_KG:
            raise ValueError(f"Drone weight limit exceeded: {weight_kg}kg > {self.MAX_WEIGHT_KG}kg")
        return distance_km * self.COST_PER_KM + weight_kg * self.COST_PER_KG

    def estimate_delivery(self, distance_km: float) -> str:
        hours = distance_km / self.AIR_SPEED_KPH
        return f"~{hours:.1f} hours by air (drone)"

    def get_tracking_link(self, shipment_id: str) -> str:
        return f"https://track.logistics.com/drone/{shipment_id}"


class Logistics(ABC):
    """Creator — declares the factory method that returns Transport objects."""

    @abstractmethod
    def create_transport(self) -> Transport:
        ...

    def plan_shipment(
        self, shipment_id: str, distance_km: float, weight_kg: float
    ) -> Dict[str, Any]:
        transport = self.create_transport()
        return {
            "shipment_id": shipment_id,
            "transport_type": type(transport).__name__,
            "cost": transport.calculate_cost(distance_km, weight_kg),
            "estimated_delivery": transport.estimate_delivery(distance_km),
            "tracking_link": transport.get_tracking_link(shipment_id),
        }


class RoadLogistics(Logistics):
    def create_transport(self) -> Transport:
        return Truck()


class SeaLogistics(Logistics):
    def create_transport(self) -> Transport:
        return Ship()


class AirLogistics(Logistics):
    def create_transport(self) -> Transport:
        return Drone()


if __name__ == "__main__":
    logistics_map: dict[str, Logistics] = {
        "road": RoadLogistics(),
        "sea": SeaLogistics(),
        "air": AirLogistics(),
    }

    shipments = [
        ("road", "SHP-001", 1200.0, 500.0),
        ("sea", "SHP-002", 8000.0, 20000.0),
        ("air", "SHP-003", 15.0, 2.5),
    ]

    for mode, sid, dist, weight in shipments:
        result = logistics_map[mode].plan_shipment(sid, dist, weight)
        print(f"  {result['shipment_id']} ({result['transport_type']}):")
        print(f"    Cost:           ${result['cost']:.2f}")
        print(f"    ETA:            {result['estimated_delivery']}")
        print(f"    Track:          {result['tracking_link']}")
        print()

