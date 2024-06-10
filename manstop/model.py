class Node:
    "An intersection in the grid"

    def __init__(self, streets):
        self.streets = streets

    def __eq__(self, other):
        # shit, I don't think I should be implementing this
        pass

    def choicesAt(self, t):
        "Next steps in the form (street, trafficSignal)"
        return [(s, s.signalAt(t)) for s in self.streets]


class Walker:
    "A person walking the grid"

    def __init__(self, watch, strategy, startNode, goalNode):
        self.watch = watch
        self.strategy = strategy
        self.node = startNode
        self.goalNode = goalNode

    def walk(self):
        while self.node != self.goalNode:
            now = self.watch.checkTime()
            street = self.strategy.choose(self.node.choicesAt(now))
            self.watch.advance(street.walkTimeAt(atTime))
            self.node = street.getNextNode()

class Strategy:
    "An algo for a Walker to use at a Node"

    @staticmethod
    def choose(choices):
        "Default implementation is just take a green when you can"
        for street, signal in choices:
            if signal == "green":
                return street
            else:
                lastRed = street
        return lastRed


class Street:
    "A path to a Node"

    def __init__(self, trafficSignal, nextNode):
        self.trafficSignal = trafficSignal
        self.nextNode = nextNode

    def signalAt(self, t):
        "Whether the light is red or green"
        return self.trafficSignal.at(t)

    def walkTimeAt(self, t):
        return 100 + self.trafficSignal.timeRemaining(t)


class TrafficSignal:
    "Changes colors over time"

    def __init__(self, period, offset):
        self.period = period
        self.offset = offset
        self.redTime = period // 2

    def at(self, t):
        "What color is it now?"
        return "green" if self.timeRemaining() == 0 else "red"

    def timeRemaining(self, t):
        "Time left to the next green, or 0 if currently green"
        normalized = (t + self.offset) % self.period
        return min(self.redTime - normalized, 0)


class Watch:
    "Just a timer, I should probably use a stdlib"

    def __init__(self):
        self.now = 0

    def checkTime(self):
        return self.now

    def advance(self, amount):
        self.now += amount
