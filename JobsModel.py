import PlotModel


class JobsModel(object):
    def __init__(self, **kwargs):
        self.jobs: [PlotModel] = []
        self.__dict__.update(kwargs)

    def __repr__(self):
        return "[%s]" % self.jobs
