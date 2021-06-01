import wx

from CreateJobs import CreateJobs
from JobsModel import JobsModel
from PlotModel import *


class Jobs(wx.Panel):
    def __init__(self, parent):
        super().__init__(parent)

        jobs_box = wx.StaticBox(self, label="任务列表")
        jobs_box_sizer = wx.StaticBoxSizer(jobs_box, wx.HORIZONTAL)

        h_box = wx.BoxSizer(wx.HORIZONTAL)

        self.job_list = wx.ListCtrl(self, -1, style=wx.LC_REPORT)
        self.job_list.Bind(wx.EVT_LIST_ITEM_SELECTED, self.list_ctrl_select)
        title_group = ["序号", "缓存磁盘", "缓存磁盘2", "最终磁盘",
                       "间隔", "并发数", "线程数", "内存大小",
                       "锄地数量", "已完成锄地数量",
                       "指纹", "农场公钥", "矿池公钥"]
        for index in range(len(title_group)):
            self.job_list.InsertColumn(index, title_group[index])

        h_box.Add(self.job_list, 1)

        v_box = wx.BoxSizer(wx.VERTICAL)
        self.create_button = wx.Button(self, label="新建任务")
        self.delete_button = wx.Button(self, label="删除任务")
        self.create_button.Bind(wx.EVT_BUTTON, self.create_jobs)
        self.delete_button.Bind(wx.EVT_BUTTON, self.delete_jobs)
        v_box.Add(self.create_button)
        v_box.AddSpacer(20)
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

        for index in range(len(self.jobs_model.jobs)):
            job: PlotModel = self.jobs_model.jobs[index]
            index = self.job_list.InsertItem(self.job_list.GetItemCount(), str(self.job_list.GetItemCount() + 1))
            str_group = [job.temp_dir, "无", job.final_dir,
                         str(job.launch_interval) + str("分钟" if job.interval_type == TimeInterval else "%"),
                         str(job.plotting_number), str(job.threads), str(job.ram),
                         str(job.plot_total), str(job.plotting_finish),
                         job.finger_print, job.farmer_public_key, job.pool_public_key]

            for column in range(len(str_group)):
                self.job_list.SetItem(index, column + 1, str_group[column])
