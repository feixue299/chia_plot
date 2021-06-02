import os
import subprocess
import threading
import time

from ChiaCommand import ChiaCommand
from JobsModel import JobsModel
from PlotModel import PlotModel

PlottingPath = "Plotting"


def start_manager():
    plotting_manager.jobs = JobsModel.readFromFile().jobs
    plotting_manager.startPlotting()


def stop_manager():
    plotting_manager.stopPlotting()


class PlottingModel:
    def __init__(self, job):
        self.create_time = str(int(time.time()))
        self.job: PlotModel = job
        self.progress: float = 0
        self.filePath = ""

    def start(self):
        args = ["chia", "plots", "create",
                "-k", str(self.job.k_size),
                "-b", str(self.job.ram),
                "-r", str(self.job.threads),
                "-t", self.job.temp_dir,
                "-d", self.job.final_dir]

        self.filePath = "job_create:" + self.job.create_date + "plotting_create:" + self.create_time
        output = open(os.path.join(PlottingPath, self.filePath), 'w')
        os.chdir(ChiaCommand.getChiaLocationPath())
        out = subprocess.Popen(args=args, stdout=output)
        print("pid:", out.pid)
        print("command:", out.args)
        b = threading.Thread(name=self.filePath, target=self.background)
        b.start()

    def background(self):
        while self.progress < 1:
            log_file = open(os.path.join(PlottingPath, self.filePath), "rU")
            percent = log_file.readlines() / 2600
            self.progress = min(percent, 1)
            time.sleep(5)


class PlottingManager:

    def __init__(self):
        self.jobs = []
        self.plottings: [PlottingModel] = []
        self.jobs_plotting_dict = {}
        self.plotting = False

    def startPlotting(self):
        self.plotting = True
        b = threading.Thread(name="Plotting Manager", target=self.createPlotting)
        b.start()

    def createPlotting(self):
        while self.plotting:
            jobsDict = self.getJobsDict()
            for job in jobsDict:
                job: PlotModel
                job_plotting_group = self.jobs_plotting_dict.get(job.create_date, [])
                if job.plotting_number > len(job_plotting_group):
                    new_plotting = PlottingModel(job)
                    self.plottings.append(new_plotting)
                    job_plotting_group.append(new_plotting)
                    self.jobs_plotting_dict[job.create_date] = job_plotting_group
                    new_plotting.start()
            time.sleep(5)

    def getJobsDict(self):
        jobsDict = {}
        for job in self.jobs:
            job: PlotModel
            jobsDict[job.create_date] = job
        return jobsDict

    def stopPlotting(self):
        self.plotting = False

    @staticmethod
    def createManager():
        if os.path.exists(PlottingPath):
            return PlottingManager.createManagerFile(PlottingPath)
        else:
            os.mkdir(PlottingPath)
            return PlottingManager.createManagerFile(PlottingPath)

    @staticmethod
    def createManagerFile(dir_path):
        file = open(os.path.join(dir_path, "PlottingManager.json"), "r")
        read = file.read()
        print("file:", file)
        file.close()
        return read


plotting_manager = PlottingManager()
