import math
from typing import List, Any
import colorama

class Slot:

    def __init__(self,name="",off=0.0,length=0.0):
        colorama.init()

        self.parent:Slot=None
        self.timeline:List[Slot]=[]
        self.name = name
        self.off = off # (relative) start time in seconds
        self.length = length # length in seconds

    def add(self, *slots):
        for slot in slots:
            slot.parent=self
            self.timeline.append(slot)

    def abs_off(self):
        par = self.parent
        ret = self.off
        while par is not None:
            ret+=par.off
            par=par.parent
        return ret

    def sort(self):
        self.timeline.sort(key=lambda x: x.off)

    def visualisation(self):
        self.sort()

        ret=[]
        buf=""
        prev_index=0
        for child in self.timeline:
            buf+=' '*math.floor((child.abs_off()-prev_index))

            if child.length>2:
                maxl=(math.floor(child.length)-2)
                name=(child.name+'')[:maxl]
                buf+='|'+name+('-'*(maxl-len(name)))+'|'
            else:
                buf+='|'*math.floor(child.length)

            ch_vis=child.visualisation()
            if len(ch_vis.strip())>0:
                ret.append(ch_vis)
            prev_index=child.abs_off()+child.length
        ret.append(buf)

        return '\n'.join(ret)

class Coordinator(Slot):
    def __init__(self):
        super().__init__(name="root")