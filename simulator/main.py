import pandas as pd
from EnergyLoader import EnergyLoader 
from Timer import Timer
from Battery import Battery


timer = Timer(init_time="2015-07-10")
battery = Battery( soc=4000, capacity=5000, base_consume=5)
energy = EnergyLoader(timer, energy_file_path="energy_dataset.csv", energy_col="Power", resolution="hour")

print(energy.df.head())
print(energy.df.tail())


def Simulator():
    ### simulation function
    pass





    return None

