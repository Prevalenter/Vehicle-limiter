from config import *
class newui(ParaDialog):
    def __init__( self, parent, title):
        setui.__init__(self, parent, title)
        self.view+=[(bool, 'Preview', 'preview') ]
        self.arg_buf=self.data.copy()
        self.init_view(self.view, self.data,modal=False)
        self.pack()
        self.ShowModal()
    def handle_(self,para):
        setui.handle_(self,para)
        self.rect.GetOnRectsize()
        self.rect.parent.UpdateDrawing()
if __name__ == '__main__':
    app = wx.PySimpleApp()
    pd = newui(None, '设置')
    pd.pack()
    pd.ShowModal()
    app.MainLoop()