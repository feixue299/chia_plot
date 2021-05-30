import os
import platform
import re

import wx

from PlotModel import PlotModel, ProgressInterval, TimeInterval


class CreateJobs(wx.Dialog):
    def __init__(self, *args, **kwargs):
        super(CreateJobs, self).__init__(*args, **kwargs)
        self.model = PlotModel()
        self.SetTitle("新建任务")

        vbox = wx.BoxSizer(wx.VERTICAL)

        self.plot_info = PlotInfo(self)
        vbox.Add(self.plot_info, 0, wx.EXPAND)

        self.wallet = Wallet(self)
        vbox.Add(self.wallet, 0, wx.EXPAND)

        self.plot_parameter = PlottingParameters(self)
        vbox.Add(self.plot_parameter, 0, wx.EXPAND)

        self.directories = Directories(self)
        vbox.Add(self.directories, 0, wx.EXPAND)

        h_box = wx.BoxSizer(wx.HORIZONTAL)
        ok_button = wx.Button(self, label='Ok')
        close_button = wx.Button(self, label='Close')

        h_box.Add(close_button, flag=wx.LEFT, border=5)
        h_box.Add(ok_button)

        vbox.Add(h_box, flag=wx.ALIGN_CENTER | wx.TOP | wx.BOTTOM, border=10)

        self.SetSizer(vbox)

        ok_button.Bind(wx.EVT_BUTTON, self.on_ok)
        close_button.Bind(wx.EVT_BUTTON, self.on_close)

        self.Fit()

    def on_close(self, e):
        self.Close()

    def on_ok(self, e):
        try:
            self.model.plot_total = int(self.plot_info.plot_total_text_ctrl.Value)
            self.model.plotting_number = int(self.plot_info.plotting_total_text_ctrl.Value)
            self.model.launch_interval = int(self.plot_info.launch_interval_text_ctrl.Value)
            self.model.interval_type = TimeInterval if self.plot_info.time_radio_button.Value else ProgressInterval
            if self.model.check():
                wx.MessageBox("提示", "信息完整", wx.OK | wx.ICON_INFORMATION)
            else:
                wx.MessageBox("提示", "信息不完整", wx.OK | wx.ICON_INFORMATION)
        except ValueError as error:
            wx.MessageBox("提示", str(error), wx.OK | wx.ICON_INFORMATION)


class PlotInfo(wx.Panel):
    def __init__(self, parent):
        super().__init__(parent)

        plot_box = wx.StaticBox(self, label="锄地信息")
        plot_box_sizer = wx.StaticBoxSizer(plot_box, wx.HORIZONTAL)

        grid_box = wx.GridSizer(2, 4, 5, 5)

        text = wx.StaticText(self, label="锄地总数")
        self.plot_total_text_ctrl = wx.TextCtrl(self)
        grid_box.Add(text)
        grid_box.Add(self.plot_total_text_ctrl)

        text = wx.StaticText(self, label="总P盘总数")
        self.plotting_total_text_ctrl = wx.TextCtrl(self)
        grid_box.Add(text)
        grid_box.Add(self.plotting_total_text_ctrl)

        text = wx.StaticText(self, label="启动间隔")
        self.launch_interval_text_ctrl = wx.TextCtrl(self)
        grid_box.Add(text)
        grid_box.Add(self.launch_interval_text_ctrl)

        self.time_radio_button = wx.RadioButton(self, label="时间间隔(分钟)")
        self.progress_radio_button = wx.RadioButton(self, label="进度间隔(%)")

        grid_box.Add(self.time_radio_button)
        grid_box.Add(self.progress_radio_button)

        plot_box_sizer.Add(grid_box)
        self.SetSizer(plot_box_sizer)


class Wallet(wx.Panel):
    def __init__(self, parent):
        super(Wallet, self).__init__(parent)

        wallet_box = wx.StaticBox(self, label="钱包信息")
        wallet_box_sizer = wx.StaticBoxSizer(wallet_box, wx.HORIZONTAL)

        title_v_box = wx.BoxSizer(wx.VERTICAL)

        for title in ["指纹:", "农场公钥:", "矿池公钥:"]:
            text = wx.StaticText(self, label=title)
            title_v_box.Add(text, 0)

        text_ctrl_v_box = wx.BoxSizer(wx.VERTICAL)
        self.finger_text_ctrl = wx.TextCtrl(self)
        self.farmer_text_ctrl = wx.TextCtrl(self)
        self.pool_text_ctrl = wx.TextCtrl(self)

        text_ctrl_v_box.Add(self.finger_text_ctrl, 1, wx.EXPAND)
        text_ctrl_v_box.Add(self.farmer_text_ctrl, 1, wx.EXPAND)
        text_ctrl_v_box.Add(self.pool_text_ctrl, 1, wx.EXPAND)

        v_box = wx.BoxSizer(wx.VERTICAL)
        default_button = wx.Button(self, label="自动获取钱包")
        custom_button = wx.Button(self, label="选择钱包")

        default_button.Bind(wx.EVT_BUTTON, self.auto_get_wallte)

        v_box.Add(default_button)
        v_box.Add(custom_button)

        wallet_box_sizer.Add(title_v_box, 0)
        wallet_box_sizer.Add(text_ctrl_v_box, 1, wx.EXPAND)
        wallet_box_sizer.Add(v_box, 0)

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
        finger_print = re.search('Fingerprint: (.*)', read)
        farmer_key = re.search('Farmer public key (.*): (.*)', read)
        pool_key = re.search('Pool public key (.*): (.*)', read)

        if finger_print:
            print("Fingerprint:", finger_print.group(1))
            self.finger_text_ctrl.SetLabel(finger_print.group(1))
        if farmer_key:
            print("Farmer public key:", farmer_key.group(2))
            self.farmer_text_ctrl.SetLabel(farmer_key.group(2))
        if pool_key:
            print("Pool public key:", pool_key.group(2))
            self.pool_text_ctrl.SetLabel(pool_key.group(2))


class PlottingParameters(wx.Panel):
    def __init__(self, parent):
        super(PlottingParameters, self).__init__(parent)

        plot_parameter_box = wx.StaticBox(self, label="配置信息")
        plot_parameter_box_sizer = wx.StaticBoxSizer(plot_parameter_box, wx.HORIZONTAL)

        grid_box = wx.GridSizer(2, 4, 5, 5)

        k_size = wx.StaticText(self, label="K-size")
        k_text_ctrl = wx.TextCtrl(self, value="32", style=wx.TE_READONLY)

        grid_box.Add(k_size)
        grid_box.Add(k_text_ctrl)

        ram = wx.StaticText(self, label="Ram(Mib)")
        ram_text_ctrl = wx.TextCtrl(self, value="3390")

        grid_box.Add(ram)
        grid_box.Add(ram_text_ctrl)

        threads = wx.StaticText(self, label="线程数")
        threads_text_ctrl = wx.TextCtrl(self, value="2")

        grid_box.Add(threads)
        grid_box.Add(threads_text_ctrl)

        plot_parameter_box_sizer.Add(grid_box, 1, wx.EXPAND)

        self.SetSizer(plot_parameter_box_sizer)


class Directories(wx.Panel):
    def __init__(self, parent):
        super(Directories, self).__init__(parent)

        box = wx.StaticBox(self, label="目录设置")
        sizer = wx.StaticBoxSizer(box, wx.HORIZONTAL)

        grid = wx.FlexGridSizer(2, 3, 5, 5)

        temp_text = wx.StaticText(self, label="临时目录")
        self.temp_text_ctrl = wx.TextCtrl(self)
        temp_button = wx.Button(self, label="选择目录")
        temp_button.Bind(wx.EVT_BUTTON, self.select_temp)

        grid.Add(temp_text)
        grid.Add(self.temp_text_ctrl, 1, wx.EXPAND)
        grid.Add(temp_button)

        final_text = wx.StaticText(self, label="最终目录")
        self.final_text_ctrl = wx.TextCtrl(self)
        final_button = wx.Button(self, label="选择目录")
        final_button.Bind(wx.EVT_BUTTON, self.select_final)

        grid.Add(final_text)
        grid.Add(self.final_text_ctrl, 1, wx.EXPAND)
        grid.Add(final_button)

        grid.AddGrowableCol(1, 1)

        sizer.Add(grid, 1, wx.EXPAND)

        self.SetSizer(sizer)

    def select_temp(self, e):
        label = self.select_dir()
        self.temp_text_ctrl.SetLabel(label)

    def select_final(self, e):
        label = self.select_dir()
        self.final_text_ctrl.SetLabel(label)

    def select_dir(self):
        dir_dialog = wx.DirDialog(self, "选择文件夹", style=wx.DD_DEFAULT_STYLE)
        dir_dialog.ShowModal()
        return dir_dialog.GetPath()
