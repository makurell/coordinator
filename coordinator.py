import math
import random
from typing import List, Any
import time

class Slot:

    def __init__(self, name="", off=0.0, length=0.0, action=None, args=None):
        if args is None:
            args = []

        self.parent:Slot=None
        self.timeline:List[Slot]=[]
        self.name = name
        self.off = off # (relative) start time in seconds
        self.length = length # length in seconds
        self.action = action
        self.args = args

    def end_off(self):
        """
        the time of the end of the currently last slot (relative to parent slot)
        """
        # last slot
        self.sort()
        if len(self.timeline)>0:
            return self.timeline[-1].off + self.timeline[-1].length
        else: return 0

    def add(self, *slots):
        """
        use this method instead of directly appending to timeline!
        """
        for slot in slots:
            slot.parent=self
            self.timeline.append(slot)

    def disperse(self, length, *slots, end_time=None, confine=False):
        """
        add and randomly disperse slots of given length into remaining available time
        :raises ValueError:
        """
        if len(slots)<=0: return
        if end_time is None: end_time=self.length

        maxl = (end_time-self.end_off())/len(slots)
        if maxl<=0 or maxl < length: raise ValueError

        if confine:
            i=0
            for slot in slots:
                slot.off=random.uniform(maxl*i,maxl*(i+1) - length)
                slot.length=length

                self.add(slot)
                i+=1
        else:
            i=0
            curoff=self.end_off()
            for slot in slots:
                nrem=((len(slots)-i-1)*length)
                slot.off=random.uniform(curoff,self.length-nrem-length)
                slot.length=length

                self.add(slot)
                curoff=slot.off+length
                i+=1

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
        if len(self.timeline)>0:
            return self.end_off() - self.timeline[0].off
        else:
            return self.length

    def run(self,precision=1):
        """
        run this slot - execute the appropriate actions at the appropriate times.
        :param precision: precision in seconds
        """
        starttime=time.time()
        if self.action is not None:
            self.action(*self.args)
        else:
            self.sort()

            queue = self.timeline
            while len(queue)>0:
                if queue[0].off<=(time.time()-starttime):
                    queue[0].run(precision=precision)
                    queue.pop(0)
                time.sleep(precision-(time.time()-starttime) % precision)

    def visualisation(self, width=None, mult=None, render_scale=True,
                      c_body='-',
                      c_fill=' ',
                      c_start='[',
                      c_end=']',
                      c_scale_fill=' ',
                      c_interval_marker='|',
                      c_pad=''):
        self.sort()

        if mult is None:
            if width is not None:
                width = max(1, width)
                mult=width/self.get_span_length() # will throw divby0 if no items
            else:
                mult=1

        ret=[]
        buf=""
        prev_index=0
        for child in self.timeline:
            buf+= c_fill * math.floor((child.abs_off() * mult - prev_index))

            ren_length=child.length*mult
            if ren_length>2:
                maxl=(math.floor(ren_length)-2)
                name= (c_pad+child.name+c_pad)[:maxl]
                buf+= c_start + name + (c_body * (maxl - len(name))) + c_end
            else:
                buf+=c_start*math.floor(ren_length)

            ch_vis=child.visualisation(mult=mult,render_scale=False)
            if len(ch_vis.strip())>0:
                ret.append(ch_vis)
            prev_index=child.abs_off()*mult+ren_length
        ret.append(buf)

        if not render_scale:
            return '\n'.join(ret)

        # get scale's interval
        key_interval = lambda x: [0.1,0.5,1,5,10][x] if x<5 else 30*2**(x-5)  # 0.1,0.5,1,5,10,30,60,120...
        i = 0
        while True:
            if key_interval(i) * mult > 3: break  # 3 = the min amount of space wanted between intervals
            i += 1
        interval = key_interval(i)

        # render scale
        maxl = math.floor(self.get_span_length() * mult)
        scale = ''
        scale_label = c_fill * maxl
        for i in range(maxl):
            if i % interval == 0:
                scale += c_interval_marker
                scale_label = scale_label[:i] + str(int(i / mult)) + scale_label[i:]
            else:
                scale += c_scale_fill

        ret.extend([scale,scale_label[:width]])
        return '\n'.join(ret)

class Coordinator(Slot):
    def __init__(self):
        super().__init__(name="root")
