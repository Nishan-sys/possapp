import wx
import sqlite3
import wx.lib.mixins.listctrl as listmix

class MyFrame(wx.Frame, listmix.ListCtrlAutoWidthMixin):
    def __init__(self):
        super().__init__(None, title="Main Categories", size=(400, 300))
        self.conn = sqlite3.connect('pos_db.db')
        self.cursor = self.conn.cursor()
        


        
        panel = wx.Panel(self)
        vbox = wx.BoxSizer(wx.VERTICAL)
        
        # Top row: TextCtrl and Button 1 side by side
        top_hbox = wx.BoxSizer(wx.HORIZONTAL)
        self.text_ctrl_maincategory = wx.TextCtrl(panel)
        self.button_add = wx.Button(panel, label="Add")
        
        top_hbox.Add(self.text_ctrl_maincategory, proportion=1, flag=wx.EXPAND | wx.RIGHT, border=5)
        top_hbox.Add(self.button_add)
        vbox.Add(top_hbox, flag=wx.EXPAND | wx.ALL, border=5)
        
        # ListCtrl (report mode with columns)
        self.list_ctrl = wx.ListCtrl(panel, style=wx.LC_REPORT | wx.BORDER_SUNKEN)
        self.list_ctrl.InsertColumn(0, 'Category ID', width=150)
        self.list_ctrl.InsertColumn(1, 'Category Name', width=150)
        self.list_ctrl.Bind(wx.EVT_LIST_ITEM_SELECTED, self.on_item_selected)
        vbox.Add(self.list_ctrl, proportion=1, flag=wx.EXPAND | wx.LEFT | wx.RIGHT, border=5)

        self.load_data_from_db()
        # Bottom row: Button 2 and Button 3
        bottom_hbox = wx.BoxSizer(wx.HORIZONTAL)
        self.button2 = wx.Button(panel, label="Edit")
        self.button3 = wx.Button(panel, label="Delete")
        bottom_hbox.Add(self.button2, flag=wx.RIGHT, border=5)
        bottom_hbox.Add(self.button3)
        vbox.Add(bottom_hbox, flag=wx.ALIGN_CENTER | wx.TOP | wx.BOTTOM, border=10)
        self.button_add.Bind(wx.EVT_BUTTON, self.on_insert)

        panel.SetSizer(vbox)
        self.Centre()
        self.Show()

    def add_main_category(self, event):
        #self.on_insert(event)
        #wx.MessageBox("Button Clicked!", "Info", wx.OK | wx.ICON_INFORMATION)
        pass


    def load_data_from_db(self):

        self.cursor.execute("SELECT * FROM main_category")  # adjust table & column names

        # Clear existing items in ListCtrl
        self.list_ctrl.DeleteAllItems()

        # Insert rows into ListCtrl
        for row in self.cursor.fetchall():
            index = self.list_ctrl.InsertItem(self.list_ctrl.GetItemCount(), str(row[0]))
            self.list_ctrl.SetItem(index, 1, row[1])
            #self.list_ctrl.SetItem(index, 2, row[2])

    def on_insert(self, event):
        main_cat = self.text_ctrl_maincategory.GetValue().strip()
        if not main_cat:
            wx.MessageBox("Please fill the text field before inserting.", "Warning", wx.OK | wx.ICON_WARNING)
            return

        # Insert into database
        self.cursor.execute("INSERT INTO main_category (main_cat_name) VALUES (?)", (main_cat,))
        self.conn.commit()

        wx.MessageBox(f"Record '{main_cat}' inserted successfully.", "Info", wx.OK | wx.ICON_INFORMATION)
        self.load_data_from_db()
        self.text_ctrl_maincategory.SetValue("")  # Clear text after insert

    def on_item_selected(self, event):
        # Get the index of the selected item
        selected_index = self.list_ctrl.GetFirstSelected()

        if selected_index != -1: # -1 means no item is selected
            # Get the text of the selected item in the first column
            item_name = self.list_ctrl.GetItemText(selected_index, col=0)
            # Get the text of the selected item in the second column
            item_value = self.list_ctrl.GetItemText(selected_index, col=1)

            print(f"Selected Item: Name='{item_name}', Value='{item_value}'")


    def on_close(self, event):
        # Close DB connection cleanly before closing window
        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.close()
        event.Skip()  # Allow the close to proceed
        


if __name__ == "__main__":
    app = wx.App(False)
    frame = MyFrame()
    app.MainLoop()
