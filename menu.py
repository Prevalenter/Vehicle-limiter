# from config import ParaDialog
import wx
# from ui import MyFrame
# class newui(ParaDialog):
#     def __init__( self, parent, title):
#         ParaDialog.__init__(self, parent, title)
#         self.view=[(bool, 'Preview', 'preview') ]
#         # self.arg_buf=self.data.copy()
#         # self.init_view(self.view, self.data,modal=False)
#         self.pack()
#         self.ShowModal()
#     def handle_(self,para):
#         pass
class Tool:
    title = 'title'
    para = None
    view = None
    def preview(self, parent, doc, para=None):
        self.run(parent, doc, para)
        parent.update()

    def show(self, parent, doc):
        self.dialog = ParaDialog(parent, self.title)
        self.dialog.init_view(self.view, self.para, True)
        self.dialog.set_handle(lambda x:self.preview(parent,  doc, self.para))

        if self.dialog.ShowModal() == wx.ID_OK:
            self.run(parent, doc, self.para)
            parent.update()
        self.dialog.Destroy()
    def start(self, parent, doc):
        if self.para is None:
            self.run(parent, doc, None)
            parent.update()
        else:
            self.show(parent, doc)
class NewTool(Tool):
    para = {'w':300, 'h':512}
    view = [(int, (100,1000), 0, 'width', 'w', 'pix'),
            (int, (100,1000), 0, 'height', 'h', 'pix')]
    # img = '../imgdata/new.png'
    title = '新建限界'
    def run(self, parent, doc, para):
        parent.doc = Doc()
        parent.doc.para = {'w':para['w'], 'h':para['h']}
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