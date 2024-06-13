from manstop.grid import fromCoordinates
from manstop.model import Strategy, Walker
from manstop.output import ProgressWriter

def main():
    writer = ProgressWriter()
    strategy = Strategy()
    myDude = Walker(strategy, writer)
    startNode = fromCoordinates(2, 3, writer)

    myDude.walk(startNode)


def test():
    print("this works too")
