import json
from json import JSONEncoder

TimeInterval = 1
ProgressInterval = 2


class PlotModel:
    def __init__(self):
        self.plot_total: int = 0
        self.plotting_number: int = 0
        self.launch_interval: int = 0
        self.interval_type: int = TimeInterval
        self.finger_print: str = ''
        self.farmer_public_key: str = ''
        self.pool_public_key: str = ''
        self.k_size: int = 32
        self.ram: int = 3390
        self.threads: int = 2
        self.temp_dir: str = ''
        self.final_dir: str = ''

    def check(self):
        if self.plot_total > 0 and \
                self.plotting_number > 0 and \
                len(self.final_dir) > 0 and \
                len(self.farmer_public_key) > 0 and \
                len(self.pool_public_key) > 0 and \
                len(self.temp_dir) > 0 and \
                len(self.final_dir) > 0:
            return True
        else:
            return False
