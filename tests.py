import os
import time
from datetime import datetime

from coordinator import Coordinator, Slot

def test_action(name):
    print('['+str(datetime.now())+'] '+name)

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
a= Slot('aprinting', 0, 20)
b= Slot('bprinting', 40, 30)
# a.add(Slot('b',8,10),
#       Slot('c',20,5))

for i in range(3):
    a.add(Slot(off=6*i,length=1,action=test_action,args=['a']))

b.disperse(2,Slot(action=test_action,args='b'),
           Slot(action=test_action,args='b'),
           Slot(action=test_action,args='b'),
           Slot(action=test_action,args='b'),
           Slot(action=test_action,args='b'),
           Slot(action=test_action,args='b'))

c.add(a)
c.add(b)

print(c.visualisation(width=100))

c.run()