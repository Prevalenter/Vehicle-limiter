# import menus
import os
import wx
# from ui import *
path='menus'
def buildItem(parent, menus_root, item):
    if item=='-':
        menus_root.AppendSeparator()
        return
    for i in item.menus:
        # print(i.string)
        mi = wx.MenuItem(menus_root, -1, i.string,i.statustext)
        parent.Bind(wx.EVT_MENU, lambda x, p=i:p().start(parent,None), mi)
        menus_root.Append(mi)
        del mi
def buildMenu(parent, data):
    menu = wx.Menu()
    for i in data:
        buildItem(parent, menu, i)
    return menu
def buildMenuBar(parent, data, menuBar=None):
    if menuBar==None:
        menuBar = wx.MenuBar()
    #这一层是在不同文件夹中，即顶级目录
    for item in data:
        #创建一个。py文件的目录条
        menuBar.Append(buildMenu(parent,data[item][:-1]), data[item][-1])
    return menuBar
def buildMenuBarByPath(parent=None,rootDir='menus'):
    menutree={}
    menubarlist=[]
    pg=__import__(rootDir,'','',[''])
    for filename in pg.catlog:
    # for filename in os.listdir(rootDir):
        # if filename=='__pycache__':continue
        pathname = os.path.join(rootDir, filename)
        if os.path.isdir(pathname):
            rpath = pathname.replace('/', '.').replace('\\','.')
            pg = __import__(rpath,'','',[''])
            pg.title = os.path.basename(path)
            if hasattr(pg, 'catlog'):
                menutree[filename]=[]
                for i in pg.catlog:
                    pg1 = __import__('menus.'+filename+'.'+i,'','',[''])
                    menutree[filename].append(pg1)
                menutree[filename].append(pg.name)
    parent.SetMenuBar(buildMenuBar(parent,menutree))
class HelloFrame(wx.Frame):
    def __init__(self, *args, **kw):
        # ensure the parent's __init__ is called
        super(HelloFrame, self).__init__(*args, **kw)
        pnl = wx.Panel(self)
        st = wx.StaticText(pnl, label="Hello World!", pos=(25,25))
        font = st.GetFont()
        font.PointSize += 10
        font = font.Bold()
        st.SetFont(font)
        # self.makeMenuBar()
        buildMenuBarByPath(self)
        self.CreateStatusBar()
        self.SetStatusText("Welcome to wxPython!")
if __name__ == "__main__":
    app = wx.App()
    frm = HelloFrame(None, title="Hello World")
    frm.Show()
    # pd = NewTool()
    # pd.start(frm,None)
    app.MainLoop()


