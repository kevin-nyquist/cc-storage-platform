import time
import os

class Reading:
    

    def __init__(self, input_file, output_file):
        self.input_file = input_file
        self.output_file = output_file

    def read_and_save(self):
        failure = 0
        with open(self.input_file, 'r') as f_input, open(self.output_file, 'w') as f_output:
            line_number = 0
            for line in f_input:
                line_number += 1
                timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
                reading_context = f"Line {line_number}: {timestamp} - {line}"
                f_output.write(reading_context)
                time.sleep(1)
                failure+=1
                if(failure == 3) :
                    # exit(-1)
                    os.system("python3 close.py")
				


if __name__ == "__main__":
    input_file = "log_2023-08-25_13-10-13.txt"
    output_file = "b.txt"

    reader = Reading(input_file, output_file)
    reader.read_and_save()

