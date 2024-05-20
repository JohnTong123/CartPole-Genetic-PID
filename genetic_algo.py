import numpy as np
from pid import PID
from cartpole import CartPole
import random
class Genetic_Algorithm:
    def __init__(self, population, tournament_size):
        self.population = population
        self.num_clones = population//10
        self.tournament_size = tournament_size
        self.mutation_rate = 0.8
        self.cross_over = 3
        self.tournament_wr = 0.5
        self.pid_values = (30*np.random.random(size =(population, 7))).tolist()
        for i in range(self.population):
            self.pid_values[i][6] = 0
    def run(self,steps):
        step_count = 0 
        f = open("demofile2.txt", "w")
        
        while(step_count<steps):
            timestep = 0 
            for i in range(self.population):
                self.pid_values[i][6] = 0
            env = CartPole(self.population,True)
            pid_count = 0 
            a = env.state[0]
            # env.render()
            b = False
            
            agent = PID(self.pid_values[pid_count][0],self.pid_values[pid_count][1],self.pid_values[pid_count][2])
            agent2 = PID(self.pid_values[pid_count][3],self.pid_values[pid_count][4],self.pid_values[pid_count][5])
            while(not env.state[3][0]):
                first = -1*agent.update(a[1])
                second = -agent2.update(a[0])
                if(abs(a[1]) <0.01):
                    self.pid_values[pid_count][6]+=(1-100*abs(a[1]))
                if(abs(a[0])<0.05):
                    self.pid_values[pid_count][6]+=(0.5-10*abs(a[0]))
                select  = 0 
                timestep+=1
                if(abs(first)>abs(second)):
                    select = first
                else:
                    select = second
                env.action(select)
                a, b = env.step()
                if (b or timestep ==5000):
                    # print("Episode #", step_count)
                    # print(" Angle PID Val: Kp ", self.pid_values[pid_count][0],", Ki ", self.pid_values[pid_count][1], ", Kd ",self.pid_values[pid_count][2])
                    # print((". X PID Val: Kp ", self.pid_values[pid_count][3],", Ki ", self.pid_values[pid_count][4], ", Kd ",self.pid_values[pid_count][5]))
                    # print(self.pid_values[pid_count][6])
                    timestep = 0 
                    pid_count+=1
                    if(pid_count >= self.population):
                        break
                    agent = PID(self.pid_values[pid_count][0],self.pid_values[pid_count][1],self.pid_values[pid_count][2])
                    agent2 = PID(self.pid_values[pid_count][3],self.pid_values[pid_count][4],self.pid_values[pid_count][5]) 
                    agent.reset()
                    agent2.reset()
                    env.reset()
                    # print(env.state[0])
            self.pid_values.sort(key=lambda x:x[6],reverse=True)
            print("Episode #", step_count)
            print(" Angle PID Val: Kp ", self.pid_values[0][0],", Ki ", self.pid_values[0][1], ", Kd ",self.pid_values[0][2])
            print((". X PID Val: Kp ", self.pid_values[0][3],", Ki ", self.pid_values[0][4], ", Kd ",self.pid_values[0][5]))
            print(self.pid_values[0][6])
            f.write("Episode #")
            f.write(str(step_count))
            f.write(" Angle PID Val: Kp ")
            f.write(str(self.pid_values[0][0]))
            f.write(", Ki ") 
            f.write(str(self.pid_values[0][1]))
            f.write(", Kd ")
            f.write(str(self.pid_values[0][2]))
            f.write(". X PID Val: Kp ")
            f.write(str(self.pid_values[0][3]))
            f.write(", Ki ")
            f.write(str(self.pid_values[0][4]))
            f.write(", Kd ")
            f.write(str(self.pid_values[0][5]))
            f.write("\n")
            self.tournament()
            step_count+=1
            
        f.close()
        f = open("output.txt", "w")
        for i in range(self.population):
            f.write(str(self.pid_values[i]))
            f.write('\n')
        f.close()
    def tournament(self):   
        temp = (np.zeros([self.population,7])).tolist()
        print(len(temp))
        for i in range(self.num_clones):
            temp[i] = self.pid_values[i].copy()
        for i in range(self.num_clones,self.population):
            # temp[i] = self.pid_values[i]
            pid_copy = self.pid_values.copy()
            tournament1=[]
            tournament2=[]
            combotourney= random.sample(pid_copy,2*self.tournament_size)
            for j in range(2*self.tournament_size):
                if(j%2==0):
                    tournament1.append(combotourney[j].copy())
                else:
                    tournament2.append(combotourney[j].copy())
            # print(tournament1)
            # print(tournament2)
            # np.sort(tournament1, key=lambda x:x[6],reverse=True)
            tournament1.sort(key=lambda x:x[6],reverse=True)
            tournament2.sort(key=lambda x:x[6],reverse=True)
            parent1 = (np.zeros(7)).tolist()
            parent2 = (np.zeros(7)).tolist()
            try:
                track = 0 
                for j in range(self.tournament_size):
                    track = j
                    if(random.random()<self.tournament_wr):
                        parent1 = tournament1[j].copy()
                        break
                    if(j == self.tournament_size-1):
                        parent1=tournament1[j]
                for j in range(self.tournament_size):
                    track = j
                    if(random.random()<self.tournament_wr):
                        parent2 = tournament2[j].copy()
                        break
                    if(j == self.tournament_size-1):
                        parent2=tournament2[j]
            except:
                print("RAAA")
                print(j)
                print(len(tournament1))
                print(len(tournament2))
                print(len(combotourney))
                quit()
            # print(parent1)
            # print(parent2)
            indices = [0,1,2,3,4,5]
            f1 = random.sample(indices.copy(), self.cross_over)
            for j in range(len(f1)):
                parent1[f1[j]] = parent2[f1[j]]
            if(random.random()<self.mutation_rate):
                index = random.randint(0,5)
                parent1[index] = max(0,parent1[index] + 2*random.random()-1)
            temp[i] = parent1
        self.pid_values=temp
