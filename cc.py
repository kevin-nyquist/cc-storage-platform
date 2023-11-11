import os

class Battery:
    def __init__(self, capacity=100, charge=100):
        self.capacity = capacity
        self.charge = charge
        self.plugged_in = False
        self.power_consumption_read = 1  # Power consumption for read operation
        self.power_consumption_write = 2  # Power consumption for write operation

    def discharge(self, read_count, write_count):
        if not self.plugged_in:
            discharge_amount = read_count * self.power_consumption_read + write_count * self.power_consumption_write
            self.charge -= discharge_amount
            if self.charge < 0:
                self.charge = 0
                print("Simulator shutting down due to low battery!")
                # Exit the simulation if charge drops below 0
                exit()

    def charge_battery(self, amount):
        self.charge += amount
        if self.charge > self.capacity:
            self.charge = self.capacity
        print(f"Charging {amount} units. Remaining charge: {self.charge}")

    def toggle_plug(self):
        self.plugged_in = not self.plugged_in
        if self.plugged_in:
            print("Plugged in.")
        else:
            print("Unplugged.")

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

# Simulate battery-powered operations
battery = Battery(capacity=100, charge=100)
content_Q = check_file_Q()
while battery.charge > 5:
    # Check file Q and read its contents if it exists
    #content_Q = check_file_Q()

    # Copy contents from file A to file B line by line
    with open("A.txt", "r") as file_A:
        for line in file_A:
            if 5<battery.charge <= 10:
                # If battery is down to 10%, copy the remaining content from file A to file Q
                with open("Q.txt", "a") as file_Q:
                    file_Q.write(line)
                    print(f"Copying remaining content to file Q due to low battery")
            if battery.charge > 10:
                # Copy line from file A to file B
                with open("B.txt", "a") as file_B:
                    file_B.write(line)
                    print(f"Line '{line.strip()}' copied to file B")

            # Monitoring battery stage based on read and write operations
            battery.discharge(0.0001*len(content_Q), 1)

    # Charging the battery
    #battery.charge_battery(20)

# Shut down the simulator when battery is down to 5%
print("Shutting down the simulator")

