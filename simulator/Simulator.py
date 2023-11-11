import os
import pandas as pd
from Timer import Timer
from Battery import Battery
from read import Reading
import time
# import atexit


class Simulator:
    """
    Simulator for testing data capturing ability during power failure and low power
    """

    def __init__(self, battery: Battery, timer: Timer, reading: Reading, worst_case: bool, sensing_freq: int, window: int):
        self.battery = battery
        self.timer = timer
        self.reading = reading
        self.worst_case = worst_case
        self.sensing_freq = sensing_freq 
        self.window = window

    def run(self):
        backups_file_path = "backups/backup_file.txt"
        reboot = False

        wait_time = self.window / self.sensing_freq

        if (os.path.exists(backups_file_path)):
            with open(backups_file_path, 'r') as backups_input:
                contents = backups_input.read()
                if "marker" in contents:
                    reboot = True
                    print("Successfully identified reboot")
                # line_number = 0
                # for line in f_input:
                #     line_number += 1
                #     if(line == "marker")

        end_time = self.timer.sum(pd.Timedelta(seconds=self.window))
        print(f"Current time {self.timer.curr_time}")
        print(f"End time {end_time}")
        while self.timer.curr_time <= end_time:
            # start_soc = self.battery.soc
            
            # monitor battery throughout window
            self.battery.battery_monitor()

            start = time.perf_counter()
            self.reading.read_and_save(self.battery)
            end = time.perf_counter()
            print(f"Total time taken: {end - start} seconds")
            self.battery.stop_monitoring()
            
            self.timer.forward(pd.Timedelta(seconds=(end - start + wait_time)))
            if (self.timer.curr_time < end_time):
                time.sleep(wait_time)
            

            
            
        







# def exit_handler():
#     print('My application is ending!')

# atexit.register(exit_handler)
