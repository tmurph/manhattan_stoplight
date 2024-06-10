class Node:
    "An intersection in the grid"

    def __init__(self, streets):
        self.streets = streets

    def accept(self, walker):
        walker.setChoices(self.streets)


class Walker:
    "A person walking the grid"

    def __init__(self, strategy, startNode):
        self.now = 0          # should use stdlib
        self.strategy = strategy
        self.choices = []
        startNode.accept(self)

    def walkTo(self, nextNode, walkTime):
        self.now += walkTime
        nextNode.accept(self)

    def setChoices(self, choices):
        self.choices = choices

    def walk(self):
        if self.choices:
            street = self.strategy.choose(self.choices, self.now)
            street.acceptAt(self, self.now)

class Strategy:
    "An algo for a Walker to use at a Node"

    @staticmethod
    def choose(choices, t):
        "Default implementation is just take a green when you can"
        for street in choices:
            signal = street.getTrafficSignal.at(t)
            if signal == "green":
                return street
            else:
                lastRed = street
        return lastRed


class Street:
    "A path to a Node"

    def __init__(self, trafficSignal, nextNode):
        self.walkTime = 100
        self.trafficSignal = trafficSignal
        self.nextNode = nextNode

    def getTrafficSignal(self):
        return self.trafficSignal

    def acceptAt(self, walker, time):
        totalTime = self.walkTime + self.trafficSignal.timeRemainingAt(time)
        walker.walkTo(self.nextNode, totalTime)


class TrafficSignal:
    "Changes colors over time"

    def __init__(self, period, offset):
        self.period = period
        self.offset = offset
        self.redTime = period // 2

    def at(self, t):
        "What color is it now?"
        return "green" if self.timeRemainingAt(t) == 0 else "red"

    def timeRemainingAt(self, t):
        "Time left to the next green, or 0 if currently green"
        normalized = (t + self.offset) % self.period
        return min(self.redTime - normalized, 0)
