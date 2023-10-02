


class Battery:
    """
    soc           : state of charge
    capacity      : capacity
    mini          : minimum energy     
    base_consume  : basic energy consumption for each boot up
    
    """
    
    def __init__(self, soc, capacity, base_consume):
        self.soc = soc
        self.capacity = capacity
        self.base_consume = base_consume
        
    
    def drain(self, drain):
        soc = self.soc - drain
        self.soc = [0,soc][soc>0]
        
        
    def charge(self, gain):
        soc = self.soc + gain
        self.soc = [soc,self.capacity][soc>self.capacity]
        