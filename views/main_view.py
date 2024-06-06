import tkinter as tk
from tkinter import ttk, messagebox
class MainView(ttk.Frame):

    def __init__(self, controller, app):
        super().__init__(app)
        self.controller = controller

        # Window

        # Create a style object
        # style = ttk.Style()

        # Configure the style to have a green background
        # style.configure("Green.TButton", background="green", font=("Arial", 10))
        # style.configure("Red.TButton", background="red", font=("Arial", 10))

        # self.delete_button = ttk.Button(self, text="ลบ", command=self.delete_selected_item)
        # self.delete_button.grid(row=3, column=3, padx=10, pady=10, ipady=10, sticky='N')

        # self.breakeven_button = ttk.Button(self, text="จุดคุ้มทุน", command=self.breakeven)
        # self.breakeven_button.grid(row=0, column=3, padx=10, pady=10, ipadx=10, ipady=10)

        # self.newprofile_button = ttk.Button(self, text="สร้างโปรไฟล์ใหม่", command=self.newprofile)
        # self.newprofile_button.grid(row=2, column=3, padx=10, pady=10, ipadx=10, ipady=10, sticky='NEW')

        # self.compare_button = ttk.Button(self, text="เปรียบเทียบ", command=self.compare)
        # self.compare_button.grid(row=4, column=3, padx=10, pady=10, ipadx=10, ipady=10, sticky='NEW')

        # self.edit_button = ttk.Button(self, text="แก้ไขโปรไฟล์", command=self.edit) 
        # self.edit_button.grid(row=1, column=3, padx=10, pady=10, ipadx=10, ipady=10, sticky='NEW')

        button_configs = [{"text": "ลบ", "command": self.delete_selected_item, "row": 3, "column": 3, "sticky": 'EW'},
            {"text": "จุดคุ้มทุน", "command": self.breakeven, "row": 0, "column": 3, "sticky": 'EW'},
            {"text": "สร้างโปรไฟล์ใหม่", "command": self.newprofile, "row": 2, "column": 3, "sticky": 'EW'},
            {"text": "เปรียบเทียบ", "command": self.compare, "row": 4, "column": 3, "sticky": 'EW'},
            {"text": "แก้ไขโปรไฟล์", "command": self.edit, "row": 1, "column": 3, "sticky": 'EW'},]

        for config in button_configs:
            button = ttk.Button(self, text=config["text"], command=config["command"])
            button.grid(row=config["row"], column=config["column"], padx=10, pady=10, ipadx=10, ipady=10, sticky=config.get("sticky", ''))


        # Budgets
        self.list_treeview = ttk.Treeview(self, columns=("ID", "Name"), show="headings")
        self.list_treeview.heading("ID", text="ไอดี")
        self.list_treeview.column("ID", width=10)
        self.list_treeview.heading("Name", text="ชื่อ")
        self.list_treeview.column("Name", width=200)
        self.list_treeview.grid(row=0, rowspan=5, column=0, padx=5, pady=5, ipadx=20, ipady=80)

        # สร้าง Scrollbar แนวแกน Y
        scroll_y = ttk.Scrollbar(self, orient='vertical', command=self.list_treeview.yview)
        self.list_treeview.configure(yscrollcommand=scroll_y.set)
        scroll_y.grid(row=0, rowspan=5, column=1, sticky='NS')

        self.grid_rowconfigure(0, weight=1)
        # self.grid_columnconfigure(0, weight=1)
        
        self.list_treeview.bind("<<TreeviewSelect>>", lambda event: self.get_selected_item())

        self.detail_treeview = ttk.Treeview(self, columns=("Detail", "Amount", "Unit"), show="headings")
        self.detail_treeview.heading("Detail", text="รายละเอียด")
        self.detail_treeview.column("Detail", width=200)
        self.detail_treeview.heading("Amount", text="ปริมาณ")
        self.detail_treeview.column("Amount", width=30)
        self.detail_treeview.heading("Unit", text="หน่วย")
        self.detail_treeview.column("Unit", width=5)
        self.detail_treeview.grid(row=0, rowspan=5, column=2, padx=5, pady=5, ipadx=170, ipady=80)
    
    def newprofile(self):
        self.controller.show_newprofile()
    
    def compare(self):
        self.controller.show_compare()

    def breakeven(self):
        self.controller.show_break()

    def edit(self):
        selected_item = self.list_treeview.focus()  # Get the item that is currently selected
        if  selected_item:  # If an item is selected
            item_text = self.list_treeview.item(selected_item, 'values')  # Get the text of the selected item
            self.controller.show_editprofile(item_text[0] )
        
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