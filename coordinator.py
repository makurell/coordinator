from typing import List, Any
import colorama

class Slot:

    def __init__(self):
        self.timeline:List[Slot]=[]
        self.name = ""
        self.off = 0.0 # (relative) start time in seconds
        self.length = 0.0 # length in seconds

    def get_span_length(self):
        """
        get length from start child to end of end child
        """
        self.sort()
        return (self.timeline[-1].off + self.timeline[-1].length) - self.timeline[0].off

    def sort(self):
        self.timeline.sort(key=lambda x: x.off)

class Coordinator(Slot):
    def __init__(self):
        super().__init__()

        # overriding
        self.name="root"
        self.off=None
        self.length=None

    def visualisation(self,width=30):
        timeline=[]
        # get scale
        step=self.get_span_length()/width
        pass