import wx


class Jobs(wx.Panel):
    def __init__(self, parent):
        super().__init__(parent)

        jobs_box = wx.StaticBox(self, label="任务列表")
        jobs_box_sizer = wx.StaticBoxSizer(jobs_box, wx.HORIZONTAL)

        h_box = wx.BoxSizer(wx.HORIZONTAL)
        job_list = wx.ListCtrl(self, -1, style=wx.LC_REPORT)
        h_box.Add(job_list, 1)

        v_box = wx.BoxSizer(wx.VERTICAL)
        self.create_button = wx.Button(self, label="新建任务")
        self.delete_button = wx.Button(self, label="删除任务")
        v_box.Add(self.create_button)
        v_box.Add(self.delete_button)
        h_box.Add(v_box, 0, wx.ALIGN_CENTER_VERTICAL)

        jobs_box_sizer.Add(h_box, 1, wx.EXPAND)

        self.SetSizer(jobs_box_sizer)
