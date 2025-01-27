from mieszkanie import House
import matplotlib.pyplot as plt
import numpy as np
from dane import outside_temperature_a, outside_temperature_b, outside_temperature_c


initial_temperature = 273.15 + 10
max_temperature= 273.15 + 26 

domek=House(initial_temperature, outside_temperature_a, max_temperature, len(outside_temperature_a)) 
domek.main()
