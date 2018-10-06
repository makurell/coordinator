from datetime import datetime
from coordinator import Coordinator, Slot

def test_action(name):
    print('['+str(datetime.now())+'] '+name)

c=Coordinator()
a= Slot('aprinting', 0, 20) # name, relative offset, length
b= Slot('bprinting', 40, 30)

for i in range(3):
    a.add(Slot(off=6*i,length=3,action=test_action,args=['a']))

# randomly disperse slots of equal length (5)
b.disperse(5,Slot(name='b1',action=test_action,args='b'),
           Slot(name='b2',action=test_action,args='b'),
           Slot(name='b3',action=test_action, args='b'))

c.add(a)
c.add(b)

print(c.visualisation(width=100))

c.run()