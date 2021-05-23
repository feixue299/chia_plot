import wx


def load(event):
    file = open(fileName.GetValue())
    fileContent.SetValue(file.read())
    file.close()


def save(event):
    file = open(fileName.GetValue(), 'w')
    file.write(fileContent.GetValue())
    file.close()


app = wx.App()
win = wx.Frame(None, title="Chia Plot")
win.Show()

openButton = wx.Button(win, label='Open', pos=(225, 5), size=(80, 25))
openButton.Bind(wx.EVT_BUTTON, load)
saveButton = wx.Button(win, label='Save', pos=(315, 5), size=(80, 25))
saveButton.Bind(wx.EVT_BUTTON, save)

fileName = wx.TextCtrl(win, pos=(5, 5), size=(210, 25))
fileContent = wx.TextCtrl(win, pos=(5, 35), size=(390, 260), style=wx.TE_MULTILINE | wx.HSCROLL)


app.MainLoop()
