# -*- coding: utf-8 -*-
# ConfigPanel used for parameters setting
import wx, platform

class NumCtrl(wx.TextCtrl):
    """NumCtrl: diverid from wx.core.TextCtrl """
    def __init__(self, parent, rang, accury):
        wx.TextCtrl.__init__(self, parent, wx.TE_RIGHT)
        self.min, self.max = rang
        self.accury = accury
        wx.TextCtrl.Bind(self, wx.EVT_KEY_UP, self.ontext)
        
    #! TODO: what is this?
    def Bind(self, z, f):
        self.f = f
        
    def ontext(self, event):
        self.f(event)
        if self.GetValue()==None:
            self.SetBackgroundColour((255,255,0))
        else:
            self.SetBackgroundColour((255,255,255))
        
    def SetValue(self, n):
        wx.TextCtrl.SetValue(self, str(round(n,self.accury) if self.accury>0 else int(n)))
        
    def GetValue(self):
        sval = wx.TextCtrl.GetValue(self)
        try:
            num = float(sval) if self.accury>0 else int(sval)
        except ValueError:
            return None
        if num<self.min or num>self.max:
            return None
        if abs(round(num, self.accury) - num) > 1E-5:
            return None
        return num

class ParaDialog (wx.Dialog):
    def __init__( self, parent, title):
        wx.Dialog.__init__ (self, parent, -1, title, style = wx.DEFAULT_DIALOG_STYLE)
        self.lst = wx.BoxSizer( wx.VERTICAL )
        self.tus = []
        self.funcs = {int:self.add_num,  float:self.add_num, 'lab':self.add_lab, bool:self.add_check,
                      str:self.add_txt, list:self.add_choice, 'color':self.add_color}

        self.on_ok, self.on_cancel = None, None
        self.ctrl_dic = {}
        boxBack = wx.BoxSizer()
        boxBack.Add(self.lst, 0, wx.ALL, 10)
        self.SetSizer( boxBack )
        self.Layout()
        self.handle = self.handle_

    def commit(self, state):
        self.Destroy()
        if state=='ok' and self.on_ok:self.on_ok()
        if state=='cancel' and self.on_cancel:self.on_cancel()

    def add_confirm(self, modal=True):
        self.lst.AddStretchSpacer(1)
        sizer = wx.BoxSizer( wx.HORIZONTAL )
        self.btn_OK = wx.Button( self, wx.ID_OK, 'OK')
        sizer.Add( self.btn_OK, 0, wx.ALIGN_RIGHT|wx.ALL, 5 )

        self.btn_cancel = wx.Button( self, wx.ID_CANCEL, 'Cancel')
        sizer.Add( self.btn_cancel, 0, wx.ALIGN_RIGHT|wx.ALL, 5 )
        self.lst.Add(sizer, 0, wx.ALIGN_RIGHT, 5 )
        if not modal:
            self.btn_OK.Bind( wx.EVT_BUTTON, lambda e:self.commit('ok'))
            self.btn_cancel.Bind( wx.EVT_BUTTON, lambda e:self.commit('cancel'))

    def init_view(self, items, para, preview=False, modal = True):
        self.para = para
        for item in items:
            self.funcs[item[0]](*item[1:])
        if preview:self.add_check('Preview', 'preview')
        self.reset(para)
        self.add_confirm(modal)
        self.pack()

    def parse(self, para) :
        self.funcs[para[0]](*para[1:])

    def add_ctrl(self, key, ctrl):
        self.lst.Add( ctrl, 0, wx.EXPAND, 5 )
        if not key is None:
            self.ctrl_dic[key] = ctrl
            if hasattr(ctrl, 'set_handle'):
                ctrl.set_handle(lambda x=None : self.para_changed(key))


    def add_num(self, rang, accu, title, key, unit):
        sizer = wx.BoxSizer( wx.HORIZONTAL )
        lab_title = wx.StaticText( self, wx.ID_ANY, title,
                                  wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_CENTRE )

        lab_title.Wrap( -1 )
        sizer.Add( lab_title, 0, wx.ALIGN_CENTER|wx.ALL, 5 )
        ctrl = NumCtrl(self, rang, accu)
        self.ctrl_dic[key] = ctrl
        ctrl.Bind(wx.EVT_KEY_UP, lambda x : self.para_changed(key))
        sizer.Add( ctrl, 2, wx.ALL, 5 )

        lab_unit = wx.StaticText( self, wx.ID_ANY, unit,
                                  wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_CENTRE )

        lab_unit.Wrap( -1 )
        sizer.Add( lab_unit, 0, wx.ALIGN_CENTER|wx.ALL, 5 )
        self.tus.append((lab_title, lab_unit))
        self.lst.Add( sizer, 0, wx.EXPAND, 5 )

    def add_color(self, title, key, unit):
        sizer = wx.BoxSizer( wx.HORIZONTAL )
        lab_title = wx.StaticText( self, wx.ID_ANY, title,
                                   wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_CENTRE )

        lab_title.Wrap( -1 )
        sizer.Add( lab_title, 0, wx.ALIGN_CENTER|wx.ALL, 5 )
        ctrl = ColorCtrl(self)
        self.ctrl_dic[key] = ctrl
        ctrl.Bind(wx.EVT_KEY_UP, lambda x : self.para_changed(key))
        sizer.Add( ctrl, 2, wx.ALL, 5 )

        lab_unit = wx.StaticText( self, wx.ID_ANY, unit,
                                  wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_CENTRE )

        lab_unit.Wrap( -1 )
        sizer.Add( lab_unit, 0, wx.ALIGN_CENTER|wx.ALL, 5 )
        self.tus.append((lab_title, lab_unit))
        self.lst.Add( sizer, 0, wx.EXPAND, 5 )

    def add_choice(self, choices, tp, title, key, unit):
        sizer = wx.BoxSizer( wx.HORIZONTAL )
        lab_title = wx.StaticText( self, wx.ID_ANY, title,
                                   wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_CENTRE )

        lab_title.Wrap( -1 )
        sizer.Add( lab_title, 0, wx.ALIGN_CENTER|wx.ALL, 5 )

        ctrl = wx.Choice( self, wx.ID_ANY,
                          wx.DefaultPosition, wx.DefaultSize,
                          [str(choice) for choice in choices], 0 )

        ctrl.SetSelection(0)
        ctrl.SetValue = lambda x:ctrl.SetSelection(choices.index(x))
        ctrl.GetValue = lambda : tp(choices[ctrl.GetSelection()])
        self.ctrl_dic[key] = ctrl
        ctrl.Bind( wx.EVT_CHOICE, lambda x : self.para_changed(key))
        sizer.Add( ctrl, 2, wx.ALL, 5 )

        lab_unit = wx.StaticText( self, wx.ID_ANY, unit,
                                  wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_CENTRE )

        lab_unit.Wrap( -1 )
        sizer.Add( lab_unit, 0, wx.ALIGN_CENTER|wx.ALL, 5 )
        self.tus.append((lab_title, lab_unit))
        self.lst.Add( sizer, 0, wx.EXPAND, 5 )

    def add_lab(self, cont):
        sizer = wx.BoxSizer( wx.HORIZONTAL )
        ctrl = wx.StaticText( self, wx.ID_ANY, cont, wx.DefaultPosition, wx.DefaultSize)
        sizer.Add( ctrl, 2, wx.ALL, 5 )
        self.lst.Add( sizer, 0, wx.EXPAND, 5)

    def add_txt(self, title, key, unit):
        sizer = wx.BoxSizer( wx.HORIZONTAL )
        lab_title = wx.StaticText( self, wx.ID_ANY, title,
                                   wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_CENTRE )

        lab_title.Wrap( -1 )
        sizer.Add( lab_title, 0, wx.ALIGN_CENTER|wx.ALL, 5 )

        ctrl = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString,
                            wx.DefaultPosition, wx.DefaultSize, 0 )

        self.ctrl_dic[key] = ctrl
        ctrl.Bind( wx.EVT_KEY_UP, lambda x : self.para_changed(key))
        sizer.Add( ctrl, 2, wx.ALL, 5 )

        lab_unit = wx.StaticText( self, wx.ID_ANY, unit,
                                  wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_CENTRE )

        lab_unit.Wrap( -1 )
        sizer.Add( lab_unit, 0, wx.ALIGN_CENTER|wx.ALL, 5 )
        self.tus.append((lab_title, lab_unit))
        self.lst.Add( sizer, 0, wx.EXPAND, 5 )

    def add_check(self, title, key):
        box = wx.BoxSizer(wx.HORIZONTAL)
        check = wx.CheckBox(self, -1, title)
        self.ctrl_dic[key] = check
        check.Bind(wx.EVT_CHECKBOX, lambda x : self.para_changed(key))
        box.Add(check, 1, wx.ALL, 5)
        self.lst.Add(box)

    def pack(self):
        mint, minu = [], []
        for t,u in self.tus:
            mint.append(t.GetSize()[0])
            minu.append(u.GetSize()[0])
        for t,u in self.tus:
            t.SetInitialSize((max(mint),-1))
            u.SetInitialSize((max(minu),-1))
        self.Fit()

    def para_changed(self, key):

        para = self.para
        for p in list(para.keys()):
            if p in self.ctrl_dic:
                para[p] = self.ctrl_dic[p].GetValue()
        #self.para_check(para, key)
        sta = sum([i is None for i in list(para.values())])==0
        self.btn_OK.Enable(sta)
        if not sta: return
        if 'preview' not in self.ctrl_dic:return
        if not self.ctrl_dic['preview'].GetValue():return
        self.handle(para)

    def reset(self, para=None):
        if para!=None:self.para = para
        for p in list(self.para.keys()):
            if p in self.ctrl_dic:
                self.ctrl_dic[p].SetValue(self.para[p])

    def get_para(self):
        return self.para

    def set_handle(self, handle):
        self.handle = handle
        if handle==None: self.handle = self.handle_

    def handle_(self, para):
        print(para)

    def __del__( self ):
        pass

if __name__ == '__main__':
    view = [(float, (0,20), 1, '半径', 'r', 'mm'),
            ('slide', (-20,20), '亮度', 'slide', 'mm'),
            ('color', '颜色', 'color', 'rgb'),
            (bool, 'Preview', 'preview')]
    data = {'r':1.2, 'slide':0,  'preview':True, 'color':(0,255,0)}

    app = wx.PySimpleApp()
    pd = ParaDialog(None, 'Test')
    pd.init_view(view, para)
    pd.pack()
    pd.ShowModal()
    app.MainLoop()
