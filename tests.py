import os
import time

from coordinator import Coordinator, Slot

c=Coordinator()
a=Slot("A",0,70)
a.timeline.extend([Slot("Aa",1,50),
                   Slot("Ab",56,10)])
c.timeline.extend([a,
                   Slot("B",71,2),
                   Slot("Ccccccccccc",75,3),
                   Slot("D",79,10)])
for i in range(200):
    print(c.visualisation(width=i))
    time.sleep(0.1)