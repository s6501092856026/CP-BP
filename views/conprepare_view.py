import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import pandas as pd
from io import BytesIO

class ConprepareView(ttk.Frame):

    def __init__(self, controller, app):
        super().__init__(app)
        self.controller = controller
        self.items = []

        self.style = ttk.Style()
        self.style.configure("My.TFrame", background='#ADD8E6')

        # Window
        self.main_frame =  ttk.Frame(self)

        self.label_profile1 = ttk.Label(self, borderwidth=1, relief="ridge", text = "", justify='center')
        self.label_profile1.grid(row=2, column=0, sticky='NSWE')
        self.label_profile1.configure(anchor='center', background='#ADD8E6')

        self.label_profile2 = ttk.Label(self, borderwidth=1, relief="ridge", text = "", justify='center')
        self.label_profile2.grid(row=2, column=1, sticky='NSWE')
        self.label_profile2.configure(anchor='center', background='#ADD8E6')

        frame_cf = ttk.Frame(self, borderwidth=1, relief="ridge", style="My.TFrame")
        frame_cf.grid(row=4, column=0, padx=10, pady=10)

        self.label_percentcf = ttk.Label(frame_cf, text = "ส่วนต่างค่าคาร์บอนเทียบเท่า")
        self.label_percentcf.grid(row=0,column=0, padx=20, pady=10, sticky='W')
        self.label_percentcf.configure(anchor='w', background='#ADD8E6')

        self.label_cf = ttk.Label(frame_cf, text = "")
        self.label_cf.grid(row=0,column=1, padx=20, pady=10, sticky = 'E')
        self.label_cf.configure(anchor='e', background='#ADD8E6')
        
        self.return_button = ttk.Button(self, text="Return to Profile", command=self.back)
        self.return_button.grid(row=4, column=1, padx=10, pady=10, ipadx=10, ipady=10, sticky = 'W')

        self.export_button = ttk.Button(self, text="Export to Excel") # , command=self.export
        self.export_button.grid(row=4, column=1, padx=10, pady=10, ipadx=10, ipady=10, sticky = 'E')

        # TREE VIEW
        self.profile1_treeview = ttk.Treeview(self, columns=("Name", "Carbon", "Unit"), show="headings")
        self.profile1_treeview.heading("Name", text="ชื่อ")
        self.profile1_treeview.column("Name", width=310, stretch=True)
        text_width = len("ค่าคาร์บอนเทียบเท่า (Y)")  # คำนวณความยาวของข้อความ
        self.profile1_treeview.heading("Carbon", text="คาร์บอนเทียบเท่า (Y)")
        self.profile1_treeview.column("Carbon", width=text_width * 5)
        self.profile1_treeview.heading("Unit", text="หน่วย")
        self.profile1_treeview.column("Unit", width=60, stretch=True)
        self.profile1_treeview.grid(row=3, column=0)

        self.profile2_treeview = ttk.Treeview(self, columns=("Name", "Carbon", "Unit"), show="headings")
        self.profile2_treeview.heading("Name", text="ชื่อ")
        self.profile2_treeview.column("Name", width=310, stretch=True)
        text_width = len("ค่าคาร์บอนเทียบเท่า (Y)")  # คำนวณความยาวของข้อความ
        self.profile2_treeview.heading("Carbon", text="คาร์บอนเทียบเท่า (Y)")
        self.profile2_treeview.column("Carbon", width=text_width * 5)
        self.profile2_treeview.heading("Unit", text="หน่วย")
        self.profile2_treeview.column("Unit", width=60, stretch=True)
        self.profile2_treeview.grid(row=3, column=1)
        
    def back(self):
        self.controller.back_main()

    def setCompareGraph(self, profile1, profile2):
        # สร้างภาพ Matplotlib
        figure = Figure(figsize=(6.5, 3.75), dpi=70)
        subplot = figure.add_subplot(111)

        # ดึงและรวมค่า "คาร์บอน" จากข้อมูลโปรไฟล์ 1 และ 2
        x_labels = [profile1, profile2]
        y_values = [0, 0]

        # รวมค่าคาร์บอนสำหรับโปรไฟล์ 1
        for item in self.profile1_treeview.get_children():
            y_values[0] += float(self.profile1_treeview.item(item, "values")[1])  # สมมติว่า "Carbon" เป็นคอลัมน์ที่สอง

        # รวมค่าคาร์บอนสำหรับโปรไฟล์ 2
        for item in self.profile2_treeview.get_children():
            y_values[1] += float(self.profile2_treeview.item(item, "values")[1])  # สมมติว่า "Carbon" เป็นคอลัมน์ที่สอง

        # กำหนดสีของแท่งกราฟ
        bar_colors = ['blue', 'green']  # คุณสามารถกำหนดสีอื่น ๆ ตามต้องการได้

        # สร้างกราฟแท่งโดยใช้สีต่าง ๆ สำหรับแต่ละแท่ง
        subplot.bar(x_labels, y_values, color=bar_colors, width=0.25)

        # เพิ่มเส้นกริด
        subplot.grid(True, linestyle='--', linewidth=0.5)

        # เพิ่มหัวเรื่อง
        subplot.set_title('Comparison of Profiles', fontsize=8, fontweight='bold', color='black')

        # เพิ่มป้ายกำกับแกน
        subplot.set_xlabel('Profile', fontsize=8, color='black')
        subplot.set_ylabel('KgCO2eq', fontsize=8, color='black')

        # ปรับแต่งเส้นขอบ
        subplot.spines['top'].set_visible(False)
        subplot.spines['right'].set_visible(False)
        subplot.spines['left'].set_color('black')
        subplot.spines['bottom'].set_color('black')

        # กำหนดเส้นและป้ายกำกับในแกน y
        subplot.set_xticks(range(len(x_labels)))
        subplot.set_xticklabels(x_labels)

        # กำหนดแบบอักษรและสีของเส้น
        subplot.tick_params(axis='both', which='major', labelsize=8, colors='black')

        # สร้างเฟรมสำหรับกราฟ
        frame = tk.Frame(self, highlightbackground='black', highlightthickness=1, borderwidth=1, relief="ridge")
        frame.grid(row=0, rowspan=2, column=0, sticky="nsew")

        # สร้างวิดเจ็ต FigureCanvasTkAgg
        canvas = FigureCanvasTkAgg(figure, master=frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    # def setCompareGraph(self, profile1, profile2):
    #     # สร้างภาพ Matplotlib
    #     figure = Figure(figsize=(6.5, 3.5), dpi=70)
    #     subplot = figure.add_subplot(111)

    #     # ดึงและรวมค่า "คาร์บอน" จากข้อมูลโปรไฟล์ 1 และ 2
    #     x_labels = [profile1, profile2]
    #     y_values = [0, 0]

    #     # รวมค่าคาร์บอนสำหรับโปรไฟล์ 1
    #     for item in self.profile1_treeview.get_children():
    #         y_values[0] += float(self.profile1_treeview.item(item, "values")[1])  # สมมติว่า "Carbon" เป็นคอลัมน์ที่สอง

    #     # รวมค่าคาร์บอนสำหรับโปรไฟล์ 2
    #     for item in self.profile2_treeview.get_children():
    #         y_values[1] += float(self.profile2_treeview.item(item, "values")[1])  # สมมติว่า "Carbon" เป็นคอลัมน์ที่สอง

    #     # กำหนดสีของแท่งกราฟ
    #     bar_colors = ['blue', 'green']  # คุณสามารถกำหนดสีอื่น ๆ ตามต้องการได้

    #     # สร้างกราฟแท่งโดยใช้สีต่าง ๆ สำหรับแต่ละแท่ง
    #     subplot.bar(x_labels, y_values, color=bar_colors, width=0.25)

    #     # เพิ่มเส้นกริด
    #     subplot.grid(True, linestyle='--', linewidth=0.5)

    #     # เพิ่มหัวเรื่อง
    #     subplot.set_title('Prepare of Profile', fontsize=8, fontweight='bold', color='black')

    #     # เพิ่มป้ายกำกับแกน
    #     subplot.set_xlabel('Profile', fontsize=8, color='black')
    #     subplot.set_ylabel('KgCO2eq', fontsize=8, color='black')

    #     # ปรับแต่งเส้นขอบ
    #     subplot.spines['top'].set_visible(False)
    #     subplot.spines['right'].set_visible(False)
    #     subplot.spines['left'].set_color('black')
    #     subplot.spines['bottom'].set_color('black')

    #     # กำหนดเส้นและป้ายกำกับในแกน y
    #     subplot.set_xticks(range(len(x_labels)))
    #     subplot.set_xticklabels(x_labels)

    #     # กำหนดแบบอักษรและสีของเส้น
    #     subplot.tick_params(axis='both', which='major', labelsize=8, colors='black')

    #     # สร้างวิดเจ็ต FigureCanvasTkAgg
    #     canvas = FigureCanvasTkAgg(figure, master=self)
    #     canvas.draw()
    #     canvas.get_tk_widget().grid(row=0, rowspan=2, column=0)

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

        self.setCompareGraph(profile1, profile2)
        self.updateLabel()

    def updateLabel(self):
        # Calculate total carbon emissions for profile 1
        total_carbon_profile1 = sum(float(self.profile1_treeview.item(item, "values")[1]) for item in self.profile1_treeview.get_children())

        # Calculate total carbon emissions for profile 2
        total_carbon_profile2 = sum(float(self.profile2_treeview.item(item, "values")[1]) for item in self.profile2_treeview.get_children())

        # Calculate percentage difference
        if total_carbon_profile1 != 0:
            percentage_difference = ((total_carbon_profile1 - total_carbon_profile2) / total_carbon_profile1) * 100
        else:
            percentage_difference = 0  # To handle division by zero

        # Update the label with the percentage difference
        self.label_cf.config(text=f"{percentage_difference:.2f}%")
        

    
    
