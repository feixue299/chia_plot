import json
import os

from PlotModel import PlotModel

ConfigDirPath = "Config"
ConfigPath = "config.json"


class JobsModel(object):

    def __init__(self):
        super(JobsModel, self).__init__()
        self.jobs = []

    def __repr__(self):
        return "[%s]" % self.jobs

    def writeToDefaultFile(self):
        self.writeToCustomFile(ConfigDirPath, ConfigPath)

    def writeToCustomFile(self, dir_path, path):
        if not os.path.exists(dir_path):
            os.mkdir(dir_path)

        with open(os.path.join(dir_path, path), "w+") as f:
            model_dir = {"jobs": []}

            for job in self.jobs:
                model_dir["jobs"] = model_dir["jobs"] + [job.__dict__]

            json.dump(model_dir, f)
            f.close()

    @staticmethod
    def readFromFile():
        try:
            if os.path.exists(os.path.join(ConfigDirPath, ConfigPath)):
                with open(os.path.join(ConfigDirPath, ConfigPath), "r") as f:
                    read = f.read()
                    load_dir = json.loads(read)
                    jobs_model = JobsModel()
                    for plot in load_dir["jobs"]:
                        plot_model = PlotModel()
                        plot_model.__dict__.update(plot)
                        jobs_model.jobs.append(plot_model)

                    f.close()
                    return jobs_model
            else:
                jobs_model = JobsModel()
                jobs_model.writeToDefaultFile()
                return jobs_model
        finally:
            pass
