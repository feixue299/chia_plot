import os
import subprocess
import platform

import wx

from JobsModel import JobsModel
from PlotModel import PlotModel


class PlottingList(wx.Panel):
    def __init__(self, parent):
        super(PlottingList, self).__init__(parent)

        box = wx.StaticBox(self, label="锄地列表")
        box_sizer = wx.StaticBoxSizer(box, wx.HORIZONTAL)

        self.plotting_list = wx.ListCtrl(self, -1, style=wx.LC_REPORT)
        self.plotting_list.Bind(wx.EVT_LIST_ITEM_SELECTED, self.list_ctrl_select)

        title_group = ["序号", "配置序号", "并发序号",
                       "进度", "开始时间", "结束时间", "总耗时",
                       "PID", "线程ID"]

        for index in range(len(title_group)):
            self.plotting_list.InsertColumn(index, title_group[index])

        box_sizer.Add(self.plotting_list, 1, wx.EXPAND)

        button_box = wx.BoxSizer(wx.VERTICAL)

        self.stop_button = wx.Button(self, label="停止增加p盘")
        self.start_button = wx.Button(self, label="启动")

        self.stop_button.Bind(wx.EVT_BUTTON, self.stop_button_click)
        self.start_button.Bind(wx.EVT_BUTTON, self.start_button_click)

        self.stop_button.Disable()
        self.start_button.Enable()

        button_box.Add(self.stop_button)
        button_box.AddSpacer(20)
        button_box.Add(self.start_button, 1, wx.EXPAND)

        box_sizer.Add(button_box, 0, wx.ALIGN_CENTER_VERTICAL)

        self.SetSizer(box_sizer)

    def list_ctrl_select(self, e):
        pass

    def stop_button_click(self, e):
        self.stop_button.Disable()
        self.start_button.Enable()

    def start_button_click(self, e):
        self.stop_button.Enable()
        self.start_button.Disable()
        jobs_model = JobsModel.readFromFile()
        if platform.system().lower() == 'windows':
            print("windows")
            cmd = "~\\AppData\\Local\\chia-blockchain\\app-?.?.?\\resources\\app.asar.unpacked\\daemon\\chia.exe"
        else:
            print("mac os")
            cmd = "/Applications/Chia.app/Contents/Resources/app.asar.unpacked/daemon/chia"
        first_job: PlotModel = jobs_model.jobs[0]
        cmd += " plots create -k " + str(first_job.k_size) + \
               " -b " + str(first_job.ram) + \
               " -n " + str(first_job.plot_total) + \
               " -r " + str(first_job.threads) + \
               " -t " + first_job.temp_dir + \
               " -d " + first_job.final_dir
        output = open('config_plot1.txt', 'w')
        out = subprocess.Popen(cmd, shell=True, stdout=output)
        print("pid:", out.pid)
