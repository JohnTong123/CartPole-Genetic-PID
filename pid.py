import math

class PID:

    def __init__(self, kp, ki, kd):
        self.ki = ki
        self.kp = kp
        self.kd = kd
        self.force_mag = 1.0
        self.accumulated_error = 0 
        self.last_error= 0 
        self.tau = 0.02

    def update(self, value):
        error = 0 - value
        self.accumulated_error += (self.last_error + error) * 0.5 * self.tau#(self.last_error * self.tau) + self.tau * (error - self.last_error) * 0.5
        output = self.kp * error + self.accumulated_error * self.ki + (error-self.last_error) * self.kd/self.tau
        # output = 
        self.last_error = error
        # print(output)
        return output

    def reset(self):
        self.accumulated_error = 0 
        self.last_error = 0 
