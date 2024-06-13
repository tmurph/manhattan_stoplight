"""
I like the stateFn approach, but let's try a big closure to share the timer.
"""

# replace with a dumb class that's just there to let the writer do something
# special at the end of the run
DONE = None

def first_green(traffic_signal):
    "Just pick the first green direction, or the last red"
    # directions are maybe a tuple like (orientation, status, delay, street)
    last_direction = None
    for direction in traffic_signal:
        last_direction = direction
        if direction.status == "green":
            break
    return last_direction

def create_walker(initial_node, choice_fn):
    "Wire everything up together"
    now = 0                     # still should use stdlib

    def node_state_fn(node):
        writer.visit(node)
        def inner():
            traffic_signal = node.trafficSignalFactory.createAt(now)
            if traffic_signal.streets:
                return choice_state_fn(traffic_signal)
            else:
                return done_state_fn()
        return inner

    def choice_state_fn(traffic_signal):
        writer.visit(traffic_signal)
        def inner():
            chosen_direction = choice_fn(traffic_signal)
            return direction_state_fn(chosen_direction)
        return inner

    def direction_state_fn(direction):
        writer.visit(direction)
        def inner():
            now += direction.delay
            return walk_state_fn(direction.street)
        return inner

    def walk_state_fn(street):
        writer.visit(street)
        def inner():
            now += street.walk_time
            return node_state_fn(street.next_node)
        return inner

    def done_state_fn():
        writer.visit(DONE)
        return None

    def inner():
        state_fn = node_state_fn(initial_node)
        while state_fn:
            state_fn = state_fn()

    return inner
