import os
import time

from coordinator import Coordinator, Slot

c= Coordinator()
a= Slot("A", 70, 0)
aa= Slot("AA", 50, 2)
aa.add(Slot("AAa", 10, 8),
       Slot("AAb", 6, 20))
a.add(aa,
      Slot("Ab", 10, 56))
c.add(a,
      Slot("B", 4, 71),
      Slot("Ccccccccccc", 3, 75),
      Slot("D", 10, 79))

print(c.visualisation(width=100))
