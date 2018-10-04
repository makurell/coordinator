import os
import time

from coordinator import Coordinator, Slot

# c= Coordinator()
# a= Slot("A", 0, 70)
# aa= Slot("AA", 2, 50)
# aa.add(Slot("AAa", 8, 10),
#        Slot("AAb", 20, 6))
# a.add(aa,
#       Slot("Ab", 56, 10))
# c.add(a,
#       Slot("B", 71, 4),
#       Slot("Ccccccccccc", 75, 3),
#       Slot("D", 79, 10))
#
# print(c.visualisation(width=100))

c= Coordinator()
a= Slot('scrolling', 0, 100)
# a.add(Slot('b',8,10),
#       Slot('c',20,5))

a.disperse(10,Slot('a'),Slot('b'))

c.add(a)

print(c.visualisation(width=100))