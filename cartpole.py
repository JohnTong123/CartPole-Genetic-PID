
import numpy as np
import pygame
import random
import math
import time

class CartPole:
    def __init__(self, iterations, pid = True, repeat = True):
        self.gravity = 9.8
        self.masscart = 1.0
        self.masspole = 0.1
        self.total_mass = self.masscart + self.masspole
        self.length = 0.5
        self.polemass_length = self.masspole * self.length
        self.force_mag = 10.0
        self.tau = 0.02
        self.x_threshold = 2.4
        self.theta_threshold = 0.5 * math.pi
        self.state = [[0,math.pi * ((random.random() * 0.2) - 0.1)],[0,0], [0,0], [0]] #x,theta,velo, angvelo, accel, angle accel, terminated
        # self.state = [[0,math.pi *0.1],[0,0], [0,0], [0]]
        self.screen  = None
        self.F = 0
        self.repeat= True
        self.max_iterations = iterations
        self.iterations = 0
        self.pid = pid
    def render(self):
        self.screen = pygame.display.set_mode((300 * self.x_threshold,500))
        self.screen.fill((125,125,125))
        pygame.draw.line(self.screen, (0,225,0),(360-100/2 + self.state[0][0] * 300,425),(360+100/2 + self.state[0][0] * 300,425),30)
        pygame.draw.line(self.screen, (255,225,0),(360+ self.state[0][0] * 300,425),(360+ self.state[0][0] * 300 + 300 * self.length * math.sin(self.state[0][1]),360- 300 * self.length * math.cos(self.state[0][1])),20)
        pygame.display.flip()
    def action(self, force):
        if(force > 1):
            force = 1
        if(force< -1):
            force = -1
        self.F = self.force_mag * force
    def step(self):
        if(self.screen!=None):
            start_time = pygame.time.get_ticks() 
        self.update()
        reseted = False
        if(self.state[3][0]):
            if self.repeat:
                if(self.iterations >=self.max_iterations-1):
                    self.end()
                    return [-1,-1], True                   
                self.reset()
                reseted = True
            else:
                if(self.screen!=None):
                    self.end()
                return [-1,-1], True
        if(self.screen!=None):
            end_time = pygame.time.get_ticks() 
            if(end_time-start_time < self.tau * 1000):
                temp = (self.tau * 1000)-(end_time-start_time)
                pygame.time.wait(int(temp))
            self.screen.fill((125,125,125))
            pygame.draw.line(self.screen, (0,225,0),(360-100/2 + self.state[0][0] * 300,425),(360+100/2 + self.state[0][0] * 300,425),30)
            pygame.draw.line(self.screen, (255,225,0),(360+ self.state[0][0] * 300,425),(360+ self.state[0][0] * 300 + 300 * self.length * math.sin(self.state[0][1]),425- 300 * self.length * math.cos(self.state[0][1])),20)
            pygame.display.flip()
        return self.state[0],reseted
    def update(self):
        
        sint = math.sin(self.state[0][1])
        cost = math.cos(self.state[0][1])        
        self.state[2][1] = (self.gravity * sint + cost * (-self.F - (self.masspole * self.length * (self.state[1][1]**2) * sint))/(self.total_mass))/(self.length * (4/3 -(self.masspole * cost**2)/(self.total_mass)))
        self.state[2][0] =(self.F + self.masspole * self.length * (self.state[1][1]**2 * sint - self.state[2][1] * cost))/(self.total_mass)
        self.state[1][0] += self.tau * self.state[2][0]
        self.state[1][1] += self.tau * self.state[2][1]
        self.state[0][0] += self.tau * self.state[1][0]
        self.state[0][1] += self.tau * self.state[1][1]
        while(self.state[0][1] > math.pi):
            self.state[0][1] -= 2*math.pi
        while(self.state[0][1] < -math.pi):
            self.state[0][1] +=2 * math.pi
        if(abs(self.state[0][0])>self.x_threshold):
            self.state[3][0] = 1
        if(abs(self.state[0][1])>self.theta_threshold):
            self.state[3][0] = 1 
        # https://coneural.org/florian/papers/05_cart_pole.pdf

    def reset(self):
        self.iterations+=1
        self.state[3] = False
        self.state = [[0,math.pi * ((random.random() * 0.12) - 0.06)],[0,0], [0,0], [0]] #x,theta,velo, angvelo, accel, angle accel, terminated
        # self.state = [[0,math.pi *0.1],[0,0], [0,0], [0]]
        if(self.screen!=None):
            self.screen.fill((125,125,125))
            pygame.draw.line(self.screen, (0,225,0),(360-100/2 + self.state[0][0] * 300,425),(360+100/2 + self.state[0][0] * 300,425),30)
            pygame.draw.line(self.screen, (255,225,0),(360+ self.state[0][0] * 300,425),(360+ self.state[0][0] * 300 + 300 * self.length * math.sin(self.state[0][1]),360- 300 * self.length * math.cos(self.state[0][1])),20)
            pygame.display.flip()
    def end(self):
        pygame.display.quit()


