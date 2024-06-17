from manstop.grid import fromCoordinates
from manstop.model import Strategy, Walker
from manstop.states import create_walker, first_green

def main():
    start_node = fromCoordinates(2, 3, writer)
    walker = create_walker(start_node, first_green)

    myDude.walk(startNode)


def test():
    print("this works too")
