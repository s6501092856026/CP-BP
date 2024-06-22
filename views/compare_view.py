from tkinter import ttk, messagebox
from utils.database import DatabaseUtil
from controllers.tooltip_controller import ToolTipController

class CompareView(ttk.Frame):

    def __init__(self, controller, app):
        super().__init__(app)
        self.controller = controller

        self.style = ttk.Style()
        self.style.configure("My.TFrame", background='#C0E4F6')

        # Frame Top

        frame_top = ttk.Frame(self, borderwidth=1, relief="ridge", style='My.TFrame')
        frame_top.grid(row=0, column=0, columnspan=2, sticky='NSWE')

        self.back_button = ttk.Button(frame_top, text="ย้อนลับ", command=self.back)
        self.back_button.grid(row=0, column=0, padx=10, pady=10)

        # Frame Tool

        frame_tool = ttk.Frame(self, borderwidth=1, relief="ridge", style='My.TFrame')
        frame_tool.grid(row=1, column=1, sticky='NS')

        self.label_profile1 = ttk.Label(frame_tool, text="โปรไฟล์ที่หนึ่ง", background='#C0E4F6')
        self.label_profile1.grid(row=0, column=0, padx=10, pady=5, sticky='N')

        self.entry_profile1 = ttk.Entry(frame_tool)
        self.entry_profile1.grid(row=1, column=0, padx=10, pady=10, sticky='S')

        self.label_profile2 = ttk.Label(frame_tool, text="โปรไฟล์ที่สอง", background='#C0E4F6')
        self.label_profile2.grid(row=2, column=0, padx=10, pady=5, sticky='N')

        self.entry_profile2 = ttk.Entry(frame_tool)
        self.entry_profile2.grid(row=3, column=0, padx=10, pady=10, sticky='S')

        self.add_button = ttk.Button(frame_tool, text="เพิ่ม", command=self.add_profile)
        self.add_button.grid(row=4, column=0, padx=10, pady=20, sticky='')

        self.complete_button = ttk.Button(frame_tool, text="เสร็จสิ้น", command=self.complete)
        self.complete_button.grid(row=5, column=0, padx=10, pady=45, ipadx=10, ipady=15)

        # Frame 
        frame_treeview = ttk.Frame(self, borderwidth=1, relief="ridge", style='My.TFrame')
        frame_treeview.grid(row=1, column=0)

        self.list_treeview = ttk.Treeview(frame_treeview, columns=("ID", "Name"), show="headings")
        self.list_treeview.heading("ID", text="ไอดี")
        self.list_treeview.column("ID", width=30, stretch=True)
        self.list_treeview.heading("Name", text="ชื่อโปรไฟล์")
        self.list_treeview.column("Name", width=150, stretch=True)
        self.list_treeview.grid(row=0, column=0, ipady=55)

        self.list_treeview.bind("<<TreeviewSelect>>", lambda event: self.get_selected_item())

        # สร้าง Scrollbar แนวแกน Y
        scroll_y = ttk.Scrollbar(frame_treeview, orient='vertical', command=self.list_treeview.yview)
        self.list_treeview.configure(yscrollcommand=scroll_y.set)
        scroll_y.grid(row=0, column=1, sticky='NS')

        self.grid_rowconfigure(0, weight=1)

        self.detail_treeview = ttk.Treeview(frame_treeview, columns=("Detail", "Emission Factor", "Amount", "Unit"), show="headings")
        self.detail_treeview.heading("Detail", text="ชื่อ")
        self.detail_treeview.column("Detail", width=370, stretch=True)
        self.detail_treeview.heading("Emission Factor", text="ปัจจัยการปล่อย")
        self.detail_treeview.column("Emission Factor", width=85, stretch=True)
        self.detail_treeview.heading("Amount", text="ปริมาณ")
        self.detail_treeview.column("Amount", width=50, stretch=True)
        self.detail_treeview.heading("Unit", text="หน่วย")
        self.detail_treeview.column("Unit", width=40, stretch=True)
        self.detail_treeview.grid(row=0, column=2, ipady=55)

        # สร้าง Scrollbar แนวแกน Y
        scroll_y = ttk.Scrollbar(frame_treeview, orient='vertical', command=self.detail_treeview.yview)
        self.detail_treeview.configure(yscrollcommand=scroll_y.set)
        scroll_y.grid(row=0, column=3, sticky='NS')

        self.grid_rowconfigure(0, weight=1)

        self.add_button_tooltips()

    def add_button_tooltips(self):
        ToolTipController(self.add_button, "เพิ่มรายการ")
        ToolTipController(self.complete_button, "ไปหน้าประมวลผลข้อมูล")
        ToolTipController(self.back_button, "กลับไปยังหน้าหลัก")

    def back(self):
        self.controller.back_main()
        
    def set_profile(self, products):
        self.list_treeview.delete(*self.list_treeview.get_children())

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

    def add_profile(self):
        selected_item = self.list_treeview.focus()
        if selected_item:
            item_text = self.list_treeview.item(selected_item, 'values')
            name = item_text[1]

            if not self.entry_profile1.get():
                self.entry_profile1.insert(0, name)
            elif name != self.entry_profile1.get() and name != self.entry_profile2.get():
                self.entry_profile2.insert(0, name)
            else:
                messagebox.showwarning("คำเตือน", "โปรไฟล์นี้ถูกเพิ่มแล้ว")

    def complete(self):
        profile1 = self.entry_profile1.get()
        profile2 = self.entry_profile2.get()

        if not profile1 or not profile2:
            messagebox.showwarning("คำเตือน", "โปรดเลือกโปรไฟล์ที่หนึ่งและโปรไฟล์ที่สองก่อนดำเนินการ")
            return

        db = DatabaseUtil.getInstance()
    
        # ค้นหา product_id จาก database โดยอ้างอิงจาก product_name ที่รับจาก entry_profile1 และ entry_profile2
        product1_id = db.fetch_data("SELECT product_id FROM product WHERE product_name = %s", (profile1,))
        product2_id = db.fetch_data("SELECT product_id FROM product WHERE product_name = %s", (profile2,))

        if product1_id and product2_id:
            # ค้นหาข้อมูลเพิ่มเติมตาม product_id
            raw_data_1 = db.fetch_data("SELECT name_raw, carbon_per_raw, amount FROM product_rawmat pr, raw_mat r WHERE pr.rawmat_id = r.rawmat_id AND pr.product_id = %s", (product1_id[0][0],))
            trans_data_1 = db.fetch_data("SELECT transpot_name, carbon_per_transpot, amount FROM product_transpotation pt, transpotation t WHERE pt.transpot_id = t.transpot_id AND pt.product_id = %s", (product1_id[0][0],))
            perf_data_1 = db.fetch_data("SELECT performance_name, carbon_per_performance, amount FROM product_performance pf, performance f WHERE pf.performance_id = f.performance_id AND pf.product_id = %s", (product1_id[0][0],))

            raw_data_2 = db.fetch_data("SELECT name_raw, carbon_per_raw, amount FROM product_rawmat pr, raw_mat r WHERE pr.rawmat_id = r.rawmat_id AND pr.product_id = %s", (product2_id[0][0],))
            trans_data_2 = db.fetch_data("SELECT transpot_name, carbon_per_transpot, amount FROM product_transpotation pt, transpotation t WHERE pt.transpot_id = t.transpot_id AND pt.product_id = %s", (product2_id[0][0],))
            perf_data_2 = db.fetch_data("SELECT performance_name, carbon_per_performance, amount FROM product_performance pf, performance f WHERE pf.performance_id = f.performance_id AND pf.product_id = %s", (product2_id[0][0],))

            # self.controller.show_conprepare((profile1, raw_data_1, trans_data_1, perf_data_1), (profile2, raw_data_2, trans_data_2, perf_data_2))
            breakpoint_data1 = self.load_breakpoint_data1(profile1)
            breakpoint_data2 = self.load_breakpoint_data2(profile2)
            self.controller.show_conprepare(profile1, profile2, raw_data_1, trans_data_1, perf_data_1, raw_data_2, trans_data_2, perf_data_2, breakpoint_data1, breakpoint_data2)
    
    def load_breakpoint_data1(self, profile1):
        db = DatabaseUtil.getInstance()
        existing_product = db.fetch_data("SELECT product_id FROM product WHERE product_name = %s", (profile1,))
        print("Existing Product Data:", existing_product)
        if existing_product:
            product_id = existing_product[0][0]
            # Fetch data from the breakeven_point table related to product_id
            breakpoint_data1 = db.fetch_data("SELECT fixed_cost, variable_cost, number_of_units, unit_price, product_efficiency FROM breakeven_point WHERE product_id = %s", (product_id,))
            return breakpoint_data1

    def load_breakpoint_data2(self, profile2):
        db = DatabaseUtil.getInstance()
        existing_product = db.fetch_data("SELECT product_id FROM product WHERE product_name = %s", (profile2,))
        print("Existing Product Data:", existing_product)
        if existing_product:
            product_id = existing_product[0][0]
            # Fetch data from the breakeven_point table related to product_id
            breakpoint_data2 = db.fetch_data("SELECT fixed_cost, variable_cost, number_of_units, unit_price, product_efficiency FROM breakeven_point WHERE product_id = %s", (product_id,))
            return breakpoint_data2
