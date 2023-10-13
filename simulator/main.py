import pandas as pd
from EnergyLoader import EnergyLoader 
from Timer import Timer
from Battery import Battery
from read import Reading
import threading
import time

timer = Timer(init_time="2015-07-10")
battery = Battery( soc=4000, capacity=5000, base_consume=5, is_monitored=True, monitoring_interval=10)
energy = EnergyLoader(timer, energy_file_path="energy_dataset.csv", energy_col="Power", resolution="hour")
reading = Reading("log_2023-08-25_13-10-13.txt", "b.txt")

# print(energy.df.head())
# print(energy.df.tail())

# battery monitoring function - Kevin
def battery_monitor() :
    # Start of monitoring thread to check the SOC of the battery at a specified interval
    battery_measure_thread = threading.Thread(daemon=True, target=battery.monitor_battery_level)
    battery_measure_thread.start()
    
    # call reading sensor data
    # battery.soc = reading.read_and_save(battery.soc)
    reading.read_and_save(battery)

    # end thread
    battery.is_monitored = False
    # this join thread line would wait until the monitoring cycle was finished to terminate
    # battery_measure_thread.join()


def full_drain() :
    battery.drain(battery)

def main():
    # initial battery level
    # print(f"Initial SOC:{battery.soc}")

    start = time.perf_counter()
    battery_monitor()
    end = time.perf_counter()
    print(f"Total time taken: {end - start} seconds")

    # final battery level
    print(f"Final SOC:{battery.soc}")
    

if __name__ == "__main__":
    main()

# def Simulator():
#     ### simulation function
#     pass
#     battery_monitor()


#     return None

# monitor the power stage

# set a frequency during the sensing operation interval (every 10 sec)
# test different frequencies

# trigger the power failure event at certain battery % level


# definition of the power draw for each sensor - Kevin