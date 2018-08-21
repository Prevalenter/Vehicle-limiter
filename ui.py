import wx
from VideoCapture import Device
from menu import NewTool
from menusloader import buildMenuBarByPath
class MyFrame(wx.Frame):
    def __init__(self, parent, ID, title):
        wx.Frame.__init__(self, parent, ID, title, size=(300, 250))
        self.Maximize(True) 
        buildMenuBarByPath(self)
        self.panel_text= wx.TextCtrl(self,-1,style=wx.TE_MULTILINE ,name='TextCtrlNameStr')
        self.win_panel=wx.Panel(self,-1, style=wx.SUNKEN_BORDER)
        self.panel_text.AppendText("华东交通大学车辆限界测量系统V1.0\n")
        self.panel_text.SetBackgroundColour("WHITE")
        self.win_panel.SetBackgroundColour("WHITE")
        topSizer = wx.BoxSizer(wx.VERTICAL)
        sizer1 = wx.BoxSizer(wx.HORIZONTAL)
        topSizer.Add(self.win_panel,6, wx.EXPAND)
        topSizer.Add(self.panel_text,1, wx.EXPAND)

        self.CreateStatusBar()
        self.SetStatusText("轨道车辆运维技术与装备研究中心")

        self.SetAutoLayout(True)
        self.SetSizer(topSizer)
        self.Layout()
        self.SetStatusText("系统初始化完成")
    def OnNew(self,event):
        pd = NewTool()
        pd.start(self,None)
        # print('ok')
if __name__ == "__main__":
    app = wx.App(False)
    mainFrame = MyFrame(None, -1, "华东交通大学车辆限界测量系统")
    mainFrame.Show()
    app.MainLoop()