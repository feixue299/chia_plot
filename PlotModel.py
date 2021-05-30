TimeInterval = 1
ProgressInterval = 2


class PlotModel:
    plot_total: int = 0
    plotting_number: int = 0
    launch_interval: int = 0
    interval_type: int = TimeInterval
    finger_print: str = ''
    farmer_public_key: str = ''
    pool_public_key: str = ''
    k_size: int = 32
    ram: int = 3390
    threads: int = 2
    temp_dir: str = ''
    final_dir: str = ''

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
