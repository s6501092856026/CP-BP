import tkinter as tk
from tkinter import ttk, Radiobutton, messagebox

class NewprofileView(ttk.Frame):

    def __init__(self, controller, app):
        super().__init__(app)
        self.controller = controller
        
        self.radio_state = tk.IntVar(value=1)

        self.radio_material = Radiobutton(self, value=1, text="Material", variable=self.radio_state, command=self.filter)
        self.radio_material.grid(row=0, column=0, padx=10, pady=10, sticky='')

        self.radio_transpot = Radiobutton(self, value=2, text="Transpotation", variable=self.radio_state, command=self.filter)
        self.radio_transpot.grid(row=0, column=2, padx=10, pady=10, sticky='W')

        self.radio_performance = Radiobutton(self, value=3, text="Performance", variable=self.radio_state, command=self.filter)
        self.radio_performance.grid(row=0, column=2, padx=10, pady=10, sticky='')

        self.combo_box = ttk.Combobox(self,)
        self.combo_box.grid(row=0, column=2, padx=10, pady=10, sticky='E')
        self.combo_box.bind("<<ComboboxSelected>>", self.filter)

        # Window
        self.entry_name = ttk.Entry(self, text = "")
        self.entry_name.grid(row=0, column=3, padx=10, pady=10, sticky='NEW')

        self.label_name = ttk.Label(self, text = "Name Profile", foreground="black", font=("Times New Roman", 10, "bold"))
        self.label_name.grid(row=0, column=4, padx=10, pady=10, sticky= 'W')

        self.back_button = ttk.Button(self, text="Back", command=self.back)
        self.back_button.grid(row=0, column=0, padx=5, pady=10, sticky='W')

        self.label_unit = ttk.Label(self, text = "Unit", foreground="black", font=("Times New Roman", 10, "bold"))
        self.label_unit.grid(row=3, column=4, padx=10, pady=10, sticky='W')

        self.entry_amount = ttk.Entry(self, text = "")
        self.entry_amount.grid(row=3, column=3, padx=10, pady=10, sticky='EW')

        self.add_button = ttk.Button(self, text="Add", command=self.add_profile_item)
        self.add_button.grid(row=4, column=3, padx=10, pady=10, ipady=10, sticky='N')

        self.delete_button = ttk.Button(self, text="Remove", command=self.delete_profile_item)
        self.delete_button.grid(row=4, column=4, padx=10, pady=10, ipady=10, sticky='N')
        
        self.complete_button = ttk.Button(self, text="Complete", command=self.show_complete)
        self.complete_button.grid(row=6, column=3, columnspan=2, padx=10, pady=10, ipadx=40, ipady=15, sticky='S')

        self.update_button = ttk.Button(self, text="Update Amount", command=self.update_amount)
        self.update_button.grid(row=5, column=3, columnspan=2, padx=10, pady=10, ipadx=10, ipady=10 ,sticky='')

        # Budgets
        self.list_treeview = ttk.Treeview(self, columns=("ID", "Name", "Carbon", "Unit"), show="headings")
        self.list_treeview.heading("ID", text="ID")
        self.list_treeview.column("ID", width=30)
        self.list_treeview.heading("Name", text="Name")
        self.list_treeview.column("Name", width=310)
        self.list_treeview.heading("Carbon", text="Carbon")
        self.list_treeview.column("Carbon", width=50)
        self.list_treeview.heading("Unit", text="Unit")
        self.list_treeview.column("Unit", width=40)
        self.list_treeview.grid(row=3, rowspan=4, column=0, ipady=75)

        # สร้าง Scrollbar แนวแกน Y
        scroll_y = ttk.Scrollbar(self, orient='vertical', command=self.list_treeview.yview)
        self.list_treeview.configure(yscrollcommand=scroll_y.set)
        scroll_y.grid(row=3, rowspan=4, column=1, sticky='NS')

        self.grid_rowconfigure(0, weight=1)
        # self.grid_columnconfigure(0, weight=1)

        self.select_treeview = ttk.Treeview(self, columns=('Type', "ID", "Name", "Amount", "Unit"), show="headings")
        self.select_treeview.heading('Type', text="Type")
        self.select_treeview.column("Type", width=85)
        self.select_treeview.heading("ID", text="ID" )
        self.select_treeview.column("ID", width=30)
        self.select_treeview.heading("Name", text="Name")
        self.select_treeview.column("Name", width=310)
        self.select_treeview.heading("Amount", text="Amount")
        self.select_treeview.column("Amount", width=100)
        self.select_treeview.heading("Unit", text="Unit")
        self.select_treeview.column("Unit", width=40)
        self.select_treeview.grid(row=3, rowspan=4, column=2, ipady=75)

        self.select_treeview.bind("<ButtonRelease-1>", self.on_select_treeview_click)
        
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

    def show_complete(self):
        items = []
        children = self.select_treeview.get_children()
        for child in children:
            items.append(self.select_treeview.item(child)['values'] )
        self.controller.show_connew(items)

    def set_select(self, products, rawmats, transpots, performances):
        self.select_treeview.delete(*self.select_treeview.get_children())

        for product in products:
            (product_name) = product
            self.entry_name.insert(0, product_name)

        for rawmat in rawmats:
            (name_raw) = rawmat
            self.select_treeview.insert("", "end", values=(name_raw)) 

        for transpot in transpots:
            (transpot_name) = transpot
            self.select_treeview.insert("", "end", values=(transpot_name))

        for performance in performances:
            (performance_name) = performance
            self.select_treeview.insert("", "end", values=(performance_name)) 

    def set_profile_name(self, rawmats, type_rawmats , transpots, performances, type_performances):
        
        # TREEVIEW
        self.list_treeview.delete(*self.list_treeview.get_children())
        for rawmat in rawmats:
            (rawmat_id, name_raw, carbon_per_raw, unit_raw) = rawmat
            self.list_treeview.insert("", "end", values=(rawmat_id, name_raw, carbon_per_raw, unit_raw,))

        for transpot in transpots:
            (transpot_id, transpot_name, carbon_per_transpot, unit_transpot) = transpot
            self.list_treeview.insert("", "end", values=(transpot_id, transpot_name, carbon_per_transpot, unit_transpot,)) 
        
        for performance in performances:
            (performance_id, performance_name, carbon_per_performance, unit_performance) = performance
            self.list_treeview.insert("", "end", values=(performance_id, performance_name, carbon_per_performance, unit_performance,)) 


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

            # ดึงค่าจาก entry_amount และแปลงเป็น float
            amount = self.entry_amount.get()
            if not amount:
                messagebox.showerror("Input Error", "Please enter a value in the amount field.")
                return

            try:
                amount = float(amount)
            except ValueError:
                messagebox.showerror("Input Error", "Please enter a valid float value in the amount field.")
                return

            item = (filter_cate_text, item_text[0], item_text[1], amount)
            self.select_treeview.insert("", "end", values=item)
    
    def on_select_treeview_click(self, event):
        selected_item = self.select_treeview.focus()
        if selected_item:
            item_values = self.select_treeview.item(selected_item, 'values')
            self.entry_amount.delete(0, tk.END)
            self.entry_amount.insert(0, item_values[3])  # Assume the Amount is at index 3

    def update_amount(self):
        selected_item = self.select_treeview.focus()
        if selected_item:
            try:
                new_amount = float(self.entry_amount.get())
            except ValueError:
                messagebox.showerror("Input Error", "Please enter a valid float value in the amount field.")
                return
        
        # Update the selected item's amount in the treeview
            item_values = list(self.select_treeview.item(selected_item, 'values'))
            item_values[3] = new_amount  # Update the Amount
            self.select_treeview.item(selected_item, values=item_values)



    def delete_profile_item(self):
        selected_item = self.select_treeview.focus()  # Get the item that is currently selected
        if  selected_item:  # If an item is selected
            self.select_treeview.delete(selected_item)