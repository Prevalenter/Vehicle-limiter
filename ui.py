import wx
import cv2
# temp=cv2.VideoCapture(0)
# ret, frame = temp.read()
# print(ret)
def camera_test(text,num):
    for i in range(num):
        temp=cv2.VideoCapture(i)
        ret, frame = temp.read()
        if ret==True:text.AppendText('摄像头'+str(i)+'已经打开\n')
        else:text.AppendText('摄像头'+str(i)+'未打开，请检查\n')

class ShowCapture(wx.Panel):
    def __init__(self, parent, capture, fps=15):
        wx.Panel.__init__(self, parent, style=wx.SUNKEN_BORDER)
        self.capture = capture
        ret, frame = self.capture.read()
        self.height, self.width = 720,626
        frame=cv2.resize(frame,(self.height,self.width))
        # frame=cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
        self.bmp = wx.Bitmap.FromBuffer(self.height,self.width, frame)
        self.timer = wx.Timer(self)
        self.timer.Start(1000./fps)
        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Bind(wx.EVT_TIMER, self.NextFrame)
        self.Bind(wx.EVT_SIZE, self.OnSize)
        
    def OnSize(self,event):
        self._Buffer = wx.Bitmap((self.height,self.width))
        self.UpdateDrawing()
        
    def OnPaint(self, evt):
        dc = wx.BufferedPaintDC(self, self._Buffer)
        self.UpdateDrawing()
    def NextFrame(self, event):
        ret, frame = self.capture.read()
        if ret:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame=cv2.resize(frame,(self.height,self.width))
            # print(frame.shape)
            self.bmp.CopyFromBuffer(frame)
            self.Refresh()
            self.UpdateDrawing()
    def UpdateDrawing(self):
        dc=wx.BufferedDC(wx.ClientDC(self), self._Buffer)
        self.Draw(dc)
    def Draw(self,dc):
        dc.DrawBitmap(self.bmp, 0, 0)
class MyFrame(wx.Frame):
    def __init__(self, parent, ID, title):
        wx.Frame.__init__(self, parent, ID, title, size=(300, 250))
        self.Maximize(True) 
        panel_text= wx.TextCtrl(self,-1,style=wx.TE_MULTILINE ,name='TextCtrlNameStr')
        camera_test(panel_text,3)
        capture0 = cv2.VideoCapture(0)
        panel_rgb= ShowCapture(self,capture0)
        panel_gray = wx.Panel(self,-1, style=wx.SUNKEN_BORDER)

        # for i in range(10):

        panel_text.AppendText("华东交通大学车辆限界测量系统V1.0\n")
        # print(panel_text.value)
        panel_rgb.SetBackgroundColour("WHITE")
        panel_gray.SetBackgroundColour("WHITE")
        panel_text.SetBackgroundColour("WHITE")

        topSizer = wx.BoxSizer(wx.VERTICAL)

        sizer1 = wx.BoxSizer(wx.HORIZONTAL)
        sizer1.Add(panel_rgb, 1, wx.EXPAND)
        sizer1.Add(panel_gray, 1, wx.EXPAND)

        topSizer.Add(sizer1,3, wx.EXPAND)
        topSizer.Add(panel_text,1, wx.EXPAND)
        # and a status bar
        self.CreateStatusBar()
        self.SetStatusText("轨道车辆运维技术与装备研究中心")
        self.makeMenuBar()
        self.SetAutoLayout(True)
        self.SetSizer(topSizer)
        self.Layout()
    def makeMenuBar(self):
        """
        A menu bar is composed of menus, which are composed of menu items.
        This method builds a set of menus and binds handlers to be called
        when the menu item is selected.
        """

        # Make a file menu with Hello and Exit items
        fileMenu = wx.Menu()
        # The "\t..." syntax defines an accelerator key that also triggers
        # the same event
        newItem = fileMenu.Append(-1, "&新建...\tCtrl-N",
                "新建限界测量工程")
        fileMenu.AppendSeparator()
        # When using a stock ID we don't need to specify the menu item's
        # label
        exitItem = fileMenu.Append(wx.ID_EXIT)

        # Now a help menu for the about item
        helpMenu = wx.Menu()
        aboutItem = helpMenu.Append(wx.ID_ABOUT)

        examMenu = wx.Menu()
        debugMenu = wx.Menu()
        demoMenu = wx.Menu()
        setMenu = wx.Menu()
        tdMenu = wx.Menu()
        inforMenu = wx.Menu()
        # Make the menu bar and add the two menus to it. The '&' defines
        # that the next letter is the "mnemonic" for the menu item. On the
        # platforms that support it those letters are underlined and can be
        # triggered from the keyboard.
        menuBar = wx.MenuBar()
        menuBar.Append(fileMenu, "&文件")
        menuBar.Append(demoMenu, "&标定")      
        menuBar.Append(setMenu, "&设置")
        menuBar.Append(tdMenu, "&三维可视化")

        menuBar.Append(examMenu, "&查看")  
        menuBar.Append(debugMenu, "&调试")
        menuBar.Append(inforMenu, "&系统信息")
        menuBar.Append(helpMenu, "&帮助")

        # Give the menu bar to the frame
        self.SetMenuBar(menuBar)

        # Finally, associate a handler function with the EVT_MENU event for
        # each of the menu items. That means that when that menu item is
        # activated then the associated handler function will be called.
        # self.Bind(wx.EVT_MENU, self.OnHello, helloItem)
        # self.Bind(wx.EVT_MENU, self.OnExit,  exitItem)
        # self.Bind(wx.EVT_MENU, self.OnAbout, aboutItem)
if __name__ == "__main__":
    app = wx.App()
    frame = MyFrame(None, -1, "华东交通大学车辆限界测量系统")
    frame.Show()
    app.MainLoop()