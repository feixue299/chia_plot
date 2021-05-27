import sys

import wx


class CreateJobs(wx.Dialog):
    def __init__(self, *args, **kwargs):
        super(CreateJobs, self).__init__(*args, **kwargs)
        self.init_ui()
        self.SetSize((800, 600))
        self.SetTitle("新建任务")

    def init_ui(self):
        vbox = wx.BoxSizer(wx.VERTICAL)

        plot_info = PlotInfo(self)
        vbox.Add(plot_info, flag=wx.ALIGN_CENTER)

        h_box = wx.BoxSizer(wx.HORIZONTAL)
        ok_button = wx.Button(self, label='Ok')
        close_button = wx.Button(self, label='Close')

        h_box.Add(close_button, flag=wx.LEFT, border=5)
        h_box.Add(ok_button)

        vbox.Add(h_box, flag=wx.ALIGN_CENTER | wx.TOP | wx.BOTTOM, border=10)

        self.SetSizer(vbox)

        ok_button.Bind(wx.EVT_BUTTON, self.OnClose)
        close_button.Bind(wx.EVT_BUTTON, self.OnClose)

    def OnClose(self, e):
        self.Close()


class PlotInfo(wx.Panel):
    def __init__(self, parent):
        super().__init__(parent)

        plot_box = wx.StaticBox(self, label="锄地信息")
        plot_box_sizer = wx.StaticBoxSizer(plot_box, wx.HORIZONTAL)

        grid_box = wx.GridSizer(2, 4, 5, 5)

        title_group = ["锄地总数", "总P盘总数", "启动间隔"]

        for title in title_group:
            text = wx.StaticText(self, label=title)
            text_ctrl = wx.TextCtrl(self)
            grid_box.Add(text)
            grid_box.Add(text_ctrl)

        time_radio_button = wx.RadioButton(self, label="时间间隔(分钟)")
        progress_radio_button = wx.RadioButton(self, label="进度间隔(%)")

        grid_box.Add(time_radio_button)
        grid_box.Add(progress_radio_button)

        plot_box_sizer.Add(grid_box)
        self.SetSizer(plot_box_sizer)

    def on_radio_group(self, e):
        pass
