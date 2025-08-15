import wx
import sqlite3



class POSPanel(wx.Panel):
    def __init__(self, parent):
        super().__init__(parent)

        # Sample product catalog (product name -> price)
        '''
        self.products = {
            "Apple": 0.50,
            "Banana": 0.30,
            "Orange": 0.80,
            "Milk (1L)": 1.20,
            "Bread (Loaf)": 1.00,
            "Eggs (Dozen)": 2.50,
            "Cheese (200g)": 3.00,
            "Coffee (250g)": 4.50,
        }
        '''
        self.products = {}  # Initialize as an empty dictionary
        conn = sqlite3.connect('pos_db.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM final_item")
        rows = cursor.fetchall()
        for my_tuple in rows:
            self.products[my_tuple[2]] = my_tuple[3] 
        # Initialize as an empty list
        #print(type(rows))  # Debugging line to check the type of rows
        conn.close()
        
        #Debugging line to check the products fetched from the database
        #self.products= ["Apple", "Banana", "Orange", "Milk (1L)", "Bread (Loaf)", "Eggs (Dozen)", "Cheese (200g)", "Coffee (250g)"]

        self.cart = {}  # Internal cart: product -> quantity

        # Main vertical sizer
        main_sizer = wx.BoxSizer(wx.VERTICAL)

        # Top: Search box and product list
        search_label = wx.StaticText(self, label="Search Products:")
        self.search_ctrl = wx.SearchCtrl(self, style=wx.TE_PROCESS_ENTER)
        self.search_ctrl.ShowSearchButton(True)
        self.search_ctrl.ShowCancelButton(True)
        self.search_ctrl.Bind(wx.EVT_TEXT, self.on_search)
        self.search_ctrl.Bind(wx.EVT_SEARCHCTRL_CANCEL_BTN, self.on_search_cancel)

        search_sizer = wx.BoxSizer(wx.HORIZONTAL)
        search_sizer.Add(search_label, 0, wx.ALIGN_CENTER_VERTICAL | wx.RIGHT, 5)
        search_sizer.Add(self.search_ctrl, 1, wx.EXPAND)

        main_sizer.Add(search_sizer, 0, wx.ALL | wx.EXPAND, 5)

        # Product List (wx.ListCtrl in report mode)
        self.product_list = wx.ListCtrl(self, style=wx.LC_REPORT | wx.BORDER_SUNKEN)
        self.product_list.InsertColumn(0, "Product", width=180)
        self.product_list.InsertColumn(1, "Price", wx.LIST_FORMAT_RIGHT, 80)
        

        self.populate_product_list()
        main_sizer.Add(self.product_list, 1, wx.ALL | wx.EXPAND, 5)
        
        # Quantity selection and Add to Cart button
        qty_label = wx.StaticText(self, label="Quantity:")
        self.qty_spin = wx.SpinCtrl(self, min=1, max=100, initial=1)
        self.btn_add = wx.Button(self, label="Add to Cart")
        self.btn_add.Bind(wx.EVT_BUTTON, self.on_add_to_cart)

        qty_sizer = wx.BoxSizer(wx.HORIZONTAL)
        qty_sizer.Add(qty_label, 0, wx.ALIGN_CENTER_VERTICAL | wx.RIGHT, 5)
        qty_sizer.Add(self.qty_spin, 0, wx.RIGHT, 15)
        qty_sizer.Add(self.btn_add, 0)

        main_sizer.Add(qty_sizer, 0, wx.ALL, 5)

        # Divider line
        line = wx.StaticLine(self)
        main_sizer.Add(line, 0, wx.EXPAND | wx.ALL, 5)

        # Cart label and list
        cart_label = wx.StaticText(self, label="Shopping Cart:")
        main_sizer.Add(cart_label, 0, wx.LEFT | wx.TOP, 5)

        self.cart_list = wx.ListCtrl(self, style=wx.LC_REPORT | wx.BORDER_SUNKEN | wx.LC_SINGLE_SEL)
        self.cart_list.InsertColumn(0, "Product", width=180)
        self.cart_list.InsertColumn(1, "Quantity", wx.LIST_FORMAT_RIGHT, 80)
        self.cart_list.InsertColumn(2, "Unit Price", wx.LIST_FORMAT_RIGHT, 80)
        self.cart_list.InsertColumn(3, "Total Price", wx.LIST_FORMAT_RIGHT, 100)

        main_sizer.Add(self.cart_list, 2, wx.ALL | wx.EXPAND, 5)

        # Cart action buttons and total display
        self.btn_remove = wx.Button(self, label="Remove Selected")
        self.btn_remove.Bind(wx.EVT_BUTTON, self.on_remove_from_cart)
        self.btn_checkout = wx.Button(self, label="Checkout")
        self.btn_checkout.Bind(wx.EVT_BUTTON, self.on_checkout)
        self.total_label = wx.StaticText(self, label="Total: $0.00", style=wx.ALIGN_RIGHT)

        bottom_sizer = wx.BoxSizer(wx.HORIZONTAL)
        bottom_sizer.Add(self.btn_remove, 0, wx.RIGHT, 10)
        bottom_sizer.Add(self.btn_checkout, 0)
        bottom_sizer.AddStretchSpacer()
        bottom_sizer.Add(self.total_label, 0, wx.ALIGN_CENTER_VERTICAL)

        main_sizer.Add(bottom_sizer, 0, wx.ALL | wx.EXPAND, 5)

        self.SetSizer(main_sizer)
        
        self.update_cart_display()

    def populate_product_list(self, filter_text=""):
        """Populate the product list, optionally filtering by search text."""
        self.product_list.DeleteAllItems()
        filter_lower = filter_text.lower()
        for product, price in self.products.items():
            if filter_lower in product.lower():
                index = self.product_list.InsertItem(self.product_list.GetItemCount(), product)
                #self.product_list.SetItem(index, 1, f"${price:.2f}")
                self.product_list.SetItem(index, 1, f"Rs:{price}")
        self.product_list.Select(0)  # Select the first item by default
        self.product_list.Focus(0)

    def on_search(self, event):
        search_term = self.search_ctrl.GetValue()
        self.populate_product_list(search_term)

    def on_search_cancel(self, event):
        self.search_ctrl.Clear()
        self.populate_product_list()

    def on_add_to_cart(self, event):
        selected_index = self.product_list.GetFirstSelected()
        if selected_index == -1:
            wx.MessageBox("Please select a product to add.", "Info", wx.OK | wx.ICON_INFORMATION)
            return

        product = self.product_list.GetItemText(selected_index)
        quantity = self.qty_spin.GetValue()

        if product in self.cart:
            self.cart[product] += quantity
        else:
            self.cart[product] = quantity

        self.update_cart_display()

    def on_remove_from_cart(self, event):
        selected_index = self.cart_list.GetFirstSelected()
        if selected_index == -1:
            wx.MessageBox("Please select an item in the cart to remove.", "Info", wx.OK | wx.ICON_INFORMATION)
            return

        product = self.cart_list.GetItemText(selected_index)
        if product in self.cart:
            del self.cart[product]
        self.update_cart_display()

    def update_cart_display(self):
        self.cart_list.DeleteAllItems()
        total = 0.0
        for product, qty in self.cart.items():
            unit_price = self.products.get(product, 0)
            total_price = unit_price * qty
            index = self.cart_list.InsertItem(self.cart_list.GetItemCount(), product)
            self.cart_list.SetItem(index, 1, str(qty))
            self.cart_list.SetItem(index, 2, f"Rs:{unit_price:.2f}")
            self.cart_list.SetItem(index, 3, f"Rs:{total_price:.2f}")
            total += total_price

        self.total_label.SetLabel(f"Total: Rs:{total:.2f}")

    def on_checkout(self, event):
        if not self.cart:
            wx.MessageBox("Cart is empty. Please add items before checkout.", "Info", wx.OK | wx.ICON_INFORMATION)
            return

        total = sum(self.products[p] * q for p, q in self.cart.items())
        wx.MessageBox(f"Total amount due: ${total:.2f}\n\nThank you for your purchase!", 
                      "Checkout", wx.OK | wx.ICON_INFORMATION)
        self.cart.clear()
        self.update_cart_display()


class POSFrame(wx.Frame):
    def __init__(self):
        super().__init__(None, title="POS Application", size=(600, 700))
        panel = POSPanel(self)
        self.Show()
        self.Centre()


if __name__ == "__main__":
    app = wx.App(False)
    frame = POSFrame()
    app.MainLoop()
