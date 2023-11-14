import os
import pandas as pd
from Timer import Timer
from Battery import Battery
from read import Reading
import time

class Simulator:
    """
    Simulator for testing data capturing ability during power failure and low power
    """

    def __init__(self, battery: Battery, timer: Timer, 
                 reading: Reading, sensing_freq: 
                 int, window: int):
        self.battery = battery
        self.timer = timer
        self.reading = reading
        self.sensing_freq = sensing_freq 
        self.window = window

    # Runs an entire sensing window as defined by a simulator object
    def run(self):
        # Check for backup file
        backups_file_path = "backups/backup_file.txt"
        reboot = Simulator.check_if_backup_exists(backups_file_path)
        if (reboot) :
            print("System reboot")

        # Initialize wait time between operations and end time for the sensing window
        wait_time = self.window / self.sensing_freq
        end_time = self.timer.calculate_window(pd.Timedelta(seconds=self.window))

        # Print current time and scheduled end time of the window
        print(f"Current time {self.timer.curr_time}")
        print(f"End time {end_time}")

        # Conduct all sensing operations within the given sensing window and space out operations wait_time
        while self.timer.curr_time <= end_time:
            # Monitor battery throughout window and start timer to measure the length of the sensing operation
            self.battery.battery_monitor()
            start = time.perf_counter()

            # Conduct the sensing operation
            self.reading.read_and_save(self.battery)
            
            # End timer and battery monitor and print results
            self.battery.stop_monitoring()
            if (self.battery.charge == 0) :
                break
            end = time.perf_counter()
            print(f"Total time taken: {end - start} seconds")
            
            # Increment the window timer and schedule next operation if there is enough time left in the window
            self.timer.forward(pd.Timedelta(seconds=(end - start + wait_time)))
            if (self.timer.curr_time < end_time):
                time.sleep(wait_time)

    # Given a file path, return True if it exists in the file system; False otherwise
    def check_if_backup_exists(f_backup) :
        if (os.path.exists(f_backup)):
            with open(f_backup, 'r') as backups_input:
                contents = backups_input.read()
                if "marker" in contents:
                    print("Successfully identified reboot")
                    return True
        return False