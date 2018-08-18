import sys
sys.path.append('..')
from ..config import Tool
import wx
# from ui import MyFrame

class NewTool(Tool):
    para = {'w':300, 'h':512}
    view = [(int, (100,1000), 0, 'width', 'w', 'pix'),
            (int, (100,1000), 0, 'height', 'h', 'pix')]
    # img = '../imgdata/new.png'
    title = '新建限界'
    string="&新建...\tCtrl-N"
    def run(self, parent, doc, para):
        print('you did it')
        # parent.canvas.Zoom(1/parent.canvas.Scale, 
        #     (para['w']//2, -para['h']//2))
menus = [NewTool]

if __name__ == '__main__':
    app = wx.App(False)
    mainFrame = MyFrame(None, -1, "华东交通大学车辆限界测量系统")
    mainFrame.Show()
    pd = NewTool()
    pd.start(mainFrame,None)
    # pd.pack()
    pd.ShowModal()
    app.MainLoop()