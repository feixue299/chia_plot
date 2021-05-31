import json
import os

import wx
from wx import FileDialog

from CreateJobs import CreateJobs
from JobsModel import JobsModel
from PlotModel import PlotModel


class Jobs(wx.Panel):
    def __init__(self, parent):
        super().__init__(parent)

        jobs_box = wx.StaticBox(self, label="任务列表")
        jobs_box_sizer = wx.StaticBoxSizer(jobs_box, wx.HORIZONTAL)

        h_box = wx.BoxSizer(wx.HORIZONTAL)

        self.job_list = wx.ListCtrl(self, -1, style=wx.LC_REPORT)
        self.job_list.InsertColumn(0, "序号")
        self.job_list.InsertColumn(1, "缓存磁盘")
        self.job_list.InsertColumn(2, "缓存磁盘2")
        self.job_list.InsertColumn(3, "最终磁盘")
        self.job_list.InsertColumn(4, "并发数")
        self.job_list.InsertColumn(5, "并发中")
        self.job_list.InsertColumn(6, "线程数")
        self.job_list.InsertColumn(7, "内存大小")
        self.job_list.InsertColumn(8, "待锄地数量")
        self.job_list.InsertColumn(9, "已进行锄地数量")
        self.job_list.InsertColumn(10, "指纹")
        self.job_list.InsertColumn(11, "农场公钥")
        self.job_list.InsertColumn(12, "矿池公钥")

        h_box.Add(self.job_list, 1)

        v_box = wx.BoxSizer(wx.VERTICAL)
        self.create_button = wx.Button(self, label="新建任务")
        self.delete_button = wx.Button(self, label="删除任务")
        self.create_button.Bind(wx.EVT_BUTTON, self.create_jobs)
        self.delete_button.Bind(wx.EVT_BUTTON, self.delete_jobs)
        v_box.Add(self.create_button)
        v_box.Add(self.delete_button)
        h_box.Add(v_box, 0, wx.ALIGN_CENTER_VERTICAL)

        jobs_box_sizer.Add(h_box, 1, wx.EXPAND)

        self.SetSizer(jobs_box_sizer)
        self.update_jobs()

    def create_jobs(self, event):
        create_jobs = CreateJobs(self)
        create_jobs.ShowModal()

    def delete_jobs(self, event):
        file = FileDialog(self, message="选择单个文件", style=wx.FD_OPEN)
        file.ShowModal()

    def update_jobs(self):
        path = "config.json"
        try:
            if os.path.exists(path):
                with open(path, "r") as f:
                    read = f.read()
                    load_dir = json.loads(read)
                    print("load_dir:", load_dir)
                    jobs_model: JobsModel = json.loads(read, object_hook=lambda d: PlotModel(**d))
                    print("jobs_model.jobs:", jobs_model.jobs)
            else:
                self.createFile(path)
        finally:
            pass

    def createFile(self, path):
        with open(path, "w+") as f:
            json.dump(JobsModel().__dict__, f)
            f.close()
            print("创建文件")
            self.writeJson()
