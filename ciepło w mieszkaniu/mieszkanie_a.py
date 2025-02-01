from elementy_mieszkania import Door, Window, Room, Heater
import matplotlib.pyplot as plt
import numpy as np
from dane import hx, ht
from funkcje import f

class House:
    def __init__(self, initial_temperature, outside_temperature, times, knobs):
        self.initial_temperature = initial_temperature
        self.times = times
        self.outside_temperature = outside_temperature

        
        room1 = Room(21, 9, times, initial_temperature)  # Lewy górny
        room2 = Room(13, 11, times, initial_temperature) # Lewy dolny
        room3 = Room(11, 9, times, initial_temperature)  # Prawy górny
        room4 = Room(19, 11, times, initial_temperature) # Prawy dolny

        self.rooms = [room1, room2, room3, room4]

        
        self.windows = [
            Window(room1, [2,3,4,5], outside_temperature),
            Window(room2, [134,135], outside_temperature),
            Window(room2, [78,91], outside_temperature),
            Window(room3, [32,43,54,65], outside_temperature),
            Window(room4, [112,131], outside_temperature),
            Window(room4, [197,198,199,200], outside_temperature)
        ]

        # Definicja grzejników (usunięto `base_max_temperature`)
        self.heaters = [
            Heater(room1, [34, 35], knobs),
            Heater(room2, [121,122], knobs),
            Heater(room2, [53,66], knobs),
            Heater(room3, [53,64], knobs),
            Heater(room4, [112,131,169,188], knobs),
            Heater(room4, [178,179], knobs)
        ]

        
        self.doors = [
            Door(room1, [171,172], room2, [3,4]),
            Door(room1, [104,125], room3, [44,45]),
            Door(room1, [184,185], room4, [3,4])
        ]
    
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
        used_all_energy = []
        time_in_hours = 0

        for t in np.arange(1, self.times):
            # Aktualizacja temperatur w pokojach
            for room in self.rooms:
                room.step(t)

            # Aktualizacja temperatur w oknach
            for window in self.windows:
                window.outside_temperature(t)

            used_all_energy_at_time = []
            for heater in self.heaters:
                if heater.room.average_temperature(t) < heater.get_max_temperature():
                    heater.heating(t)

                used_all_energy_at_time.append(heater.used_energy())
            used_all_energy.append(np.sum(used_all_energy_at_time))

            
            for door in self.doors:
                door.door_temperature(t)

            time_in_hours = t * ht / 3600

            if t % 900 == 0 and t <= 7200:  
                house_matrix = self.create_house_matrix(t)
                plt.figure(figsize=(8, 6))
                im = plt.imshow(house_matrix, cmap="plasma", vmin=275.15, vmax=300.15)
                cbar = plt.colorbar(im, label='Temperature (°C / K)')

                def kelvin_to_celsius(kelvin):
                    return kelvin - 273.15

                # Ustawienie podziałek na kolorowej belce (Kelwiny i Celsjusze)
                tick_values = np.linspace(275.15, 300.15, 6)  # 6 równych podziałek
                cbar.set_ticks(tick_values)
                cbar.set_ticklabels([f"{kelvin_to_celsius(k):.1f}°C / {k:.1f}K" for k in tick_values])
                plt.title(f"Temperatura po {int(t/(900))}/8 godziny grzania")
                plt.show()
                plt.savefig(f"temperature_po_godzinie{t/(900)}_grzania.png") 
                plt.close()
                    
        
        plt.figure(figsize=(10, 6))
        time_in_hours = np.arange(len(used_all_energy)) * ht / 3600  
        plt.plot(time_in_hours, used_all_energy, label="Zużycie energii", color="blue")
        plt.xlabel("Czas [godziny]")
        plt.ylabel("Zużycie energii [J]")
        plt.title("Wykres zużycia energii w czasie")
        plt.grid(True)
        plt.legend()
        plt.ylim(min(used_all_energy) * 0.9, max(used_all_energy) * 1.1)
        plt.show()
        print(used_all_energy[-1])
