import pandas as pd


class EnergyLoader:
    """
    energy loader
    """
    def __init__(self, timer, energy_file_path, energy_col, resolution="hour"):
        self.energy_file_path = energy_file_path
        self.timer            = timer
        self.resolution       = resolution
        self.energy_col       = energy_col       # power
        self.df      = None             # dataframe of hourly data
        self.load_energy(resolution='hour')      
       
 
    def load_energy_hour(self, start, end, column):
        if self.df is not None:
            df = self.df
        else:
            energy_pred = pd.read_csv(self.energy_file_path)
            df = energy_pred 
            df['time'] = pd.to_datetime(df['Time'])
            df = df.set_index('time')
            self.df = df
        res = df[ (df.index >= start) & (df.index < end) ][column]
        return res
        
        
    def load_energy_driver(self, column, start=None, end=None, resolution='hour'):
        if not start:        
            start = self.timer.curr_time        # default start time is curr
        if not end:
            end = start + pd.Timedelta(days=1)  # default end time
        if 'hour' == resolution:
            return self.load_energy_hour(start, end, column).values


        
    def load_energy(self, start=None, end=None, resolution="hour", column=None):
        if not column:
            column = self.energy_col
        return self.load_energy_driver(column=column, start=start, end=end, resolution=resolution)
        
