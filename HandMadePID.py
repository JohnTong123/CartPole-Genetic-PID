from cartpole import CartPole
from pid import PID
import time
import numpy as np
import matplotlib.pyplot as plt

env = CartPole(1,True)
# env.render()
a = env.state[0]
b = False
agent = PID(15,38.5,3)
agent2 = PID(0.9,0.15,0.2)

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