from cartpole import CartPole
from pid import PID
import time
import numpy as np
import matplotlib.pyplot as plt

env = CartPole(1,True)
env.render()
a = env.state[0]
b = False
agent = PID(31.332939589122248,4.397045679363643,12.95031779661186)
agent2 = PID(9.280049216318023,1.101632441913221,12.9004768148372)

step = 0
ypoints = np.zeros(1000)
y2points = np.zeros(1000)
while(not env.state[3][0]):
    first = -1*agent.update(a[1])
    second = -agent2.update(a[0])
    select  = 0 
    if(abs(first)>abs(second)):
        select = first
    else:
        select = second
    env.action(select)
    a, b = env.step()
    ypoints[step] = a[1]
    y2points[step] = a[0]
    step+=1
    if b:
        agent.reset()
    if(step==1000):
        break
env.end()
xpoints = np.array([i*0.02 for i in range(0,1000)])

plt.plot(xpoints, ypoints)
plt.show()
plt.plot(xpoints, y2points)
plt.show()
plt.close()