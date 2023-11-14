import time
import os
from Battery import Battery
from datetime import datetime

class Reading():

    def __init__(self, input_file, output_file):
        self.input_file = input_file
        self.output_file = output_file

    # Simulate battery-powered operations for reading sensors
    def read_and_save(self, battery):
        # Set thresholds to 10% and 5% of total capacity
        low_battery = battery.capacity * 0.1
        critically_low_battery = battery.capacity * 0.05

        # Check backup file and read its contents if it exists
        backup_content = Reading.check_backup_file() # move to only run once at start of operations
        if (backup_content) : 
            print(f"Contents in backup file: {backup_content}")

        # log when the backup file is present on reboot <-- will record to interruptions.txt at reboot
        try:
            # Copy contents from the input file(senors) to the output file line by line
            with open(self.input_file, "r") as f_input:
                for line in f_input:
                    # greater than 10% battery life left
                    if battery.charge > low_battery:   
                        # Copy input to the output file
                        with open(self.output_file, "a") as f_output:
                            f_output.write(line)
                            # print(f"Line '{line.strip()}' copied to {self.output_file}")
                    if critically_low_battery < battery.charge <= low_battery:
                        # If battery is at 10% or below, copy the remaining content  to the backup file
                        with open("backups/backup_file.txt", "a") as f_backup:
                            f_backup.write(line)
                            # print(f"Copying remaining content to backup file due to low battery") 
                    
                    # Monitoring battery stage based on read and write operations
                    battery.discharge(0.0001*len(backup_content), 1)
        except SystemExit as e:
            with open("backups/interruptions.txt", "a") as f_interruptions:
                    f_interruptions.write("System Shutdown at: " + str(datetime.now()) + "\n")
				
    # Function to check if backup file exists and if it does, read its contents
    def check_backup_file():
        if os.path.exists("backups/backup_file.txt"):
            with open("backups/backup_file.txt", "r") as f_backup:
                backup_content = f_backup.read()
                # print(f"Contents in backup file: {backup_content}")
                return backup_content
        return None
