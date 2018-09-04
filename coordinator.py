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

    def visualisation(self,width=None,mult=None,render_scale=True):
        # get visualisation
        if mult is None:
            if width is not None:
                width = max(1, width)
                mult=width/self.get_span_length()
            else:
                mult=1
        ret=super(Coordinator,self).visualisation(width=width,mult=mult)

        if not render_scale:
            return ret

        # get scale's interval
        key_interval = lambda x: [0.1, 0.5, 1, 5, 10][x] if x < 5 else 30 * 2 ** (x - 5)  # 0.1,0.5,1,5,10,30,60,120...
        i = 0
        while True:
            if key_interval(i)*mult>3: break # 3 = the min amount of space wanted between intervals
            i+=1
        interval=key_interval(i)

        # render scale
        maxl=math.floor(self.get_span_length()*mult)
        scale=''
        scale_label=' '*maxl
        for i in range(maxl):
            if i % interval==0:
                scale+='|'
                scale_label=scale_label[:i]+str(int(i/mult))+scale_label[i:]
            else:
                scale+=' '
        return ret+'\n'+scale[:width]+'\n'+scale_label[:width]