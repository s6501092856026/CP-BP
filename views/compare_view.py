import tkinter as tk
from tkinter import ttk, messagebox
from utils.database import DatabaseUtil

class CompareView(ttk.Frame):

    def __init__(self, controller, app):
        super().__init__(app)
        self.controller = controller

        self.style = ttk.Style()
        self.style.configure("My.TFrame", background='#ADD8E6')

        # Window

        self.back_button = ttk.Button(self, text="ย้อนลับ", command=self.back)
        self.back_button.grid(row=0, column=0, pady=10, sticky='SW')

        # Frame Tool

        frame_tool = ttk.Frame(self, borderwidth=1, relief="ridge", style='My.TFrame')
        frame_tool.grid(row=1, column=1, sticky='NS')

        self.label_profile1 = ttk.Label(frame_tool, text="โปรไฟล์ที่หนึ่ง", background='#ADD8E6')
        self.label_profile1.grid(row=0, column=0, padx=10, pady=5, sticky='N')

        self.entry_profile1 = ttk.Entry(frame_tool)
        self.entry_profile1.grid(row=1, column=0, padx=10, pady=10, sticky='S')

        self.label_profile2 = ttk.Label(frame_tool, text="โปรไฟล์ที่สอง", background='#ADD8E6')
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
        self.list_treeview.column("ID", width=10, stretch=True)
        self.list_treeview.heading("Name", text="ชื่อโปรไฟล์")
        self.list_treeview.column("Name", width=200, stretch=True)
        self.list_treeview.grid(row=0, column=0, ipadx=40, ipady=75)

        self.list_treeview.bind("<<TreeviewSelect>>", lambda event: self.get_selected_item())

        # สร้าง Scrollbar แนวแกน Y
        scroll_y = ttk.Scrollbar(frame_treeview, orient='vertical', command=self.list_treeview.yview)
        self.list_treeview.configure(yscrollcommand=scroll_y.set)
        scroll_y.grid(row=0, column=1, sticky='NS')

        self.grid_rowconfigure(0, weight=1)

        self.detail_treeview = ttk.Treeview(frame_treeview, columns=("Detail", "Emission Factor", "Amount", "Unit"), show="headings")
        self.detail_treeview.heading("Detail", text="ชื่อ")
        self.detail_treeview.column("Detail", width=310, stretch=True)
        self.detail_treeview.heading("Emission Factor", text="ค่าสัมประสิทธิ์")
        self.detail_treeview.column("Emission Factor", width=80, stretch=True)
        self.detail_treeview.heading("Amount", text="ปริมาณ")
        self.detail_treeview.column("Amount", width=50, stretch=True)
        self.detail_treeview.heading("Unit", text="หน่วย")
        self.detail_treeview.column("Unit", width=40, stretch=True)
        self.detail_treeview.grid(row=0, column=2, ipadx=100, ipady=75)

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
            name = (item_text[1])

            if not self.entry_profile1.get():
                self.entry_profile1.insert(0, name)
            else:
                self.entry_profile2.insert(0, name)
    
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
            self.controller.show_conprepare(profile1, profile2, raw_data_1, trans_data_1, perf_data_1, raw_data_2, trans_data_2, perf_data_2)
