import os
import platform
import re

import wx


class CreateJobs(wx.Dialog):
    def __init__(self, *args, **kwargs):
        super(CreateJobs, self).__init__(*args, **kwargs)
        self.init_ui()
        # self.SetSize((800, 600))
        self.SetTitle("新建任务")

    def init_ui(self):
        vbox = wx.BoxSizer(wx.VERTICAL)

        plot_info = PlotInfo(self)
        vbox.Add(plot_info, 0, wx.EXPAND)

        wallet = Wallet(self)
        vbox.Add(wallet, 0, wx.EXPAND)

        h_box = wx.BoxSizer(wx.HORIZONTAL)
        ok_button = wx.Button(self, label='Ok')
        close_button = wx.Button(self, label='Close')

        h_box.Add(close_button, flag=wx.LEFT, border=5)
        h_box.Add(ok_button)

        vbox.Add(h_box, flag=wx.ALIGN_CENTER | wx.TOP | wx.BOTTOM, border=10)

        self.SetSizer(vbox)

        ok_button.Bind(wx.EVT_BUTTON, self.on_close)
        close_button.Bind(wx.EVT_BUTTON, self.on_close)

        self.Fit()

    def on_close(self, e):
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


class Wallet(wx.Panel):
    def __init__(self, parent):
        super(Wallet, self).__init__(parent)

        wallet_box = wx.StaticBox(self, label="钱包信息")
        wallet_box_sizer = wx.StaticBoxSizer(wallet_box, wx.HORIZONTAL)

        wallet_text_ctrl = wx.TextCtrl(self)
        default_button = wx.Button(self, label="自动获取钱包")
        custom_button = wx.Button(self, label="选择钱包")

        default_button.Bind(wx.EVT_BUTTON, self.auto_get_wallte)

        wallet_box_sizer.Add(wallet_text_ctrl, 1, wx.EXPAND)
        wallet_box_sizer.Add(default_button, 0)
        wallet_box_sizer.Add(custom_button, 0)

        self.SetSizer(wallet_box_sizer)

    def auto_get_wallte(self, e):
        if platform.system().lower() == 'windows':
            print("windows")
            cmd = "~\\AppData\\Local\\chia-blockchain\\app-?.?.?\\resources\\app.asar.unpacked\\daemon\\chia.exe" \
                  "keys show"
        else:
            print("mac os")
            cmd = "/Applications/Chia.app/Contents/Resources/app.asar.unpacked/daemon/chia keys show"
        cmd_resp = os.popen(cmd)
        read = cmd_resp.read()
        match_object = re.match(r'Farmer public key (.*)', read, re.M | re.I)
        if match_object:
            print("matchObj.group() : ", match_object.group())
            print("matchObj.group(1) : ", match_object.group(1))
            print("matchObj.group(2) : ", match_object.group(2))
        else:
            print("no match")
