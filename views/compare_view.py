import tkinter as tk
from tkinter import ttk, Radiobutton

class CompareView(ttk.Frame):

    def __init__(self, controller, app):
        super().__init__(app)
        self.controller = controller

        def filter():
            print (self.radio_state.get())
            gender = self.radio_state.get()
            self.list_treeview.delete(*self.list_treeview.get_children())

        # RadioButton
            
            # Material
            #if gender == 1:
                #for row in data :
                    #self.list_treeview.insert("", "end", values=row)
            # Transpotation
            #elif gender == 2:
                #for row[2] == "Transpotation"
                    #self.list_treeview.insert("", "end", values=row)
            # Performance
            #elif gender == 3:
                #for row[2] == "Perfoemance"
                    #self.list_treeview.insert("", "end", values=row)
        
        self.radio_state = tk.IntVar()
        self.radio_material = Radiobutton(self, value=1, text="Material", variable=self.radio_state, command=filter)
        self.radio_material.grid(row=0,column=0, padx=10, pady=10, sticky='')
        self.radio_transpot = Radiobutton(self, value=2, text="Transpotation", variable=self.radio_state, command=filter)
        self.radio_transpot.grid(row=0,column=0, padx=10, pady=10, sticky='E')
        self.radio_performance = Radiobutton(self, value=3, text="Performance", variable=self.radio_state, command=filter)
        self.radio_performance.grid(row=0,column=1, padx=10, pady=10, sticky='')

        # Window

        self.back_button = ttk.Button(self, text="Back", command=self.back)
        self.back_button.grid(row=0, column=0, padx=5, sticky='W')

        self.entry_profile1 = ttk.Entry(self)
        self.entry_profile1.grid(row=3, column=3, padx=10, pady=10, sticky='N')

        self.entry_profile2 = ttk.Entry(self)
        self.entry_profile2.grid(row=3, column=3, padx=10, pady=10, sticky='')

        self.add_button = ttk.Button(self, text="Add")
        self.add_button.grid(row=3,column=3, padx=10, pady=10, sticky='S')

        self.delete_button = ttk.Button(self, text="Delete")
        self.delete_button.grid(row=4,column=3, padx=10, pady=10, sticky='N')
        
        self.bp_button = ttk.Button(self, text="Break-even Point")
        self.bp_button.grid(row=4, column=3, padx=10, pady=10, ipadx=10, ipady=10, sticky='EW')

        self.complete_button = ttk.Button(self, text="Complete")
        self.complete_button.grid(row=4, column=3, padx=10, pady=10, ipadx=10, ipady=20, sticky='SEW')

        # Budgets
        self.list_treeview = ttk.Treeview(self, columns=("ID", "Name"), show="headings")
        self.list_treeview.heading("ID", text="ID" )
        self.list_treeview.heading("Name", text="Name")
        self.list_treeview.grid(row=3, rowspan=2, column=0, padx=5, pady=5, ipadx=40, ipady=75)
        # self.treeview1.insert("", "end")

        def on_select(event):
            select_item = self.list_treeview.focus
            values = self.list_treeview.item(select_item)["values"]
            print(values)

        self.list_treeview.bind("<<TreeviewSelect>>",on_select)

        self.treeview2 = ttk.Treeview(self)
        self.treeview2.grid(row=3, rowspan=2, column=1, padx=5, pady=5, ipadx=40, ipady=75)

    def back(self):
        self.controller.back_main()

    def set_profile(self, products):
        self.list_treeview.delete(*self.list_treeview.get_children())
        # [(1, 'machine', None, None), (2, 'not', None, None)]

        for product in products:
            (product_id, product_name) = product
            self.list_treeview.insert("", "end", values=(product_id, product_name))


