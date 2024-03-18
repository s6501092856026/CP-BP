import tkinter as tk
from tkinter import ttk, Radiobutton

class NewprofileView(ttk.Frame):

    def __init__(self, controller, app):
        super().__init__(app)
        self.controller = controller
        
        self.radio_state = tk.IntVar(value=1)

        self.radio_material = Radiobutton(self, value=1, text="Material", variable=self.radio_state, command=self.filter)
        self.radio_material.grid(row=0,column=0, padx=10, pady=10, sticky='')

        self.radio_transpot = Radiobutton(self, value=2, text="Transpotation", variable=self.radio_state, command=self.filter)
        self.radio_transpot.grid(row=0,column=2, padx=10, pady=10, sticky='W')

        self.radio_performance = Radiobutton(self, value=3, text="Performance", variable=self.radio_state, command=self.filter)
        self.radio_performance.grid(row=0,column=2, padx=10, pady=10, sticky='')

        self.combo_box = ttk.Combobox(self,)
        self.combo_box.grid(row=0,column=2, padx=10, pady=10, sticky='E')
        self.combo_box.bind("<<ComboboxSelected>>", self.filter)

        # Window
        self.entry_name = ttk.Entry(self)
        self.entry_name.grid(row=0,column=3, padx=10, pady=10, sticky='NEW')

        self.label_name = ttk.Label(self, text = "Name Profile", foreground="black", font=("Times New Roman", 10, "bold"))
        self.label_name.grid(row=0,column=4, padx=10, pady=10, sticky= 'W')

        self.back_button = ttk.Button(self, text="Back", command=self.back)
        self.back_button.grid(row=0, column=0, padx=5, pady=10, sticky='W')

        self.label_unit = ttk.Label(self, text = "Unit", foreground="black", font=("Times New Roman", 10, "bold"))
        self.label_unit.grid(row=3,column=4, padx=10, pady=10, sticky='W')

        self.entry_unit = ttk.Entry(self)
        self.entry_unit.grid(row=3,column=3, padx=10, pady=10, sticky='EW')

        self.add_button = ttk.Button(self, text="Add", command=self.add_profile_item)
        self.add_button.grid(row=4,column=3, padx=15, pady=10, sticky='')

        self.delete_button = ttk.Button(self, text="Remove", command=self.delete_profile_item)
        self.delete_button.grid(row=4,column=4, padx=15, pady=10, sticky='')
        
        self.bp_button = ttk.Button(self, text="Break-even Point", command=self.breakeven)
        self.bp_button.grid(row=5, column=3, columnspan=2, padx=10, pady=10, ipadx=20, ipady=10, sticky='S')

        self.complete_button = ttk.Button(self, text="Complete", command=self.connew)
        self.complete_button.grid(row=6, column=3, columnspan=2, padx=10, pady=10, ipadx=40, ipady=15, sticky='')

        # Budgets
        self.list_treeview = ttk.Treeview(self, columns=("ID", "Name"), show="headings")
        self.list_treeview.heading("ID", text="ID")
        self.list_treeview.column("ID", width=30)
        self.list_treeview.heading("Name", text="Name")
        self.list_treeview.column("Name", width=310)
        self.list_treeview.grid(row=3, rowspan=4, column=0, ipady=75)

        # สร้าง Scrollbar แนวแกน Y
        scroll_y = ttk.Scrollbar(self, orient='vertical', command=self.list_treeview.yview)
        self.list_treeview.configure(yscrollcommand=scroll_y.set)

        scroll_y.grid(row=3,rowspan=4, column=1, sticky='NS')

        self.grid_rowconfigure(0, weight=1)
        # self.grid_columnconfigure(0, weight=1)

        # self.mat_treeview = ttk.Treeview(self, columns=("ID", "Name"), show="headings")
        # self.mat_treeview.heading("ID", text="ID" )
        # self.mat_treeview.column("ID", width=10)
        # self.mat_treeview.heading("Name", text="Name")
        # self.mat_treeview.grid(row=3, rowspan=4, column=0, padx=5, pady=5, ipadx=40, ipady=75)

        # self.transpot_treeview = ttk.Treeview(self, columns=("ID", "Name"), show="headings")
        # self.transpot_treeview.heading("ID", text="ID" )
        # self.transpot_treeview.column("ID", width=10)
        # self.transpot_treeview.heading("Name", text="Name")
        # self.transpot_treeview.grid(row=3, rowspan=4, column=0, padx=5, pady=5, ipadx=40, ipady=75)

        # self.performance_treeview = ttk.Treeview(self, columns=("ID", "Name"), show="headings")
        # self.performance_treeview.heading("ID", text="ID" )
        # self.performance_treeview.column("ID", width=10)
        # self.performance_treeview.heading("Name", text="Name")
        # self.performance_treeview.grid(row=3, rowspan=4, column=0, padx=5, pady=5, ipadx=40, ipady=75)

        self.select_treeview = ttk.Treeview(self, columns=('Type', "ID", "Name", "Amount", ), show="headings")
        self.select_treeview.heading('Type', text="Type")
        self.select_treeview.column("Type", width=85)
        self.select_treeview.heading("ID", text="ID" )
        self.select_treeview.column("ID", width=30)
        self.select_treeview.heading("Name", text="Name")
        self.select_treeview.column("Name", width=310)
        self.select_treeview.heading("Amount", text="Amount")
        self.select_treeview.grid(row=3, rowspan=4, column=2, padx=5, pady=5, ipady=75)
        
    def filter(self, event = None):
        
        # radio button
        filter_cate = self.radio_state.get()
        
        # combobox
        filter_type = self.combo_box.get()
        self.controller.show_profile_name(filter_cate, filter_type)

    def back(self):
        self.controller.back_main()

    def show_detail_view(self):
        self.controller.show_detail_view()

    def breakeven(self):
        self.controller.show_break()
    
    def connew(self):
        self.controller.show_connew()

    def set_profile_name(self, rawmats, type_rawmats , transpots, performances, type_performances):
        
        # TREEVIEW
        self.list_treeview.delete(*self.list_treeview.get_children())
        for rawmat in rawmats:
            (rawmat_id, name_raw) = rawmat
            self.list_treeview.insert("", "end", values=(rawmat_id, name_raw,))

        for transpot in transpots:
            (transpot_id, transpot_name) = transpot
            self.list_treeview.insert("", "end", values=(transpot_id, transpot_name,)) 
        
        for performance in performances:
            (performance_id, performance_name) = performance
            self.list_treeview.insert("", "end", values=(performance_id, performance_name,)) 


        # COMBOBOX
        self.combo_box.delete(0, tk.END)
        if len(type_rawmats) > 0:
            values = []
            for type_rawmat in type_rawmats:
                values.append(type_rawmat[0])
            self.combo_box['values'] = values
        if len(type_performances) > 0:
            values = []
            for type_performance in type_performances:
                values.append(type_performance[0])
            self.combo_box['values'] = values

    def add_profile_item(self):
        selected_item = self.list_treeview.focus()  # Get the item that is currently selected
        if  selected_item:  # If an item is selected
            item_text = self.list_treeview.item(selected_item, 'values')
            filter_cate = self.radio_state.get()
            filter_cate_text = ''
            if filter_cate == 1:
                filter_cate_text = 'Material'
            elif filter_cate == 2:
                filter_cate_text = 'Transpotation'
            else:
                filter_cate_text = 'Performance'

            item = (filter_cate_text, item_text[0], item_text[1] )
            self.select_treeview.insert("", "end", values=item) 

    def delete_profile_item(self):
        selected_item = self.select_treeview.focus()  # Get the item that is currently selected
        if  selected_item:  # If an item is selected
            self.select_treeview.delete(selected_item)