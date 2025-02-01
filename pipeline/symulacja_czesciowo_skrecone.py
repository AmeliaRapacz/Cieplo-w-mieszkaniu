from mieszkanie_czesciowo_skrecone import House
import matplotlib.pyplot as plt
import numpy as np
from dane import outside_temperature_a

initial_temperature = outside_temperature_a[0]


knobs = 5  
domek = House(initial_temperature, outside_temperature_a, len(outside_temperature_a), knobs)
domek.main(7200*8, 7200*15)
