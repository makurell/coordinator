import math
from typing import List, Any
import colorama

class Slot:

    def __init__(self,name="",off=0.0,length=0.0):
        colorama.init()

        self.timeline:List[Slot]=[]
        self.name = name
        self.off = off # (relative) start time in seconds
        self.length = length # length in seconds

    def get_span_length(self):
        """
        get length from start child to end of end child
        """
        self.sort()
        if len(self.timeline)>0:
            return (self.timeline[-1].off + self.timeline[-1].length) - self.timeline[0].off
        else:
            return self.length

    def sort(self):
        self.timeline.sort(key=lambda x: x.off)

    def visualisation(self):
        self.sort()

        ret=[]

        buf=""
        prev_index=0
        for child in self.timeline:
            buf+=' '*math.floor((child.off-prev_index))

            if child.length>2:
                maxl=(math.floor(child.length)-2)
                name=(child.name+' ')[:maxl]
                buf+='|'+name+('x'*(maxl-len(name)))+'|'
            else:
                buf+='|'*math.floor(child.length)

            ch_vis=child.visualisation()
            if len(ch_vis.strip())>0:
                ret.append(ch_vis)
            prev_index=child.off+child.length
        ret.append(buf)

        return '\n'.join(ret)

class Coordinator(Slot):
    def __init__(self):
        super().__init__("root")