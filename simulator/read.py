import time
import os
from Battery import Battery

class Reading():
    # Set to 500 because 500 is 10% of the overall capacity
    FAILURE_POINT = 500

    def __init__(self, input_file, output_file):
        self.input_file = input_file
        self.output_file = output_file

    def read_and_save(self, battery_level):
        with open(self.input_file, 'r') as f_input, open(self.output_file, 'w') as f_output:
            line_number = 0
            for line in f_input:
                line_number += 1
                timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
                reading_context = f"Line {line_number}: {timestamp} - {line}"
                f_output.write(reading_context)
                time.sleep(0.5)
                battery_level -= 10
                # manual failure at 3900 SOC
                if(battery_level == 3900) :
                    battery_level = 0
                if(battery_level <= Reading.FAILURE_POINT) :
                    os.system("python3 close.py")
                    return battery_level
            return battery_level
				
# if __name__ == "__main__":
#def run_sensors() :
    #input_file = "log_2023-08-25_13-10-13.txt"
    #output_file = "b.txt"

    # reader = Reading(input_file, output_file)
    #reader.read_and_save()

