from abc import ABC, abstractmethod
from random import randrange

class Node:
    "An intersection in the grid"

    def __init__(self, trafficSignalFactory, name, writer):
        self.trafficSignalFactory = trafficSignalFactory
        self.name = name
        self.streets = []

    def addStreet(self, street):
        self.streets.append(street)

    def addStreets(self, streets):
        self.streets.extend(streets)

    def accept(self, walker):
        self.writer.reachedNode(self.name)
        walker.choose(self.streets, self.trafficSignalFactory)

class Walker:
    "A person walking the grid"

    def __init__(self, writer):
        self.now = 0          # should use stdlib
        self.writer = writer

    def choose(self, streets, trafficSignalFactory):
        self.writer.choosingAt(self.now)
        if streets:
            trafficSignal = trafficSignalFactory.createAt(self.now)
            foundStreet = None
            for street in streets:
                foundStreet = street
                signal = trafficSignal.getStatus(street.getOrientation())
                if signal == "green":
                    break
            street.accept(self, trafficSignal)
        else:
            self.writer.doneAt(self.now)

    def walk(self, startNode):
        startNode.accept(self)


class Street:
    "A path to a Node"

    def __init__(self, orientation, walkTime, nextNode, name, writer):
        self.orientation = orientation
        self.walkTime = walkTime
        self.nextNode = nextNode
        self.name = name
        self.writer = writer

    def getOrientation(self):
        "NESW"
        return self.orientation

    def accept(self, walker, trafficSignal):
        self.writer.reachedStreet(self.name)
        self.writer.crossing(self.orientation, trafficSignal)
        walker.advance(self.walkTime)
        walker.advance(trafficSignal.getDelay(self.orientation))
        self.nextNode.accept(walker)


class TrafficSignal:
    """Changes colors over time.

    halfPeriod: amount of time between light changes
    offset: where in the cycle the light begins (0 == begin at the start of the red light)
    checkTime: the current time we're checking the signal
"""

    def __init__(self, halfPeriod, offset, checkTime):
        normalized = (checkTime + offset) % (halfPeriod * 2)
        print(f"we're at {normalized} in the traffic light cycle")
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
