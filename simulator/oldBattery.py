import time
import threading

class Battery:
    """
    soc           : state of charge
    capacity      : capacity
    mini          : minimum energy     
    base_consume  : basic energy consumption for each boot up
    is_monitored  : whether the battery is being actively monitored or not
    monitoring_interval : the length in time in which we want to monitor the battery
    """
    
    def __init__(self, soc, capacity, base_consume, is_monitored, monitoring_interval):
        self.soc = soc
        self.capacity = capacity
        self.base_consume = base_consume
        self.is_monitored = is_monitored
        self.monitoring_interval = monitoring_interval
        
    
    def drain(self, drain):
        soc = self.soc - drain
        self.soc = [0,soc][soc>0]
        
        
    def charge(self, gain):
        soc = self.soc + gain
        self.soc = [soc,self.capacity][soc>self.capacity]
        
    def battery_monitor(self) :
        # Start of monitoring thread to check the SOC of the battery at a specified interval
        battery_measure_thread = threading.Thread(daemon=True, target=self.monitor_battery_level)
        battery_measure_thread.start()

    def monitor_battery_level(self):
        while self.is_monitored:
            print(f"Current battery level: {self.soc}")
            time.sleep(self.monitoring_interval)

    def stop_monitoring(self):
        self.is_monitored = False