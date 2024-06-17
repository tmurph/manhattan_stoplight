from manstop.model import Node, Street, FixedSignalFactory

def fromFile(f):
    "Something that can parse a file would be nice"

def fromCoordinates(x, y, writer):
    "Wire up a default grid sized X streets by Y streets"
    default_walktime = 100
    default_lighttime = 130

    traffic_signal_factory = FixedSignalFactory(default_lighttime, 0)

    all_nodes = [[Node(traffic_signal_factory, f"({i}, {j})", writer) for j in range(y)] for i in range(x)]
    for i in range(x):
        for j in range(y):
            if i + 1 < x:
                next_node_x = all_nodes[i + 1][j]
                next_street_x = Street("E", default_walktime, next_node_x, f"({i}, {j}, E)")
                all_nodes[i][j].addStreet(next_street_x)
            if j + 1 < y:
                next_node_y = all_nodes[i][j + 1]
                next_street_y = Street("N", default_walktime, next_node_y, f"({i}, {j}, N)")
                all_nodes[i][j].addStreet(next_street_y)

    return all_nodes[0][0]

def from_coordinates(x, y):
    "Wire up a default grid sized X streets by Y streets"
    default_walktime = 100
    default_lighttime = 130

    traffic_signal_factory = FixedSignalFactory(default_lighttime, 0)

    all_nodes = [[Node(traffic_signal_factory, f"({i}, {j})", writer) for j in range(y)] for i in range(x)]
    for i in range(x):
        for j in range(y):
            if i + 1 < x:
                next_node_x = all_nodes[i + 1][j]
                next_street_x = Street("E", default_walktime, next_node_x, f"({i}, {j}, E)")
                all_nodes[i][j].addStreet(next_street_x)
            if j + 1 < y:
                next_node_y = all_nodes[i][j + 1]
                next_street_y = Street("N", default_walktime, next_node_y, f"({i}, {j}, N)")
                all_nodes[i][j].addStreet(next_street_y)

    return all_nodes[0][0]
