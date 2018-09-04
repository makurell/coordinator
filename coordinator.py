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
        """
        use this method instead of directly appending to timeline!
        """
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

    def get_span_length(self):
        """
        get length from first child's start to last child's end (or given length if no children)
        """
        self.sort()
        if len(self.timeline)>0:
            return (self.timeline[-1].off+self.timeline[-1].length)-self.timeline[0].off
        else:
            return self.length

    def visualisation(self,width=None,mult=None):
        self.sort()

        if mult is None:
            if width is not None:
                mult=width/self.get_span_length()
            else:
                mult=1

        ret=[]
        buf=""
        prev_index=0
        for child in self.timeline:
            buf+=' '*math.floor((child.abs_off()*mult-prev_index))

            ren_length=child.length*mult
            if ren_length>2:
                maxl=(math.floor(ren_length)-2)
                name= child.name[:maxl]
                buf+='|'+name+('-'*(maxl-len(name)))+'|'
            else:
                buf+='|'*math.floor(ren_length)

            ch_vis=child.visualisation(mult=mult)
            if len(ch_vis.strip())>0:
                ret.append(ch_vis)
            prev_index=child.abs_off()*mult+ren_length
        ret.append(buf)

        return '\n'.join(ret)

class Coordinator(Slot):
    def __init__(self):
        super().__init__(name="root")