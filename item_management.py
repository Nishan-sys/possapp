import wx
from main_cat_dialog import MyDialog
class MainCategoryFrame(wx.Dialog):
    def __init__(self):
        super().__init__(None, title="Main Category Management", size=(300, 200))
        panel = wx.Panel(self)
        label = wx.StaticText(panel, label="Main Category Management Window", pos=(50, 80))

class SubCategoryFrame(wx.Dialog):
    def __init__(self):
        super().__init__(None, title="Sub Category Management", size=(300, 200))
        panel = wx.Panel(self)
        label = wx.StaticText(panel, label="Sub Category Management Window", pos=(50, 80))

class FinalItemFrame(wx.Dialog):
    def __init__(self):
        super().__init__(None, title="Final Item", size=(300, 200))
        panel = wx.Panel(self)
        label = wx.StaticText(panel, label="Final Item Window", pos=(50, 80))

class OpenWindowsDialog(wx.Dialog):
    def __init__(self,parent=None):
        super().__init__(None, title="Open Windows Dialog", size=(320, 180))
        panel = wx.Panel(self)

        # Buttons for opening windows
        btn_main_cat = wx.Button(panel, label="Main Category Management", pos=(40, 20), size=(240, 30))
        btn_sub_cat = wx.Button(panel, label="Sub Category Management", pos=(40, 60), size=(240, 30))
        btn_final_item = wx.Button(panel, label="Final Item", pos=(40, 100), size=(240, 30))

        # Bind button events
        btn_main_cat.Bind(wx.EVT_BUTTON, self.on_open_main_category)
        btn_sub_cat.Bind(wx.EVT_BUTTON, self.on_open_sub_category)
        btn_final_item.Bind(wx.EVT_BUTTON, self.on_open_final_item)

    def on_open_main_category(self, event):
        #self.main_cat_window = MyDialog()
        dlg = MyDialog(self)
        dlg.Centre()
        dlg.ShowModal()
        dlg.Destroy()
        #self.main_cat_window = MainCategoryFrame()
        #self.main_cat_window.Show()

    def on_open_sub_category(self, event):
        wx.MessageBox(
            "This is a message box in wxPython!",   # Message text
            "Message Box Title",                    # Window title
            wx.OK | wx.ICON_INFORMATION             # Buttons + icon
        )

    def on_open_final_item(self, event):
        wx.MessageBox(
            "This is a message box in wxPython!",   # Message text
            "Message Box Title",                    # Window title
            wx.OK | wx.ICON_INFORMATION             # Buttons + icon
        )
'''
if __name__ == "__main__":
    app = wx.App()
    dialog = OpenWindowsDialog()
    dialog.ShowModal()
    dialog.Destroy()
    #app.MainLoop()
'''