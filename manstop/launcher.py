from manstop.grid import fromCoordinates
from manstop.model import Strategy, Walker

def main():
    startNode = fromCoordinates(2, 3)
    strategy = Strategy()
    myDude = Walker(strategy, startNode)
    myDude.walk()


def test():
    print("this works too")
