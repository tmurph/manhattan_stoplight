from abc import ABC, abstractmethod
from dataclasses import dataclass
from random import randrange

@dataclass
class Node:
    "An intersection in the grid"
    name: str
    traffic_signal_factory: TrafficSignalFactory

    def traffic_signal_at(self, time):
        return self.traffic_signal_factory.create_at(time)


@dataclass
class Direction:
    "A static container for a path to take from a traffic signal."
    status: str
    delay: int
    street: Street


@dataclass
class Street:
    "A path to a Node"
    name: str
    walk_time: float
    next_node: Node


class TrafficSignalFactory(ABC):
    "Control how the traffic signals interact"

    @abstractmethod
    def create_at(self, time):
        pass

    @abstractmethod
    def add_street(self, street):
        pass

class FixedSignalFactory(TrafficSignalFactory):
    "Return traffic lights that share a common period and offset"

    def __init__(self, half_period, offset):
        self.half_period = half_period
        self.offset = offset

    def create_at(self, time):
        return TrafficSignal(self.half_period, self.offset, time)


class RandomSignalFactory(TrafficSignalFactory):
    "Return traffic lights with a common period but random offset"

    def __init__(self, half_period):
        self.half_period = half_period

    def create_at(self, time):
        return TrafficSignal(self.half_period, randrange(2 * self.half_period), time)


class TrafficSignal:
    """Factory for a crossing state at a point in time.

    half_period: amount of time between light changes
    offset: where in the cycle the light begins (0 == begin at the start of the red light)
"""

    def __init__(self, half_period, offset, streets):
        self._half_period = half_period
        self._offset = offset
        self._streets = streets

    def checkAt(self, time):
        "What choices are we looking at?"
        normalized = (time + self._offset) % (self._half_period * 2)
        print(f"we're at {normalized} in the traffic light cycle")
        if normalized < self._half_period:
            return {"N": Direction("red", self._half_period - normalized, self._streets["N"]),
                    "E": Direction("green", 0, self._streets["E"])}
        else:
            return {"N": Direction("green", 0, self._streets["N"]),
                    "E": Direction("red", 2 * self._half_period - normalized, self._streets["E"])}
