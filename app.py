import wx

from ChiaCommand import ChiaCommand
from Jobs import Jobs
from PlottingList import PlottingList
from PlottingManager import PlottingManager


class Panel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent=parent, id=-1)

        v_box = wx.BoxSizer(wx.VERTICAL)

        jobs_panel = Jobs(self)
        v_box.Add(jobs_panel, 0, wx.EXPAND)

        plotting = PlottingList(self)
        v_box.Add(plotting, 0, wx.EXPAND)

        self.SetSizer(v_box)


class Frame(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, parent=None, title=u'chia', size=(1000, 600),
                          style=wx.DEFAULT_FRAME_STYLE ^ wx.MAXIMIZE_BOX)
        panel = Panel(self)
        self.Centre()
        panel.Fit()
        self.Show()


class App(wx.App):
    def OnInit(self):
        frame = Frame()
        frame.Show()
        self.SetTopWindow(frame)
        return True


if __name__ == '__main__':
    app = App()
    PlottingManager.createManager()
    app.MainLoop()
