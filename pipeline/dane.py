import numpy as np
import csv
import json



file_temp = "C:/Users/48665/Desktop/modelowanie/temp_data.csv"
file_constans  = "C:/Users/48665/Desktop/modelowanie/constants.json"

density = 0
specific_heat = 0
radiators_power = 0
alpha = 0


with open(file_constans, mode='r', encoding='utf-8') as file:
    data = json.load(file)
    constants = data["constants"]
    density = constants.get("air density", 0)
    specific_heat = constants.get("specific heat", 0)
    radiators_power = constants.get("radiators power", 0)
    alpha = constants.get("alpha", 0)

outside_temperature_a = []
outside_temperature_b = []
outside_temperature_c = []

with open(file_temp, mode='r') as file:
    reader = csv.reader(file)
    next(reader)
    for row in reader:
        outside_temperature_a.append(float(row[1])+273.15)
        outside_temperature_b.append(float(row[2])+273.15)
        outside_temperature_c.append(float(row[3])+273.15)

def iteration_temperature(temp_godzinowa, iteration=(7200)):
    temp_ht=[]
    for temp in temp_godzinowa:
        temp_ht.extend(np.repeat(temp, iteration))
    return(temp_ht)
  
outside_temperature_a=iteration_temperature(outside_temperature_a)
outside_temperature_b=iteration_temperature(outside_temperature_b)
outside_temperature_c=iteration_temperature(outside_temperature_c)

times=len(outside_temperature_a)

ht = 0.5
hx = 0.5