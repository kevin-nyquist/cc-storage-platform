import pandas as pd
from datetime import datetime


class Timer:
    def __init__(self, init_time, curr_time=None, date_format="%Y-%m-%d"):
        self.init_time = datetime.strptime(init_time, date_format)
        self.curr_time = self.init_time if not curr_time else datetime.strptime(init_time, date_format)
        
    def step(self, size=1):
        # size unit: second
        self.curr_time += pd.Timedelta(seconds=size)
    
    def forward(self, step):
        self.curr_time += step


    def backward(self, step):
        self.curr_time -= step

    def calculate_window(self, step):
        return self.curr_time + step





