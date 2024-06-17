"""
I like the stateFn approach, but let's try a big closure to share the timer.
"""

# replace with a dumb class that's just there to let the writer do something
# special at the end of the run
DONE = None

def first_green(choices):
    "Just pick the first green direction, or the last red"
    # choices is a dict of tuples like {orientation: (status, delay, street)}
    last_direction = None
    for _, direction in enumerate(choices):
        last_direction = direction
        if direction.status == "green":
            break
    return last_direction

def create_walker(initial_node, choice_fn, writer):
    "Wire everything up together"
    now = 0                     # still should use stdlib

    def node_state_fn(node):
        writer.visit(node)
        def inner():
            if (choices := node.traffic_signal_at(now)):
                return choice_state_fn(choices)
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
