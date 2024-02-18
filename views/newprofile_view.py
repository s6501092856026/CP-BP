import tkinter as tk
from tkinter import ttk, Radiobutton

class NewprofileView(ttk.Frame):

    def __init__(self, controller, app):
        super().__init__(app)
        self.controller = controller

        #def filter():
            #print (self.radio_state.get())
            #gender = self.radio_state.get()
            #self.list_treeview.delete(*self.list_treeview.get_children())

        # RadioButton
            
            # Material
            #if gender == 1:
                # ดึงข้อมูลมาจาก Database
            
                #for row in data :
                    #self.list_treeview.insert("", "end", values=row)
            # Transpotation
            #elif gender == 2:
                #for row[2] == "Transpotation":
                    #self.list_treeview.insert("", "end", values=row)
            # Performance
            #elif gender == 3:
                #for row[2] == "Perfoemance"
                    #self.list_treeview.insert("", "end", values=row)
        data = ["Option 1", "Option 2", "Option 3", "Option 4"]
        
        self.radio_state = tk.IntVar()
        self.radio_material = Radiobutton(self, value=1, text="Material", variable=self.radio_state, command=filter)
        self.radio_material.grid(row=0,column=0, padx=10, pady=10, sticky='')
        self.radio_transpot = Radiobutton(self, value=2, text="Transpotation", variable=self.radio_state, command=filter)
        self.radio_transpot.grid(row=0,column=0, padx=10, pady=10, sticky='E')
        self.radio_performance = Radiobutton(self, value=3, text="Performance", variable=self.radio_state, command=filter)
        self.radio_performance.grid(row=0,column=1, padx=10, pady=10, sticky='')

        self.combo_box = ttk.Combobox(self, values=data)
        self.combo_box.grid(row=0,column=2, padx=10, pady=10, sticky='')

        # Window

        self.entry_name = ttk.Entry(self)
        self.entry_name.grid(row=3,column=2, padx=10, pady=10, sticky='SEW')

        self.label_name = ttk.Label(self, text = "Name Profile", justify='center')
        self.label_name.grid(row=3,column=2, padx=10, pady=10)

        self.back_button = ttk.Button(self, text="Back", command=self.back)
        self.back_button.grid(row=0, column=0, padx=5, pady=10, sticky='W')

        self.add_button = ttk.Button(self, text="Add")
        self.add_button.grid(row=4,column=2, padx=10, pady=10, sticky='S')

        self.delete_button = ttk.Button(self, text="Delete")
        self.delete_button.grid(row=5,column=2, padx=10, pady=10, sticky='N')
        
        self.bp_button = ttk.Button(self, text="Break-even Point")
        self.bp_button.grid(row=6, column=2, padx=10, pady=10, ipadx=10, ipady=10, sticky='NEW')

        self.complete_button = ttk.Button(self, text="Complete")
        self.complete_button.grid(row=6, column=2, padx=10, pady=10, ipadx=10, ipady=15, sticky='SEW')

        # Budgets
        self.list_treeview = ttk.Treeview(self, columns=("ID", "Name"), show="headings")
        self.list_treeview.heading("ID", text="ID" )
        self.list_treeview.heading("Name", text="Name")
        self.list_treeview.grid(row=3, rowspan=4, column=0, padx=5, pady=5, ipadx=40, ipady=75)
        self.list_treeview.insert("", "end")

        def on_combobox_select(event):
            selected_item = self.combo_box.get()
            print("Selected:", selected_item)

        def on_select(event):
            select_item = self.list_treeview.focus
            values = self.list_treeview.item(select_item)["values"]
            print(values)

        self.combo_box.bind("<<ComboboxSelected>>", on_combobox_select)

        self.list_treeview.bind("<<TreeviewSelect>>",on_select)

        self.detail_treeview = ttk.Treeview(self)
        self.detail_treeview.grid(row=3, rowspan=4, column=1, padx=5, pady=5, ipadx=40, ipady=75)
    
    def back(self):
        self.controller.back_main()





