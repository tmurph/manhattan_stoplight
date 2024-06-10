from abc import ABC, abstractmethod
from random import randrange

class Node:
    "An intersection in the grid"

    def __init__(self, trafficSignalFactory):
        self.trafficSignalFactory = trafficSignalFactory
        self.streets = []

    def addStreet(self, street):
        self.streets.append(street)

    def addStreets(self, streets):
        self.streets.extend(streets)

    def accept(self, walker):
        walker.setStreets(self.streets)
        walker.setTrafficSignalFactory(self.trafficSignalFactory)

class Walker:
    "A person walking the grid"

    def __init__(self, strategy, startNode):
        self.now = 0          # should use stdlib
        self.strategy = strategy
        self.streets = []
        self.trafficSignalFactory = None
        startNode.accept(self)

    def setStreets(self, streets):
        self.streets = streets

    def setTrafficSignalFactory(self, trafficSignalFactory):
        self.trafficSignalFactory = trafficSignalFactory

    def cross(self, street, trafficSignal):
        "How much time it takes the WALKER to cross"
        self.now += street.getWalkTime()
        self.now += trafficSignal.getDelay(street.getOrientation())

    def waitFor(self, waitTime):
        self.now += waitTime

    def walk(self):
        if self.streets:
            trafficSignal = self.trafficSignalFactory.createAt(self.now)
            street = self.strategy.choose(self.streets, trafficSignal)
            self.cross(street, trafficSignal)
            street.accept(self)

class Strategy:
    "An algo for a Walker to use at a Node"

    @staticmethod
    def choose(streets, trafficSignal):
        "Default implementation is just take a green when you can"
        for street in streets:
            signal = trafficSignal.getStatus(street.getOrientation())
            if signal == "green":
                return street
            else:
                lastRed = street
        return lastRed


class Street:
    "A path to a Node"

    def __init__(self, orientation, walkTime, nextNode):
        self.orientation = orientation
        self.walkTime = walkTime
        self.nextNode = nextNode

    def getWalkTime(self):
        return self.walkTime

    def getOrientation(self):
        "NESW"
        return self.orientation

    def accept(self, walker):
        self.nextNode.accept(walker)


class TrafficSignal:
    """Changes colors over time.

    halfPeriod: amount of time between light changes
    offset: where in the cycle the light begins (0 == begin at the start of the red light)
    checkTime: the current time we're checking the signal
"""

    def __init__(self, halfPeriod, offset, checkTime):
        # Save the time left to the next green, or 0 if already green
        normalized = (checkTime + offset) % (halfPeriod * 2)
        if normalized < halfPeriod:
            self.status = {"N": "red", "E": "green"}
            self.delay = {"N": halfPeriod - normalized, "E": 0}
        else:
            self.status = {"N": "green", "E": "red"}
            self.delay = {"N": 0, "E": 2 * halfPeriod - normalized}

    def getStatus(self, orientation):
        "What color is it now, looking towards ORIENTATION?"
        return self.status[orientation]

    def getDelay(self, orientation):
        "How long to hold up WALKER before they head towards ORIENTATION"
        return self.delay[orientation]


class TrafficSignalFactory(ABC):
    "Control how the traffic signals interact"

    @abstractmethod
    def createAt(self, t):
        pass


class FixedSignalFactory(TrafficSignalFactory):
    "Return traffic lights that share a common period and offset"

    def __init__(self, halfPeriod, offset):
        self.halfPeriod = halfPeriod
        self.offset = offset

    def createAt(self, t):
        return TrafficSignal(self.halfPeriod, self.offset, t)


class RandomSignalFactory(TrafficSignalFactory):
    "Return traffic lights with a common period but random offset"

    def __init__(self, halfPeriod):
        self.halfPeriod = halfPeriod

    def createAt(self, t):
        return TrafficSignal(self.halfPeriod, randrange(2 * self.halfPeriod), t)
