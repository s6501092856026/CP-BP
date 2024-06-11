import tkinter as tk
from tkinter import ttk, Radiobutton, messagebox
from controllers.tooltip_controller import ToolTipController
from utils.database import DatabaseUtil

class NewprofileView(ttk.Frame):

    def __init__(self, controller, app):
        super().__init__(app)
        self.controller = controller
        
        self.style = ttk.Style()
        self.style.configure("My.TFrame", background='#ADD8E6')

        self.radio_state = tk.IntVar(value=1)

        # Frame Fliter
        frame_fliter = ttk.Frame(self, borderwidth=1, relief="ridge", style='My.TFrame')
        frame_fliter.grid(row=0, column=0, sticky='WE')

        self.back_button = ttk.Button(frame_fliter, text="ย้อนกลับ", command=self.back)
        self.back_button.grid(row=0, column=0, padx=5, pady=5)

        self.radio_material = Radiobutton(frame_fliter, value=1, text="วัตถุดิบ", variable=self.radio_state, command=self.filter)
        self.radio_material.grid(row=0, column=1, padx=70, pady=10)
        self.radio_material.configure(font=('Tohama', 10, 'bold'), background='#ADD8E6')

        self.radio_transpot = Radiobutton(frame_fliter, value=2, text="การขนส่ง", variable=self.radio_state, command=self.filter)
        self.radio_transpot.grid(row=0, column=2, padx=70, pady=10)
        self.radio_transpot.configure(font=('Tohama', 10, 'bold'), background='#ADD8E6')

        self.radio_performance = Radiobutton(frame_fliter, value=3, text="กระบวนการ", variable=self.radio_state, command=self.filter)
        self.radio_performance.grid(row=0, column=3, padx=70, pady=10)
        self.radio_performance.configure(font=('Tohama', 10, 'bold'), background='#ADD8E6')

        self.combo_box = ttk.Combobox(frame_fliter,)
        self.combo_box.grid(row=0, column=4, padx=60, pady=10)
        self.combo_box.bind("<<ComboboxSelected>>", self.filter)

        # Frame Button
        frame_button = ttk.Frame(self, borderwidth=1, relief="ridge", style='My.TFrame')
        frame_button.grid(row=0, rowspan=2, column=1, sticky='NS')

        self.entry_name = ttk.Entry(frame_button, text = "")
        self.entry_name.grid(row=0, column=0, padx=10, pady=10, sticky='EW')

        self.label_name = ttk.Label(frame_button, text = "ชื่อโปรไฟล์", background='#ADD8E6')
        self.label_name.grid(row=0, column=1, padx=10, pady=10, sticky= 'W')

        self.label_unit = ttk.Label(frame_button, text = "หน่วย", background='#ADD8E6')
        self.label_unit.grid(row=1, column=1, padx=10, pady=10, sticky='W')

        self.entry_amount = ttk.Entry(frame_button, text = "")
        self.entry_amount.grid(row=1, column=0, padx=10, pady=10, sticky='EW')

        self.add_button = ttk.Button(frame_button, text="เพิ่ม", command=self.add_profile_item)
        self.add_button.grid(row=2, column=0, padx=10, pady=10, ipady=2, sticky='WN')

        self.delete_button = ttk.Button(frame_button, text="ลบ", command=self.delete_profile_item)
        self.delete_button.grid(row=2, column=1, padx=10, pady=10, ipady=2, sticky='EN')

        self.update_button = ttk.Button(frame_button, text="อัพเดท", command=self.update_amount)
        self.update_button.grid(row=3, column=0, columnspan=2, padx=10, pady=10, ipadx=5, ipady=5 ,sticky='NEW')

        self.save_as_button = ttk.Button(frame_button, text="บันทึกเป็น", command=self.save_as_profile)
        self.save_as_button.grid(row=4, column=0, columnspan=2, padx=10, pady=40, ipadx=5, ipady=5, sticky='')
        
        self.complete_button = ttk.Button(frame_button, text="เสร็จสิ้น", command=self.show_complete)
        self.complete_button.grid(row=5, column=0, columnspan=2, padx=10, pady=20, ipadx=30, ipady=10, sticky='S')

        self.add_button_tooltips()
        
        # Frame Button
        frame_treeview = ttk.Frame(self, borderwidth=1, relief="ridge", style='My.TFrame')
        frame_treeview.grid(row=1, column=0, sticky='NS')

        # Budgets
        self.list_treeview = ttk.Treeview(frame_treeview, columns=("ID", "Name", "Emission Factor", "Unit"), show="headings")
        self.list_treeview.heading("ID", text="ไอดี")
        self.list_treeview.column("ID", width=30, stretch=True)
        self.list_treeview.heading("Name", text="ชื่อ")
        self.list_treeview.column("Name", width=310, stretch=True)
        self.list_treeview.heading("Emission Factor", text="ค่าสัมประสิทธิ์")
        self.list_treeview.column("Emission Factor", width=80, stretch=True)
        self.list_treeview.heading("Unit", text="หน่วย")
        self.list_treeview.column("Unit", width=40, stretch=True)
        self.list_treeview.grid(row=0, column=0, ipady=75)

        # สร้าง Scrollbar แนวแกน Y
        scroll_y = ttk.Scrollbar(frame_treeview, orient='vertical', command=self.list_treeview.yview)
        self.list_treeview.configure(yscrollcommand=scroll_y.set)
        scroll_y.grid(row=0, column=1, sticky='NS')

        self.grid_rowconfigure(0, weight=1)

        self.select_treeview = ttk.Treeview(frame_treeview, columns=('Type', "ID", "Name", "Emission Factor", "Amount", "Unit"), show="headings")
        self.select_treeview.heading('Type', text="ประแภท")
        self.select_treeview.column("Type", width=85, stretch=True)
        self.select_treeview.heading("ID", text="ไอดี" )
        self.select_treeview.column("ID", width=30, stretch=True)
        self.select_treeview.heading("Name", text="ชื่อ")
        self.select_treeview.column("Name", width=310, stretch=True)
        self.select_treeview.heading("Emission Factor", text="ค่าสัมประสิทธิ์")
        self.select_treeview.column("Emission Factor", width=80, stretch=True)
        self.select_treeview.heading("Amount", text="ปริมาณ")
        self.select_treeview.column("Amount", width=50, stretch=True)
        self.select_treeview.heading("Unit", text="หน่วย")
        self.select_treeview.column("Unit", width=40, stretch=True)
        self.select_treeview.grid(row=0, column=2, ipady=75)

        self.select_treeview.bind("<ButtonRelease-1>", self.on_select_treeview_click)

        # สร้าง Scrollbar แนวแกน Y
        scroll_y = ttk.Scrollbar(frame_treeview, orient='vertical', command=self.select_treeview.yview)
        self.select_treeview.configure(yscrollcommand=scroll_y.set)
        scroll_y.grid(row=0, column=3, sticky='NS')

        self.grid_rowconfigure(0, weight=1)

    def add_button_tooltips(self):
        ToolTipController(self.add_button, "เพิ่มรายการ")
        ToolTipController(self.delete_button, "ลบรายการ")
        ToolTipController(self.save_as_button, "บันทึกโปรไฟล์")
        ToolTipController(self.complete_button, "ไปหน้าประมวลผลข้อมูล")
        ToolTipController(self.update_button, "อัพเดทรายการ")
        ToolTipController(self.back_button, "กลับไปยังหน้าหลัก")

    def filter(self, event = None):
        
        # radio button
        filter_cate = self.radio_state.get()
        
        # combobox
        filter_type = self.combo_box.get()
        self.controller.show_profile_name(filter_cate, filter_type)

    def back(self):
        self.select_treeview.delete(*self.select_treeview.get_children())
        self.controller.back_main()

    def show_detail_view(self):
        self.controller.show_detail_view()

    def show_complete(self):
        profile_name = self.entry_name.get()
        if not profile_name:
            messagebox.showwarning("แจ้งเตือน", "โปรดใส่ชื่อในช่องชื่อโปรไฟล์")
            return
    
        items = []
        children = self.select_treeview.get_children()
        for child in children:
            items.append(self.select_treeview.item(child)['values'])

        breakpoint_data = self.load_breakpoint_data(profile_name)
        self.controller.show_connew(profile_name, items, breakpoint_data)

    def load_breakpoint_data(self, profile_name):
        db = DatabaseUtil.getInstance()
        existing_product = db.fetch_data("SELECT product_id FROM product WHERE product_name = %s", (profile_name,))
        print("Existing Product Data:", existing_product)
        if existing_product:
            product_id = existing_product[0][0]
            # Fetch data from the breakeven_point table related to product_id
            breakpoint_data = db.fetch_data("SELECT fixed_cost, variable_cost, number_of_units, unit_price, product_efficiency FROM breakeven_point WHERE product_id = %s", (product_id,))
            return breakpoint_data

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
        if selected_item:  # If an item is selected
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
                messagebox.showerror("ข้อผิดพลาดในการป้อนข้อมูล", "กรุณาใส่ค่าในช่องปริมาณ")
                return

            try:
                amount = float(amount)
            except ValueError:
                messagebox.showerror("ข้อผิดพลาดในการป้อนข้อมูล", "กรุณาใส่ค่าที่เป็นจำนวนทศนิยมที่ถูกต้องในช่องปริมาณ")
                return

            item = (filter_cate_text, item_text[0], item_text[1], item_text[2], amount, item_text[3])
            self.select_treeview.insert("", "end", values=item)
            # เรียกใช้ฟังก์ชัน update_amount() เพื่ออัปเดตค่าของรายการที่เพิ่มล่าสุด
            self.update_amount()

    def on_select_treeview_click(self, event):
        selected_item = self.select_treeview.focus()
        if selected_item:
            item_values = self.select_treeview.item(selected_item, 'values')
            self.entry_amount.delete(0, tk.END)
            self.entry_amount.insert(0, item_values[4])  # Assume the Amount is at index 4

    def update_amount(self):
        selected_item = self.select_treeview.focus()
        if selected_item:
            try:
                new_amount = float(self.entry_amount.get())
            except ValueError:
                messagebox.showerror("ข้อผิดพลาดในการป้อนข้อมูล", "โปรดป้อนค่าทศนิยมที่ถูกต้องในช่องป้อนตัวเลข")
                return
        
        # Update the selected item's amount in the treeview
            item_values = list(self.select_treeview.item(selected_item, 'values'))
            item_values[4] = new_amount  # Update the Amount
            self.select_treeview.item(selected_item, values=item_values)

    def delete_profile_item(self):
        selected_item = self.select_treeview.focus()  # Get the item that is currently selected
        if  selected_item:  # If an item is selected
            self.select_treeview.delete(selected_item)

    def save_as_profile(self):
        profile_name = self.entry_name.get()
        items = [self.select_treeview.item(child)['values'] for child in self.select_treeview.get_children()]

        # ตรวจสอบจำนวนค่าใน items
        for item in items:
            if len(item) != 6:
                # แสดงข้อความข้อผิดพลาดหรือดำเนินการเพิ่มเติมตามที่เหมาะสม
                messagebox.showerror("ข้อผิดพลาด", "มีจำนวนค่าไม่ถูกต้องในรายการ")
                return
            
        self.controller.save_as_profile(profile_name, items)