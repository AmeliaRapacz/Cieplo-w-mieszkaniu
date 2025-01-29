from funkcje import diff_matrix, f
import numpy as np
from dane import ht, hx 
from dane import density, specific_heat, radiators_power, alpha



class Room:
    def __init__(self, N, M, times, initial_temperature):
        self.N = N
        self.M = M
        self.k = times
        self.u = np.zeros((self.k, N * M))
        self.u[0, :] = np.repeat(initial_temperature, N * M)
        self.L = diff_matrix(self.N, self.M)

        self.IB1 = [i for i in range(N * M) if i % N == 0]
        self.IB2 = [i for i in range(N * M) if (i + 1) % N == 0]
        self.IB3 = [i for i in range(N * M) if i < N]
        self.IB4 = [i for i in range(N * M) if N * M - N <= i]

        self.IB1_sasiad = [i for i in range(N * M) if (i-1) % N== 0]
        self.IB2_sasiad = [i for i in range(N * M) if (i + 2) % N == 0]
        self.IB3_sasiad = [i for i in range(N * M) if N <=i < 2*N]
        self.IB4_sasiad = [i for i in range(N * M) if (M*N - 2*N) <= i < (M*N -N)]

    
        self.walls = []
        self.walls.extend(self.IB3)
        self.walls.extend(self.IB4)
        self.walls.extend(self.IB1)
        self.walls.extend(self.IB2)
        self.walls = list(set(self.walls))
        self.interior = [i for i in range(N * M) if i not in self.walls]

    
    def step(self, t, alpha = alpha): 
        self.u[t, :] = self.u[t - 1, :] + ((alpha*ht)/ hx**2) * np.matmul(self.L, self.u[t - 1, :])
        self.u[t, self.IB1] = self.u[t, self.IB1_sasiad]
        self.u[t, self.IB2] = self.u[t, self.IB2_sasiad]
        self.u[t, self.IB3] = self.u[t, self.IB3_sasiad]
        self.u[t, self.IB4] = self.u[t, self.IB4_sasiad]
    
    def average_temperature(self, t):
        return(np.sum(self.u[t, self.interior]) / ((self.N - 2) * (self.M - 2)))
        
class Window:
    def __init__(self, room, cords, outside_temperature_values):
        self.room = room
        self.cords = cords
        self.outside_temperature_values = outside_temperature_values

    def outside_temperature(self, t):
        self.room.u[t, self.cords] = self.outside_temperature_values[t]

class Heater:
    def __init__(self, room, cords, knobs, power=radiators_power): 
        self.room = room
        self.cords = cords
        self.power = power
        self.time_work = 0
        
        self.knobs_temperature = [273.15, 280.15, 285.15, 288.15, 292.15, 296.15, 301.15]  
        self.knobs =  knobs if knobs in range(len(self.knobs_temperature)) else 5
        self.max_temperature = self.knobs_temperature[self.knobs] 
        
    def termostats(self, new_mode):
        if new_mode in range(7):  
            self.knobs = new_mode 
            self.max_temperature = self.knobs_temperature[self.knobs]  

    def get_max_temperature(self):
        return self.knobs_temperature[self.knobs]
    
    def heating(self, t, ro = density, hx = hx, ht = ht, cw = specific_heat): 
        radiator_area = len(self.cords)*hx**2

        self.room.u[t, self.cords] = self.room.u[t, self.cords] + ht*f(self.power, ro, radiator_area, cw)

        self.time_work += 1
        
    def used_energy(self, ro = density, hx = hx, ht = ht, cw = specific_heat): 
        radiator_area = len(self.cords)*hx**2
        return(self.time_work*f(self.power, ro, radiator_area, cw))*radiator_area

class Door:
    def __init__(self, room_1, cords_1, room_2, cords_2):
        self.room_1 = room_1
        self.cords_1 = cords_1
        self.room_2 = room_2
        self.cords_2 = cords_2
    #temp w obrebie drzwi jest brana z pokoi, ktore te drzwi lacza i usrednianma
    def door_temperature(self, t):
        door_temperature = []
        door_temperature.append(self.room_1.u[t, self.cords_1])
        door_temperature.append(self.room_2.u[t, self.cords_2])

        door_temperature = np.mean(door_temperature)

        self.room_1.u[t, self.cords_1] = door_temperature
        self.room_2.u[t, self.cords_2] = door_temperature
