import time
import os
from Battery import Battery

class Reading():
    # Set to 500 because 500 is 10% of the overall capacity
    FAILURE_POINT = 500

    def __init__(self, input_file, output_file):
        self.input_file = input_file
        self.output_file = output_file

    def read_and_save(self, battery):
        with open(self.input_file, 'r') as f_input, open(self.output_file, 'w') as f_output:
            line_number = 0
            for line in f_input:
                line_number += 1
                timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
                reading_context = f"Line {line_number}: {timestamp} - {line}"
                f_output.write(reading_context)
                time.sleep(0.1)
                battery.drain(10)
                if(battery.soc <= Reading.FAILURE_POINT) :
                    os.system("python3 close.py")
                    return battery.soc
            return battery.soc
        
    def read_and_save2(self, battery):
        # Simulate battery-powered operations assuming battery charge is 100

        # Check file Q and read its contents if it exists
        #content_Q = check_file_Q()
        # log when Q is present on reboot <-- will record to interruptions.txt any time the system reboots
        try:
            # Copy contents from file A to file B line by line
            with open(self.input_file, "r") as f_input:
                for line in f_input:
                    # greater than 10% battery life left
                    if battery.charge > 10:   
                        # Copy line from file A to file B
                        with open(self.output_file, "a") as f_output:
                            f_output.write(line)
                            # print(f"Line '{line.strip()}' copied to {self.output_file}")
                    if 5<battery.charge <= 10:
                        # If battery is down to 10%, copy the remaining content from file A to file Q
                        with open("backups/backup_file.txt", "a") as f_backup:
                            f_backup.write(line)
                            print(f"Copying remaining content to backup file due to low battery") 
                    
                    # Monitoring battery stage based on read and write operations
                    battery.discharge(0.0001*1, 0.0001*1) # (0.0001*len(content_Q), 1) <-- Q wasn't there or length was zero
        except SystemExit as e:
            print("Shutting down the simulator")
            
        # Charging the battery
        #battery.charge_battery(20)
				
    # Function to check if file Q exists and read its contents
    def check_file_Q():
        if os.path.exists("Q.txt"):
            with open("Q.txt", "r") as file_Q:
                content_Q = file_Q.read()
                print(f"Contents in file Q: {content_Q}")
                return content_Q
        else:
            print("File Q does not exist.")
            return None



# if __name__ == "__main__":
#def run_sensors() :
    #input_file = "log_2023-08-25_13-10-13.txt"
    #output_file = "b.txt"

    # reader = Reading(input_file, output_file)
    #reader.read_and_save()

