import sys
import cv2
sys.path.append('..')
from ..config import Tool
import wx
from VideoCapture import Device
class ShowCapture(wx.Panel):
    def __init__(self, parent, capture, fps=30):
        wx.Panel.__init__(self, parent, style=wx.SUNKEN_BORDER)
        self.SetDoubleBuffered(True)
        self.capture = capture
        ret, frame = self.capture.read()
        self.height, self.width = 480,417
        self._Buffer = wx.Bitmap((self.height,self.width))
        frame=cv2.resize(frame,(self.height,self.width))
        self.bmp = wx.Bitmap.FromBuffer(self.height,self.width, frame)
        self.timer = wx.Timer(self)
        self.timer.Start(1000./fps)

        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Bind(wx.EVT_TIMER, self.NextFrame)
        self.Bind(wx.EVT_SIZE, self.OnSize)
    def OnSize(self,event):
        self._Buffer = wx.Bitmap((self.height,self.width))
    def OnPaint(self, evt):
        dc = wx.BufferedPaintDC(self, self._Buffer)
    def NextFrame(self, event):
        ret, frame = self.capture.read()
        if ret:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame=cv2.resize(frame,(self.height,self.width))
            self.bmp.CopyFromBuffer(frame)
            self.UpdateDrawing()
            self.Refresh()
    def UpdateDrawing(self):
        dc=wx.BufferedDC(wx.ClientDC(self), self._Buffer)
        self.Draw(dc)
    def Draw(self,dc):
        dc.DrawBitmap(self.bmp, 0, 0)
class TabOne(wx.Panel):
    """docstring for TabOne"""
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        self.parent = parent
        campanellst=[]
        topsizer = wx.BoxSizer(wx.VERTICAL)
        horisizer1 = wx.BoxSizer(wx.HORIZONTAL)
        campanellst.append(ShowCapture(self,cv2.VideoCapture(0)))
        horisizer1.Add(campanellst[0],3, wx.EXPAND)
        horisizer1.Add(wx.Button(self, -1, "按钮4"),3, wx.EXPAND)
        horisizer1.Add(wx.Button(self, -1, "按钮4"),3, wx.EXPAND)

        horisizer2 = wx.BoxSizer(wx.HORIZONTAL)
        horisizer2.Add(wx.Button(self, -1, "按钮4"),3, wx.EXPAND)
        horisizer2.Add(wx.Button(self, -1, "按钮4"),3, wx.EXPAND)
        horisizer2.Add(wx.Button(self, -1, "按钮4"),3, wx.EXPAND)

        topsizer.Add(horisizer1,2, wx.EXPAND)
        topsizer.Add(horisizer2,2, wx.EXPAND)

        self.SetAutoLayout(True)
        self.SetSizer(topsizer)
        self.Layout()
class TabTwo(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        # t = wx.StaticText(self, -1, "This is the third tab", (20,20))
        horisizer1 = wx.BoxSizer(wx.HORIZONTAL)
        horisizer1.Add(wx.Button(self, -1, "按钮4"),3, wx.EXPAND)
        horisizer1.Add(wx.Button(self, -1, "按钮4"),3, wx.EXPAND)
        self.SetAutoLayout(True)
        self.SetSizer(horisizer1)
        self.Layout() 
class TabFour(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        t = wx.StaticText(self, -1, "This is the last tab", (20,20))
class NewTool(Tool):
    camlist=Device().getDisplayName().split(',')
    para = {'w':300, 'cam':camlist[0]}
    view = [(int, (100,1000), 0, 'width', 'w', 'pix'),
            (list, camlist, str, 'cam', 'cam', 'cam')]
    string="&新建...\tCtrl-N"
    statustext = '新建限界'
    def run(self, parent, doc, para):

        nb = wx.Notebook(parent.win_panel)

        tab=TabOne(nb)
        tab1=TabTwo(nb)
        tab2=TabFour(nb)

        nb.AddPage(tab, "各点位")
        nb.AddPage(tab1, "融合整体")
        nb.AddPage(tab2, "Tab 3")

        sizer = wx.BoxSizer()
        sizer.Add(nb, 1, wx.EXPAND)
        parent.win_panel.SetSizer(sizer)
        parent.Maximize(False) 
        parent.Maximize(True)
        parent.win_panel.Refresh()

menus = [NewTool]

if __name__ == '__main__':
    app = wx.App(False)
    mainFrame = MyFrame(None, -1, "华东交通大学车辆限界测量系统")
    mainFrame.Show()
    pd = NewTool()
    pd.start(mainFrame,None)
    pd.ShowModal()
    app.MainLoop()