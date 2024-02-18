import tkinter as tk
from tkinter import ttk

class MainView(ttk.Frame):

    def __init__(self, controller, app):
        super().__init__(app)
        self.controller = controller

        # Window

        self.edit_profile = ttk.Button(self, text = "Edit Profile")
        self.edit_profile.grid(row=0, column=2, padx=10, pady=10, ipady=10, sticky='N')

        self.delete_button = ttk.Button(self, text="Delete Profile")
        self.delete_button.grid(row=0, column=2, padx=10, pady=10, ipady=5, sticky='S')

        self.breakeven_button = ttk.Button(self, text="Break-even Point", command=self.breakeven)
        self.breakeven_button.grid(row=1, column=2, padx=10, pady=10, ipadx=10, ipady=10, sticky='SEW')

        self.newprofile_button = ttk.Button(self, text="Create New Profile", command=self.newprofile)
        self.newprofile_button.grid(row=2, column=2, padx=10, pady=10, ipady=10, sticky='NEW')

        self.compare_button = ttk.Button(self, text="Compare", command=self.compare)
        self.compare_button.grid(row=2, column=2, padx=10, pady=10, ipadx=10, ipady=10, sticky='SEW')

        # Budgets
        self.list_treeview = ttk.Treeview(self, columns=("ID", "Name"), show="headings")
        self.list_treeview.heading("ID", text="ID" )
        self.list_treeview.heading("Name", text="Name")
        self.list_treeview.grid(row=0, rowspan=3, column=0, padx=5, pady=5, ipadx=40, ipady=75)
        self.list_treeview.insert("", "end")


        self.detail_treeview = ttk.Treeview(self)
        self.detail_treeview.grid(row=0, rowspan=3, column=1, padx=5, pady=5, ipadx=40, ipady=75)
    
    def newprofile(self):
        self.controller.show_newprofile()
    
    def compare(self):
        self.controller.show_compare()

    def breakeven(self):
        self.controller.show_break()




