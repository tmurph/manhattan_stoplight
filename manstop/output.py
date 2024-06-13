class ProgressWriter:
    "should just do the printf debugging I'm doing now"

    def __init__(self):

    def crossing(self, orientation, trafficSignal):
        print(f"heading {orientation}")
        print(f"the signal is {trafficSignal.getStatus(orientation)}")
        print(f"crossed, now it is {self.now}")

    def choosingAt(self, time):
        print(f"wondering where to go at {time}")

    def doneAt(self, time):
        print(f"done!  it is now {time}")

    def reachedNode(self, name):
        print(f"reached Node {name}")

    def reachedStreet(self, name):
        print(f"reached Street {name}")
