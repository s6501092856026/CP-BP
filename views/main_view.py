import tkinter as tk
from tkinter import ttk

class MainView(ttk.Frame):

    def __init__(self, controller, app):
        super().__init__(app)
        self.controller = controller

        # Window

        self.label_delete = ttk.Label(self, text="Delete Profile", justify='center', anchor='center', foreground="black", font=("Times New Roman", 10, "bold"))
        self.label_delete.grid(row=2, column=2, padx=10, pady=10, ipady=10, sticky='NEW')

        self.delete_button = ttk.Button(self, text="Delete", command=self.delete_selected_item)
        self.delete_button.grid(row=2, column=2, padx=10, pady=10, ipady=10, sticky='S')

        self.label_break = ttk.Label(self, text="Calculate Break-even Point", justify='center', anchor='center', foreground="black", font=("Times New Roman", 10, "bold"))
        self.label_break.grid(row=0, column=2, padx=10, pady=10, ipadx=10, ipady=10, sticky='NEW')

        self.breakeven_button = ttk.Button(self, text="Break-even Point", command=self.breakeven)
        self.breakeven_button.grid(row=0, column=2, padx=10, pady=10, ipadx=10, ipady=10, sticky='S')

        self.label_create = ttk.Label(self, text="Create New Profile", justify='center', anchor='center', foreground="black", font=("Times New Roman", 10, "bold"))
        self.label_create.grid(row=1, column=2, padx=10, pady=10, ipady=10, sticky='NEW')

        self.newprofile_button = ttk.Button(self, text="New Profile", command=self.newprofile)
        self.newprofile_button.grid(row=1, column=2, padx=10, pady=10, ipadx=10, ipady=10, sticky='S')

        self.label_compare = ttk.Label(self, text="Compare Product", justify='center', anchor='center', foreground="black", font=("Times New Roman", 10, "bold"))
        self.label_compare.grid(row=3, column=2, padx=10, pady=10, ipady=10, sticky='NEW')

        self.compare_button = ttk.Button(self, text="Compare", command=self.compare)
        self.compare_button.grid(row=3, column=2, padx=10, pady=10, ipadx=10, ipady=10, sticky='S')

        # Budgets
        self.list_treeview = ttk.Treeview(self, columns=("ID", "Name"), show="headings")
        self.list_treeview.heading("ID", text="ID")
        self.list_treeview.column("ID", width=10)
        self.list_treeview.heading("Name", text="Name")
        self.list_treeview.column("Name", width=200)
        self.list_treeview.grid(row=0, rowspan=4, column=0, padx=0, pady=0, ipadx=40, ipady=75)
        
        self.list_treeview.bind("<<TreeviewSelect>>", lambda event: self.get_selected_item())

        self.detail_treeview = ttk.Treeview(self, columns=("Detail"), show="headings")
        self.detail_treeview.heading("Detail", text="Detail")
        self.detail_treeview.grid(row=0, rowspan=4, column=1, padx=0, pady=0, ipadx=40, ipady=75)
    
    def newprofile(self):
        self.controller.show_newprofile()
    
    def compare(self):
        self.controller.show_compare()

    def breakeven(self):
        self.controller.show_break()

    def set_profile(self, products):
        self.list_treeview.delete(*self.list_treeview.get_children())
        # [(1, 'machine', None, None), (2, 'not', None, None)]

        for product in products:
            (product_id, product_name) = product
            self.list_treeview.insert("", "end", values=(product_id, product_name))
            
    def set_detail(self, rawmats, transpots, performances):
        self.detail_treeview.delete(*self.detail_treeview.get_children())

        for rawmat in rawmats:
            (name_raw) = rawmat
            self.detail_treeview.insert("", "end", values=(name_raw)) 

        for transpot in transpots:
            (transpot_name) = transpot
            self.detail_treeview.insert("", "end", values=(transpot_name))

        for performance in performances:
            (performance_name) = performance
            self.detail_treeview.insert("", "end", values=(performance_name)) 

    def get_selected_item(self):
        selected_item = self.list_treeview.focus()  # Get the item that is currently selected
        if  selected_item:  # If an item is selected
            item_text = self.list_treeview.item(selected_item, 'values')  # Get the text of the selected item
            self.controller.show_detail(item_text[0])

    def delete_selected_item(self):
        selected_item = self.list_treeview.focus()  # Get the item that is currently selected
        if  selected_item:  # If an item is selected
            item_text = self.list_treeview.item(selected_item, 'values')  # Get the text of the selected item
            self.controller.delete_profile(item_text[0])
            self.controller.show_profile()