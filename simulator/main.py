import pandas as pd
from EnergyLoader import EnergyLoader 
from Timer import Timer
from Battery import Battery
# import DataCollector from DataCollector

timer = Timer(init_time="2015-07-10")
battery = Battery( soc=4000, capacity=5000, base_consume=5)
energy = EnergyLoader(timer, energy_file_path="energy_dataset.csv", energy_col="Power", resolution="hour")

print(energy.df.head())
print(energy.df.tail())


def Simulator():
    ### simulation function
    pass





    return None


# battery monitoring function - Kevin
# def battery_monitor() :
    # monitor the power stage

    # set a frequency during the sensing operation interval (every 10 sec)
    # test different frequencies

    # trigger the power failure event at certain battery % level


# definition of the power draw for each sensor - Kevin

# def power_failure(int soc) :
    # battery.drain(soc, soc) use this function to drop the soc to simulate battery dying

