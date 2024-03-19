import tkinter as tk
from tkinter import ttk

class CompareView(ttk.Frame):

    def __init__(self, controller, app):
        super().__init__(app)
        self.controller = controller

        # Window

        self.back_button = ttk.Button(self, text="Back", command=self.back)
        self.back_button.grid(row=0, column=0, padx=5, sticky='W')

        self.label_product1 = ttk.Label(self, text="First Profile", justify='center', anchor='center', foreground="black", font=("Times New Roman", 10, "bold"))
        self.label_product1.grid(row=3, column=3, columnspan=2, padx=10, pady=10, sticky='N')

        self.entry_product1 = ttk.Entry(self)
        self.entry_product1.grid(row=3, column=3, columnspan=2 , padx=10, pady=10, sticky='')

        self.label_product2 = ttk.Label(self, text="Second Profile", justify='center', anchor='center', foreground="black", font=("Times New Roman", 10, "bold"))
        self.label_product2.grid(row=3, column=3,columnspan=2, padx=10, pady=10, sticky='S')

        self.entry_product2 = ttk.Entry(self)
        self.entry_product2.grid(row=4, column=3, columnspan=2 , padx=10, pady=10, sticky='N')

        self.add_button = ttk.Button(self, text="Add")
        self.add_button.grid(row=4, column=3, padx=10, pady=10, ipady=10, sticky='S')

        self.delete_button = ttk.Button(self, text="Delete")
        self.delete_button.grid(row=4, column=4, padx=10, pady=10, ipady=10, sticky='S')

        self.complete_button = ttk.Button(self, text="Complete", command=self.conprepare)
        self.complete_button.grid(row=5, column=3, columnspan=2 , padx=10, pady=10, ipadx=10, ipady=15, sticky='SEW')

        # Budgets
        self.list_treeview = ttk.Treeview(self, columns=("ID", "Name"), show="headings")
        self.list_treeview.heading("ID", text="ID" )
        self.list_treeview.column("ID", width=10)
        self.list_treeview.heading("Name", text="Name")
        self.list_treeview.grid(row=3, rowspan=3, column=0, padx=5, pady=5, ipadx=40, ipady=75)
        # self.treeview1.insert("", "end")

        self.list_treeview.bind("<<TreeviewSelect>>", lambda event: self.get_selected_item())

        self.detail_treeview = ttk.Treeview(self, columns=("Detail"), show="headings")
        self.detail_treeview.heading("Detail", text="Detail")
        self.detail_treeview.grid(row=3, rowspan=3, column=1, padx=5, pady=5, ipadx=40, ipady=75)

    def back(self):
        self.controller.back_main()

    def conprepare(self):
        self.controller.show_conprepare()

    def set_profile(self, products):
        self.list_treeview.delete(*self.list_treeview.get_children())
        # [(1, 'machine', None, None), (2, 'not', None, None)]

        for product in products:
            (product_id, product_name) = product
            self.list_treeview.insert("", "end", values=(product_id, product_name))

    def set_detail(self, rawmats, transpots):
        self.detail_treeview.delete(*self.detail_treeview.get_children())

        for rawmat in rawmats:
            (name_raw) = rawmat
            self.detail_treeview.insert("", "end", values=(name_raw)) 

        for transpot in transpots:
            (transpot_name) = transpot
            self.detail_treeview.insert("", "end", values=(transpot_name))
        
    def get_selected_item(self):
        selected_item = self.list_treeview.focus()  # Get the item that is currently selected
        if  selected_item:  # If an item is selected
            item_text = self.list_treeview.item(selected_item, 'values')  # Get the text of the selected item
            self.controller.show_detail(item_text[0])


