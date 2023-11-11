import os
import threading
import time
import sys

"""
    capacity      : capacity
    charge           : state of charge
    base_consume  : basic energy consumption for each boot up
    is_monitored  : whether the battery is being actively monitored or not
    monitoring_interval : the length in time in which we want to monitor the battery
    """

class Battery:
    def __init__(self, capacity, charge, base_consume, is_monitored, monitoring_interval):
        self.capacity = capacity
        self.charge = charge
        self.base_consume = base_consume
        self.is_monitored = is_monitored
        self.monitoring_interval = monitoring_interval
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
                sys.exit()

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

    def battery_monitor(self) :
        # Start of monitoring thread to check the SOC of the battery at a specified interval
        battery_measure_thread = threading.Thread(daemon=True, target=self.monitor_battery_level)
        battery_measure_thread.start()

    def monitor_battery_level(self):
        while self.is_monitored:
            print(f"Current battery level: {self.charge}")
            time.sleep(self.monitoring_interval)

    def stop_monitoring(self):
        self.is_monitored = False