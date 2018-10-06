# coordinator
A util library to help with scheduling of actions.

This library helps divide time into time slots, which can be divided further into more slots, etc. Actions may be scheduled to take place in a certain time slot.

## Example
```python
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
```

Output:
```
[--]    [--]    [--]                                       [b1---]                 [b2---][b3---]
[aprinting-----------------]                            [bprinting-------------------------------]
|    |    |    |    |    |    |    |    |    |    |    |    |    |    |    |    |    |    |    |    
0    3    7    10   14   17   21   24   28   31   35   38   42   45   49   52   56   59   63   66   
```
```
[2018-10-06 02:25:58.273714] a
[2018-10-06 02:26:04.275271] a
[2018-10-06 02:26:10.274867] a
[2018-10-06 02:26:40.275337] b
[2018-10-06 02:26:57.275597] b
[2018-10-06 02:27:03.275827] b

Process finished with exit code 0
```
