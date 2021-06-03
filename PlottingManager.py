import os
import subprocess
import threading
import time

from ChiaCommand import ChiaCommand
from JobsModel import JobsModel
from PlotModel import PlotModel, TimeInterval, ProgressInterval

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
        self.pid = None

    def start(self):
        args = ["plots", "create",
                "-k", str(self.job.k_size),
                "-b", str(self.job.ram),
                "-r", str(self.job.threads),
                "-t", self.job.temp_dir,
                "-d", self.job.final_dir]

        self.filePath = "plotting_log_job_create_" + self.job.create_date +\
                        "_plotting_create_" + self.create_time + ".log"
        path = os.path.join(PlottingPath, self.filePath)
        print("path:", path)
        with open(path, 'w') as f:
            cmd = [ChiaCommand.getChiaPath()] + args
            out = subprocess.Popen(args=cmd, stdout=f, shell=True)
            f.close()
            self.pid = out.pid
            print("pid:", out.pid)
            print("command:", out.args)

        b = threading.Thread(name=self.filePath, target=self.background)
        b.start()

    def background(self):
        while self.progress < 1:
            time.sleep(5)
            log_file = open(os.path.join(PlottingPath, self.filePath), "r")
            percent = len(log_file.readlines()) / 2600
            self.progress = min(percent, 1)
            log_file.close()


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
            print("当前并发锄地数:", len(self.plottings))
            print("当前并发情况：", self.getCurrentPlottingStatus())
            for key, value in jobsDict.items():
                value: PlotModel
                job_plotting_group = self.jobs_plotting_dict.get(key, [])
                plotting_count = len(job_plotting_group)
                if value.plotting_number > plotting_count:
                    def create_new_plotting():
                        new_plotting = PlottingModel(value)
                        self.plottings.append(new_plotting)
                        job_plotting_group.append(new_plotting)
                        self.jobs_plotting_dict[key] = job_plotting_group
                        new_plotting.start()
                        time.sleep(5)

                    if plotting_count > 0:
                        last_plotting: PlottingModel = job_plotting_group[plotting_count - 1]

                        if value.interval_type == TimeInterval and \
                                time.time() - int(last_plotting.create_time) > value.launch_interval * 60:
                            create_new_plotting()
                        elif value.interval_type == ProgressInterval and \
                                last_plotting.progress * 100 > value.launch_interval:
                            create_new_plotting()
                    else:
                        create_new_plotting()

                for plotting in job_plotting_group:
                    if plotting.progress >= 1:
                        job_plotting_group.remove(plotting)

            time.sleep(5)

    def getCurrentPlottingStatus(self):
        status = {}
        for key, value in self.jobs_plotting_dict.items():
            progress_group = []
            for model in value:
                model: PlottingModel
                progress_group.append(model.progress)
            status[key] = progress_group
        return status

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
        file.close()
        return read


plotting_manager = PlottingManager()
