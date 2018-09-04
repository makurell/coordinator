import os
import time

from coordinator import Coordinator, Slot

c=Coordinator()
a=Slot("A", 0, 70)
aa=Slot("AA", 2, 50)
aa.add(Slot("AAa", 8, 10),
       Slot("AAb", 20, 6))
a.add(aa,
      Slot("Ab", 56, 10))
c.add(a,
      Slot("B", 71, 2),
      Slot("Ccccccccccc", 75, 3),
      Slot("D", 79, 10))

print(c.visualisation())
