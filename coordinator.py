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
        return (self.timeline[-1].off + self.timeline[-1].length) - self.timeline[0].off

    def sort(self):
        self.timeline.sort(key=lambda x: x.off)

class Coordinator(Slot):
    def __init__(self):
        super().__init__("root")

    def visualisation(self,width=30):
        """
        :param width: should be slightly less than console width
        :return:
        """
        self.sort()

        colours=['\033[' + str(x) + 'm' for x in list(range(30,37+1))] # ansi colours

        timeline=[] # (index, length)
        nameline=[] # (index, name)
        # get scale
        scale=self.get_span_length()/width

        # build model
        for i in range(width):
            for child in self.timeline:
                if i*scale <= child.off < i*scale*2:
                    timeline.append((i,math.floor(child.length*scale)))
                    nameline.append((i,child.name))

        # render
        ret1=''
        ret2=''
        for i in range(width):
            for item in timeline:
                if i==item[0]:
                    ret1+=colours[i%len(colours)]+'|'+colorama.Style.RESET_ALL
                    break
            else:
                ret1+=' '

        iterator=iter(range(width))
        for i in iterator:
            for item in nameline:
                if i==item[0]:
                    trim=len(item[1])
                    if i != len(nameline)-1:
                        trim=nameline[i+1][0]-i # (i=item[0])
                    ren=(item[1][trim:]+'..') if len(item[1])>trim+2 else item[1]
                    ret2+=ren
                    for j in range(len(ren)):
                        next(iterator) # skip iteration a bit
                    break
            else:
                ret2+=' '

        return ret1+'\n'+ret2
