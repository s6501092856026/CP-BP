import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import openpyxl.drawing
import openpyxl.drawing.image
import openpyxl.styles
import pandas as pd
import openpyxl
from io import BytesIO
from utils.database import DatabaseUtil

class ConprepareView(ttk.Frame):

    def __init__(self, controller, app):
        super().__init__(app)
        self.controller = controller
        self.items = []

        # Window
        self.main_frame =  ttk.Frame(self)

        self.label_name1 = ttk.Label(self, text = "โปรไฟล์ที่หนึ่ง")
        self.label_name1.grid(row=0, column=0, padx=10, pady=10, sticky='NW')

        self.label_profile1 = ttk.Label(self, text = "")
        self.label_profile1.grid(row=0, column=0, padx=10, pady=10, sticky='N')

        self.label_name2 = ttk.Label(self, text = "โปรไฟล์ที่สอง")
        self.label_name2.grid(row=0, column=1, padx=10, pady=10, sticky='NW')

        self.label_profile2 = ttk.Label(self, text = "")
        self.label_profile2.grid(row=0, column=1, padx=10, pady=10, sticky='N')

        self.label_totalcf = ttk.Label(self, text = "ส่วนต่างค่าคาร์บอนเทียบเท่า", font=("Times New Roman", 10, "bold"))
        self.label_totalcf.grid(row=7,column=0, padx=10, pady=10, sticky='W')

        self.label_cf = ttk.Label(self, text = "0")
        self.label_cf.grid(row=7,column=0, padx=10, pady=10, sticky = 'E')

        self.label_unit = ttk.Label(self, text = "หน่วย", font=("Times New Roman", 10, "bold"))
        self.label_unit.grid(row=7,column=1, padx=10, pady=10, sticky = 'W')
        
        self.return_button = ttk.Button(self, text="Return to Profile", command=self.back)
        self.return_button.grid(row=8, column=0, padx=10, pady=10, ipadx=10, ipady=10, sticky = 'W')

        self.export_button = ttk.Button(self, text="Export to Excel") # , command=self.export
        self.export_button.grid(row=8, column=1, padx=10, pady=10, ipadx=10, ipady=10, sticky = 'E')

        # TREE VIEW
        self.profile1_treeview = ttk.Treeview(self, columns=("Name", "Carbon", "Unit"), show="headings")
        self.profile1_treeview.heading("Name", text="ชื่อ")
        self.profile1_treeview.column("Name", width=310)
        self.profile1_treeview.heading("Carbon", text="ค่าคาร์บวนเทียบเท่า")
        self.profile1_treeview.column("Carbon", width=95)
        self.profile1_treeview.heading("Unit", text="หน่วย")
        self.profile1_treeview.column("Unit", width=60)
        self.profile1_treeview.grid(row=3, rowspan=2, column=0, padx=5, pady=5)

        self.profile2_treeview = ttk.Treeview(self, columns=("Name", "Carbon", "Unit"), show="headings")
        self.profile2_treeview.heading("Name", text="ชื่อ")
        self.profile2_treeview.column("Name", width=310)
        self.profile2_treeview.heading("Carbon", text="ค่าคาร์บอนเทียบเท่า")
        self.profile2_treeview.column("Carbon", width=95)
        self.profile2_treeview.heading("Unit", text="หน่วย")
        self.profile2_treeview.column("Unit", width=60)
        self.profile2_treeview.grid(row=3, rowspan=2, column=1, padx=5, pady=5)
        
    def back(self):
        self.controller.back_main()

    def show_profile(self, profile1, profile2, rawmats, transpots, performances):

        # Check if any of the data is None
        if rawmats is None or transpots is None or performances is None:
            messagebox.showerror("Error", "Data is missing")
            return
        # แสดงข้อมูลโปรไฟล์ที่เลือกใน Label
        self.label_profile1.config(text=profile1)
        self.label_profile2.config(text=profile2)

        
        # Clear existing data in the treeview
        self.profile1_treeview.delete(*self.profile1_treeview.get_children())
        
        # Insert raw materials data
        for rawmat in rawmats:
            self.profile1_treeview.insert("", "end", values=(rawmat[0], rawmat[1] * rawmat[2], rawmat[3]))

        # Insert transportation data
        for transpot in transpots:
            self.profile1_treeview.insert("", "end", values=(transpot[0], transpot[1] * transpot[2], transpot[3]))

        # Insert performances data
        for performance in performances:
            self.profile1_treeview.insert("", "end", values=(performance[0], performance[1] * performance[2], performance[3]))

    def show_treeview(self, product_name):
        db = DatabaseUtil.getInstance()
        existing_product = db.fetch_data("SELECT product_id FROM product p WHERE p.product_name = %s", (product_name,))
    
        # ตรวจสอบว่ามีผลิตภัณฑ์ที่ตรงกับชื่อหรือไม่
        if existing_product:
            product_id = existing_product[0][0]
        
            # ดึงข้อมูล raw materials ที่เกี่ยวข้องกับผลิตภัณฑ์
            rawmats = db.fetch_data("SELECT name_raw, carbon_per_raw, amount, unit_raw FROM product p, product_rawmat pr, raw_mat r WHERE p.product_id = pr.product_id AND pr.rawmat_id = r.rawmat_id AND p.product_id = "+ product_id)
        
            # ดึงข้อมูล transportation ที่เกี่ยวข้องกับผลิตภัณฑ์
            transpots = db.fetch_data("SELECT transpot_name, carbon_per_transpot, amount, unit_transpot FROM product p, product_transpotation pt, transpotation t WHERE p.product_id = pt.product_id AND pt.transpot_id = t.transpot_id AND p.product_id = "+ product_id)
        
            # ดึงข้อมูล performances ที่เกี่ยวข้องกับผลิตภัณฑ์
            performances = db.fetch_data("SELECT performance_name, carbon_per_performance, amount, unit_performance FROM product p, product_performance pf, performance f WHERE p.product_id = pf.product_id AND pf.performance_id = f.performance_id AND p.product_id = "+ product_id)
            # อัปเดต view ด้วยข้อมูลที่ดึงมา
            self.controller.show_profile(rawmats, transpots, performances)

    # def update_data(self, rawmats, transpots, performances):
    #     # Clear existing data in the treeview
    #     self.profile1_treeview.delete(*self.profile1_treeview.get_children())
        
    #     # Insert raw materials data
    #     for rawmat in rawmats:
    #         self.profile1_treeview.insert("", "end", values=(rawmat[0], rawmat[1] * rawmat[2], rawmat[3]))

    #     # Insert transportation data
    #     for transpot in transpots:
    #         self.profile1_treeview.insert("", "end", values=(transpot[0], transpot[1] * transpot[2], transpot[3]))

    #     # Insert performances data
    #     for performance in performances:
    #         self.profile1_treeview.insert("", "end", values=(performance[0], performance[1] * performance[2], performance[3]))
    
