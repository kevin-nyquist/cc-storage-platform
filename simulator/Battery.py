import time


class Battery:
    """
    soc           : state of charge
    capacity      : capacity
    mini          : minimum energy     
    base_consume  : basic energy consumption for each boot up
    
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
        

    def monitor_battery_level(self):
        while self.is_monitored:
            print(f"Current battery level: {self.soc}")
            time.sleep(self.monitoring_interval)