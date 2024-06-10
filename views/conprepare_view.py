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

    def show_profile(self, profile1, profile2, rawmats_1, transpots_1, performances_1, rawmats_2, transpots_2, performances_2):

        # Check if any of the data is None
        if rawmats_1 is None or transpots_1 is None or performances_1 is None or rawmats_2 is None or transpots_2 is None or performances_2 is None:
            messagebox.showerror("Error", "Data is missing")
            return

        # แสดงข้อมูลโปรไฟล์ที่เลือกใน Label
        self.label_profile1.config(text=profile1)
        self.label_profile2.config(text=profile2)

        # Clear existing data in the treeview
        self.profile1_treeview.delete(*self.profile1_treeview.get_children())
        self.profile2_treeview.delete(*self.profile2_treeview.get_children())

        # Insert raw materials data for profile 1
        for rawmat in rawmats_1:
            self.profile1_treeview.insert("", "end", values=(rawmat[0], round(float(rawmat[1]) * float(rawmat[2]), 3), "KgCO2eq"))

        # Insert transportation data for profile 1
        for transpot in transpots_1:
            self.profile1_treeview.insert("", "end", values=(transpot[0], round(float(transpot[1]) * float(transpot[2]), 3), "KgCO2eq"))

        # Insert performances data for profile 1
        for performance in performances_1:
            self.profile1_treeview.insert("", "end", values=(performance[0], round(float(performance[1]) * float(performance[2]), 3), "KgCO2eq"))

        # Insert raw materials data for profile 2
        for rawmat in rawmats_2:
            self.profile2_treeview.insert("", "end", values=(rawmat[0], round(float(rawmat[1]) * float(rawmat[2]), 3), "KgCO2eq"))

        # Insert transportation data for profile 2
        for transpot in transpots_2:
            self.profile2_treeview.insert("", "end", values=(transpot[0], round(float(transpot[1]) * float(transpot[2]), 3), "KgCO2eq"))

        # Insert performances data for profile 2
        for performance in performances_2:
            self.profile2_treeview.insert("", "end", values=(performance[0], round(float(performance[1]) * float(performance[2]), 3), "KgCO2eq"))


    
    
