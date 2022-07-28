from python_ssh import ConnectAutomation
import wx

class MyFrame(wx.Frame):    
    def __init__(self):
        super().__init__(parent=None, title='studi3talternative')
        panel = wx.Panel(self)        
        my_sizer = wx.BoxSizer(wx.VERTICAL)        
        self.text_ctrl = wx.TextCtrl(panel,style=wx.TE_PASSWORD)
        my_sizer.Add(self.text_ctrl, 0, wx.ALL | wx.EXPAND, 5)        
        my_btn = wx.Button(panel, label='Copy remote to local')
        my_btn.Bind(wx.EVT_BUTTON, self.on_press)
        my_sizer.Add(my_btn, 0, wx.ALL | wx.CENTER, 5)        
        panel.SetSizer(my_sizer)        
        self.Show()

    def on_press(self, event):
        value = self.text_ctrl.GetValue()
        if not value:
            print("You didn't enter anything!")
        else:
            con=ConnectAutomation(value)
            con.ssh_connection()

if __name__ == '__main__':
    app = wx.App()
    frame = MyFrame()
    app.MainLoop()



# import wx
# ########################################################################
# class LoginDialog(wx.Dialog):
#     """"""
#     #----------------------------------------------------------------------
#     def __init__(self):
#         """Constructor"""
#         wx.Dialog.__init__(self, None, title="Login")

#         self.mainSizer = wx.BoxSizer(wx.VERTICAL)
#         btnSizer = wx.BoxSizer(wx.HORIZONTAL)

#         userLbl = wx.StaticText(self, label="Username:")
#         userTxt = wx.TextCtrl(self)
#         self.addWidgets(userLbl, userTxt)

#         passLbl = wx.StaticText(self, label="Password:")
#         passTxt = wx.TextCtrl(self, style=wx.TE_PASSWORD)
#         self.addWidgets(passLbl, passTxt)

#         okBtn = wx.Button(self, wx.ID_OK)
#         btnSizer.Add(okBtn, 0, wx.CENTER|wx.ALL, 5)
#         cancelBtn = wx.Button(self, wx.ID_CANCEL)
#         btnSizer.Add(cancelBtn, 0, wx.CENTER|wx.ALL, 5)

#         self.mainSizer.Add(btnSizer, 0, wx.CENTER)
#         self.SetSizer(self.mainSizer)

#     #----------------------------------------------------------------------
#     def addWidgets(self, lbl, txt):
#         """
#         """
#         sizer = wx.BoxSizer(wx.HORIZONTAL)
#         sizer.Add(lbl, 0, wx.ALL|wx.CENTER, 5)
#         sizer.Add(txt, 1, wx.EXPAND|wx.ALL, 5)
#         self.mainSizer.Add(sizer, 0, wx.EXPAND)

# if __name__ == "__main__":
#     app = wx.App(False)
#     dlg = LoginDialog()
#     dlg.ShowModal()
#     dlg.Destroy()
#     app.MainLoop()