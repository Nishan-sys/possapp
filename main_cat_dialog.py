import wx
import sqlite3
import wx.lib.mixins.listctrl as listmix


class MyDialog(wx.Dialog, listmix.ListCtrlAutoWidthMixin):
    def __init__(self, parent=None):
        super().__init__(parent, title="Main Categories", size=(400, 300))

        # Connect DB and create table if needed
        self.conn = sqlite3.connect('pos_db.db')
        self.cursor = self.conn.cursor()
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS main_category (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                main_cat_name TEXT NOT NULL
            )
        ''')
        self.conn.commit()

        panel = wx.Panel(self)
        vbox = wx.BoxSizer(wx.VERTICAL)

        # Top row: TextCtrl + Add button
        top_hbox = wx.BoxSizer(wx.HORIZONTAL)
        self.text_ctrl_maincategory = wx.TextCtrl(panel)
        self.button_add = wx.Button(panel, label="Add")
        top_hbox.Add(self.text_ctrl_maincategory, proportion=1, flag=wx.EXPAND | wx.RIGHT, border=5)
        top_hbox.Add(self.button_add)
        vbox.Add(top_hbox, flag=wx.EXPAND | wx.ALL, border=5)

        # ListCtrl with columns
        self.list_ctrl = AutoWidthListCtrl(panel)
        #self.list_ctrl = AutoWidthListCtrl(panel)
        #self.list_ctrl = wx.ListCtrl(panel, style=wx.LC_REPORT | wx.BORDER_SUNKEN)
        self.list_ctrl.InsertColumn(0, 'Category ID', width=150)
        self.list_ctrl.InsertColumn(1, 'Category Name', width=150)

        vbox.Add(self.list_ctrl, proportion=1, flag=wx.EXPAND | wx.LEFT | wx.RIGHT, border=5)

        # Make last column auto width
        #listmix.ListCtrlAutoWidthMixin.__init__(self)

        # Bottom buttons: Edit and Delete
        bottom_hbox = wx.BoxSizer(wx.HORIZONTAL)
        self.button_edit = wx.Button(panel, label="Edit")
        self.button_delete = wx.Button(panel, label="Delete")
        bottom_hbox.Add(self.button_edit, flag=wx.RIGHT, border=5)
        bottom_hbox.Add(self.button_delete)
        vbox.Add(bottom_hbox, flag=wx.ALIGN_CENTER | wx.TOP | wx.BOTTOM, border=10)

        panel.SetSizer(vbox)

        # Bind events
        self.button_add.Bind(wx.EVT_BUTTON, self.on_insert)
        self.button_edit.Bind(wx.EVT_BUTTON, self.on_edit)
        self.button_delete.Bind(wx.EVT_BUTTON, self.on_delete)
        self.list_ctrl.Bind(wx.EVT_LIST_ITEM_SELECTED, self.on_item_selected)
        self.Bind(wx.EVT_CLOSE, self.on_close)

        # Load initial data
        self.load_data_from_db()

    def load_data_from_db(self):
        self.cursor.execute("SELECT * FROM main_category")
        self.list_ctrl.DeleteAllItems()
        for row in self.cursor.fetchall():
            index = self.list_ctrl.InsertItem(self.list_ctrl.GetItemCount(), str(row[0]))  # id
            self.list_ctrl.SetItem(index, 1, str(row[1]))  # name

    def on_insert(self, event):
        main_cat = self.text_ctrl_maincategory.GetValue().strip()
        if not main_cat:
            wx.MessageBox("Please fill the text field before inserting.", "Warning", wx.OK | wx.ICON_WARNING)
            return

        self.cursor.execute("INSERT INTO main_category (main_cat_name) VALUES (?)", (main_cat,))
        self.conn.commit()
        wx.MessageBox(f"Record '{main_cat}' inserted successfully.", "Info", wx.OK | wx.ICON_INFORMATION)
        self.load_data_from_db()
        self.text_ctrl_maincategory.SetValue("")

    def on_edit(self, event):
        selected_index = self.list_ctrl.GetFirstSelected()
        if selected_index == -1:
            wx.MessageBox("Please select an item to edit.", "Warning", wx.OK | wx.ICON_WARNING)
            return
        cat_id = int(self.list_ctrl.GetItemText(selected_index, 0))
        old_name = self.list_ctrl.GetItemText(selected_index, 1)
        dlg = wx.TextEntryDialog(self, "Edit Category Name:", "Edit", defaultValue=old_name)
        if dlg.ShowModal() == wx.ID_OK:
            new_name = dlg.GetValue().strip()
            if new_name:
                self.cursor.execute("UPDATE main_category SET main_cat_name=? WHERE id=?", (new_name, cat_id))
                self.conn.commit()
                self.load_data_from_db()
            else:
                wx.MessageBox("Category name cannot be empty.", "Warning", wx.OK | wx.ICON_WARNING)
        dlg.Destroy()

    def on_delete(self, event):
        selected_index = self.list_ctrl.GetFirstSelected()
        if selected_index == -1:
            wx.MessageBox("Please select an item to delete.", "Warning", wx.OK | wx.ICON_WARNING)
            return
        cat_id = int(self.list_ctrl.GetItemText(selected_index, 0))
        dlg = wx.MessageDialog(self, "Are you sure you want to delete this category?", "Confirm Delete",
                               wx.YES_NO | wx.NO_DEFAULT | wx.ICON_QUESTION)
        if dlg.ShowModal() == wx.ID_YES:
            self.cursor.execute("DELETE FROM main_category WHERE id=?", (cat_id,))
            self.conn.commit()
            self.load_data_from_db()
        dlg.Destroy()

    def on_item_selected(self, event):
        selected_index = self.list_ctrl.GetFirstSelected()
        if selected_index != -1:
            item_id = self.list_ctrl.GetItemText(selected_index, 0)
            item_name = self.list_ctrl.GetItemText(selected_index, 1)
            print(f"Selected Item: ID='{item_id}', Name='{item_name}'")

    def on_close(self, event):
        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.close()
        event.Skip()

class AutoWidthListCtrl(wx.ListCtrl, listmix.ListCtrlAutoWidthMixin):
    def __init__(self, parent):
        wx.ListCtrl.__init__(self, parent, style=wx.LC_REPORT | wx.BORDER_SUNKEN)
        listmix.ListCtrlAutoWidthMixin.__init__(self)

'''
if __name__ == "__main__":
    app = wx.App(False)
    dlg = MyDialog()
    dlg.Center()
    dlg.ShowModal()
    dlg.Destroy()
    #app.MainLoop()
'''