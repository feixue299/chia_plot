from datetime import time
import threading
import time as _time

import wx

from JobsModel import JobsModel
from PlotModel import PlotModel
from PlottingManager import start_manager, stop_manager, plotting_manager, PlottingModel


class PlottingList(wx.Panel):
    def __init__(self, parent):
        super(PlottingList, self).__init__(parent)
        self.first_launch = True

        box = wx.StaticBox(self, label="锄地列表")
        box_sizer = wx.StaticBoxSizer(box, wx.HORIZONTAL)

        self.plotting_list = wx.ListCtrl(self, -1, style=wx.LC_REPORT)
        self.plotting_list.Bind(wx.EVT_LIST_ITEM_SELECTED, self.list_ctrl_select)

        title_group = ["序号", "配置序号", "并发序号",
                       "进度", "开始时间", "结束时间", "总耗时",
                       "PID"]

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
        stop_manager()

    def start_button_click(self, e):
        self.stop_button.Enable()
        self.start_button.Disable()
        start_manager()

        if self.first_launch:
            self.first_launch = False
            b = threading.Thread(name="update_dataSource", target=self.loop_update)
            b.start()

    def loop_update(self):
        while True:
            self.update_dataSource()
            _time.sleep(5)

    def update_dataSource(self):
        print("update_dataSource")
        self.plotting_list.DeleteAllItems()
        jobs = JobsModel.readFromFile().jobs

        for plotting in plotting_manager.plottings:
            plotting: PlottingModel
            item_index = self.plotting_list \
                .InsertItem(self.plotting_list.GetItemCount(),
                            str(self.plotting_list.GetItemCount() + 1))
            print("self.plotting_list.GetItemCount():", item_index)
            job_index = 1

            # 查找配置表中序号
            for index in range(len(jobs)):
                plot_model: PlotModel = jobs[index]
                if plot_model.create_date == plotting.job.create_date:
                    job_index = index + 1
                    break

            # 查找当前并发的序号
            concurrence_index = 1
            plotting_group = plotting_manager.jobs_plotting_dict.get(plotting.job.create_date, [])
            for index in range(len(plotting_group)):
                p: PlottingModel = plotting_group[index]
                if plotting.create_time == p.create_time:
                    concurrence_index = index + 1
                    break

            create_datetime = _time.strftime('%Y-%m-%d %H:%M:%S',
                                             _time.localtime(int(plotting.create_time)))
            str_group = [str(job_index),
                         str(concurrence_index),
                         "%.3f" % (plotting.progress * 100) + "%",
                         create_datetime,
                         "",
                         "",
                         str(plotting.pid)]
            print("str_group: ", str_group)
            for column in range(len(str_group)):
                self.plotting_list.SetItem(item_index, column + 1, str_group[column])
