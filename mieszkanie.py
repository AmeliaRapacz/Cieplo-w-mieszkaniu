from elementy_mieszkania import Door, Window, Room, Heater
import matplotlib.pyplot as plt
import numpy as np
from dane import hx,ht
from funkcje import f


class House:
    def __init__(self, initial_temperature, outside_temperature, max_temperature, times):

        self.initial_temperature = initial_temperature
        self.times = times
        self.outside_temperature = outside_temperature


        room1 = Room(21, 9, times, initial_temperature) # lewy górny okk
        room2 = Room(13, 11, times, initial_temperature) #lewy dolny
        room3 = Room(11, 9, times, initial_temperature) #prawy górny
        room4 = Room(19, 11, times, initial_temperature) #prawy dolny


        self.rooms = [room1, room2, room3, room4]

        window1=Window(room1, [2,3,4,5], outside_temperature)
        window2=Window(room2, [134,135],  outside_temperature)
        window3=Window(room2, [78,91],  outside_temperature)
        window4=Window(room3, [32,43,54,65],  outside_temperature)
        window5=Window(room4, [112,131],  outside_temperature)
        window6=Window(room4, [197,198,199,200],  outside_temperature)

        self.windows = [window1, window2, window3, window4,window5, window6]

        heater1=Heater(room1, [34, 35], max_temperature)
        heater2=Heater(room2, [121,122], max_temperature)
        heater3=Heater(room2, [53,66], max_temperature)
        heater4=Heater(room3, [53,64], max_temperature)
        heater5=Heater(room4, [112,131,169, 188], max_temperature)
        heater6=Heater(room4, [178,179], max_temperature)

        self.heaters = [heater1, heater2, heater3, heater4, heater5, heater6]

        door1=Door(room1,[171,172], room2,[3,4])
        door2=Door(room1,[104,125], room3,[44,45])
        door3=Door(room1,[184,185], room4,[3,4])

        self.doors = [door1, door2, door3]
    

    def create_house_matrix(self, t):
        house_matrix = np.zeros((self.rooms[0].M + self.rooms[1].M, self.rooms[0].N + self.rooms[2].N))

        room1_matrix = self.rooms[0].u[t, :].reshape(self.rooms[0].M, self.rooms[0].N) 
        room2_matrix = self.rooms[1].u[t, :].reshape(self.rooms[1].M, self.rooms[1].N)
        room3_matrix = self.rooms[2].u[t, :].reshape(self.rooms[2].M, self.rooms[2].N)
        room4_matrix = self.rooms[3].u[t, :].reshape(self.rooms[3].M, self.rooms[3].N)

        house_matrix[0:self.rooms[0].M, 0:self.rooms[0].N] = room1_matrix
        house_matrix[self.rooms[0].M:, 0:self.rooms[1].N] = room2_matrix
        house_matrix[0:self.rooms[2].M, self.rooms[0].N:] = room3_matrix
        house_matrix[self.rooms[2].M:, self.rooms[1].N:] = room4_matrix

        return house_matrix
    
    def main(self):
        # Wykorzystana energia, potrzebne później!
        used_all_energy = []
        for t in np.arange(1, self.times):   
            for room in self.rooms:
                room.step(t)

            for window in self.windows:
                window.outside_temperature(t)

            used_all_energy_at_time = []
            for heater in self.heaters:
                if heater.room.average_temperature(t) < heater.max_temperature:
                    heater.heating(t)
                used_all_energy_at_time.append(heater.used_energy())
            used_all_energy.append(np.sum(used_all_energy_at_time))
            
            for door in self.doors:
                door.door_temperature(t)
            
            # Rysowanie rozkładu temperatury w domu
            if t % 7200 == 0 or t == self.times - 1:  # Co 7200 kroków lub na końcu
                house_matrix = self.create_house_matrix(t)
                plt.figure(figsize=(8, 6))
                plt.imshow(house_matrix, cmap="plasma")
                plt.colorbar(label='Temperature')
                plt.title(f"Temperatura o godzinie: {t/(60*60*2)-1}")
                plt.show()
                plt.savefig(f"temperature_o_godzinie{t/(60*60*2)-1}.png") 
                plt.close()
                    
        # Wykres zużycia energii
        plt.figure(figsize=(10, 6))
        time_in_hours = np.arange(len(used_all_energy)) * ht / 3600  # Przeliczenie czasu na godziny
        plt.plot(time_in_hours, used_all_energy, label="Zużycie energii", color="blue")
        plt.xlabel("Czas [godziny]")
        plt.ylabel("Zużycie energii [J]")
        plt.title("Wykres zużycia energii w czasie")
        plt.grid(True)
        plt.legend()
        plt.ylim(min(used_all_energy) * 0.9, max(used_all_energy) * 1.1)
        plt.show()
    
