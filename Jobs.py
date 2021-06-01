import json
import os
import sys

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
        self.job_list.Bind(wx.EVT_LIST_ITEM_SELECTED, self.list_ctrl_select)
        self.job_list.InsertColumn(0, "序号")
        self.job_list.InsertColumn(1, "缓存磁盘")
        self.job_list.InsertColumn(2, "缓存磁盘2")
        self.job_list.InsertColumn(3, "最终磁盘")
        self.job_list.InsertColumn(4, "并发数")
        self.job_list.InsertColumn(5, "线程数")
        self.job_list.InsertColumn(6, "内存大小")
        self.job_list.InsertColumn(7, "待锄地数量")
        self.job_list.InsertColumn(8, "指纹")
        self.job_list.InsertColumn(9, "农场公钥")
        self.job_list.InsertColumn(10, "矿池公钥")

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
        self.update_jobs()

    def list_ctrl_select(self, e):
        item: wx.ListItem = e.GetItem()
        self.current_item = item

    def delete_jobs(self, event):
        if self.current_item is not None:
            del self.jobs_model.jobs[self.current_item.GetId()]
            self.jobs_model.writeToDefaultFile()
            self.update_jobs()

    def update_jobs(self):
        self.job_list.DeleteAllItems()

        self.jobs_model: JobsModel = JobsModel.readFromFile()

        for index in range(0, len(self.jobs_model.jobs)):
            job: PlotModel = self.jobs_model.jobs[index]
            index = self.job_list.InsertItem(self.job_list.GetItemCount(), str(self.job_list.GetItemCount() + 1))
            self.job_list.SetItem(index, 1, job.temp_dir)
            self.job_list.SetItem(index, 2, "无")
            self.job_list.SetItem(index, 3, job.final_dir)
            self.job_list.SetItem(index, 4, str(job.plotting_number))
            self.job_list.SetItem(index, 5, str(job.threads))
            self.job_list.SetItem(index, 6, str(job.ram))
            self.job_list.SetItem(index, 7, str(job.plot_total))
            self.job_list.SetItem(index, 8, job.finger_print)
            self.job_list.SetItem(index, 9, job.farmer_public_key)
            self.job_list.SetItem(index, 10, job.pool_public_key)

