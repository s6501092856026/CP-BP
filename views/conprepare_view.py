import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import openpyxl.drawing
import openpyxl.drawing.image
import openpyxl.styles
import openpyxl
from io import BytesIO
from controllers.tooltip_controller import ToolTipController
# import pandas as pd
# import matplotlib.pyplot as plt

class ConprepareView(ttk.Frame):

    def __init__(self, controller, app):
        super().__init__(app)
        self.controller = controller
        self.items = []

        self.style = ttk.Style()
        self.style.configure("My.TFrame", background='#ADD8E6')

        self.frame_break_visible = True
        self.frame_break2_visible = True

        # Window
        self.main_frame =  ttk.Frame(self)

        self.label_profile1 = ttk.Label(self, borderwidth=1, relief="ridge", text = "", justify='center')
        self.label_profile1.grid(row=2, column=0, sticky='NSWE')
        self.label_profile1.configure(anchor='center')

        self.label_profile2 = ttk.Label(self, borderwidth=1, relief="ridge", text = "", justify='center')
        self.label_profile2.grid(row=2, column=1, sticky='NSWE')
        self.label_profile2.configure(anchor='center')

        # Frame CF
        frame_cf = ttk.Frame(self, borderwidth=1, relief="ridge", style="My.TFrame")
        frame_cf.grid(row=3, column=0, sticky='NSWE')

        self.label_percentcf = ttk.Label(frame_cf, justify='center', text = "ส่วนต่างค่าคาร์บอน", font=('bold'))
        self.label_percentcf.grid(row=0, column=0, padx=20, pady=10, sticky='W')
        self.label_percentcf.configure(anchor='w', background='#ADD8E6')

        self.label_cf = ttk.Label(frame_cf, justify='center', text = "", font=('bold'))
        self.label_cf.grid(row=0, column=1, padx=20, pady=10, sticky = 'E')
        self.label_cf.configure(anchor='e', background='#FFFFCC')

        self.dif_percent = ttk.Label(frame_cf, text = "ส่วนต่างกำไร", font=('bold'))
        self.dif_percent.grid(row=1, column=0, padx=20, pady=10, sticky='W')
        self.dif_percent.configure(anchor='w', background='#ADD8E6')

        self.add_dif_percent = ttk.Label(frame_cf, text = "", font=('bold'))
        self.add_dif_percent.grid(row=1, column=1, padx=20, pady=10, sticky = 'E')
        self.add_dif_percent.configure(anchor='e', background='#FFFFCC')

        # Button
        self.return_button = ttk.Button(self, text="Return to Profile", command=self.back)
        self.return_button.grid(row=3, column=1, padx=10, pady=10, ipadx=10, ipady=10, sticky = 'W')

        self.export_button = ttk.Button(self, text="Export to Excel", command=self.export)
        self.export_button.grid(row=3, column=1, padx=10, pady=10, ipadx=10, ipady=10, sticky = 'E')

        # Frame Profile1
        frame_profile1 = ttk.Frame(self, borderwidth=1, relief="ridge", style="My.TFrame")
        frame_profile1.grid(row=1, column=0, sticky='NSWE')

        self.profile1_treeview = ttk.Treeview(frame_profile1, columns=("Name", "Carbon"), show="headings")
        self.profile1_treeview.heading("Name", text="ชื่อ")
        self.profile1_treeview.column("Name", width=370, stretch=True)
        text_width = len("ค่าคาร์บอน (Y)")  # คำนวณความยาวของข้อความ
        self.profile1_treeview.heading("Carbon", text="ค่าคาร์บอน (Y)")
        self.profile1_treeview.column("Carbon", width=text_width * 5)
        # self.profile1_treeview.heading("Unit", text="หน่วย")
        # self.profile1_treeview.column("Unit", width=60, stretch=True)
        self.profile1_treeview.grid(row=0, column=0)

        # สร้าง Scrollbar แนวแกน Y
        scroll_y = ttk.Scrollbar(frame_profile1, orient='vertical', command=self.profile1_treeview.yview)
        self.profile1_treeview.configure(yscrollcommand=scroll_y.set)
        scroll_y.grid(row=0, column=1, sticky='NS')

        self.grid_rowconfigure(0, weight=1)

        # Frame Profile2
        frame_profile2 = ttk.Frame(self, borderwidth=1, relief="ridge", style="My.TFrame")
        frame_profile2.grid(row=1, column=1, sticky='NSWE')

        self.profile2_treeview = ttk.Treeview(frame_profile2, columns=("Name", "Carbon"), show="headings") # , "Unit"
        self.profile2_treeview.heading("Name", text="ชื่อ")
        self.profile2_treeview.column("Name", width=370, stretch=True)
        text_width = len("ค่าคาร์บอน (Y)")  # คำนวณความยาวของข้อความ
        self.profile2_treeview.heading("Carbon", text="ค่าคา์บอน (Y)")
        self.profile2_treeview.column("Carbon", width=text_width * 5)
        # self.profile2_treeview.heading("Unit", text="หน่วย")
        # self.profile2_treeview.column("Unit", width=60, stretch=True)
        self.profile2_treeview.grid(row=0, column=0)

        # สร้าง Scrollbar แนวแกน Y
        scroll_y = ttk.Scrollbar(frame_profile2, orient='vertical', command=self.profile2_treeview.yview)
        self.profile2_treeview.configure(yscrollcommand=scroll_y.set)
        scroll_y.grid(row=0, column=1, sticky='NS')

        self.grid_rowconfigure(0, weight=1)

        # Frame Breakeven_point 1
        frame_break = ttk.Frame(self, borderwidth=1, relief="ridge", style="My.TFrame")
        frame_break.grid(row=0, column=2, sticky='NSWE')

        self.break_profile1 = ttk.Label(frame_break, text = "", borderwidth=1, relief="ridge")
        self.break_profile1.grid(row=0, column=0, columnspan=3, sticky='NSWE')
        self.break_profile1.configure(anchor='center')

        self.totalcost = ttk.Label(frame_break, text = "ต้นทุนรวม")
        self.totalcost.grid(row=1, column=0, padx=10, pady=10, sticky='W')
        self.totalcost.configure(anchor='w', background='#ADD8E6')

        self.revenue = ttk.Label(frame_break, text = "รายได้")
        self.revenue.grid(row=2, column=0, padx=10, pady=10, sticky='W')
        self.revenue.configure(anchor='w', background='#ADD8E6')
        
        self.profit = ttk.Label(frame_break, text = "กำไร")
        self.profit.grid(row=3, column=0, padx=10, pady=10, sticky='W')
        self.profit.configure(anchor='w', background='#ADD8E6')
        
        self.breakeven = ttk.Label(frame_break, text = "ปริมาณผลิตที่จุดคุ้มทุน")
        self.breakeven.grid(row=4, column=0, padx=10, pady=10, sticky='W')
        self.breakeven.configure(anchor='w', background='#ADD8E6')

        self.efficiency = ttk.Label(frame_break, text = "ประสิทธิภาพการผลิต")
        self.efficiency.grid(row=5, column=0, padx=10, pady=10, sticky='W')
        self.efficiency.configure(anchor='w', background='#ADD8E6')

        self.add_totalcost = ttk.Label(frame_break, text = "")
        self.add_totalcost.grid(row=1, column=1, padx=10, pady=10, sticky='E')
        self.add_totalcost.configure(anchor='w', background='#FFFFCC')

        self.add_revenue = ttk.Label(frame_break, text = "")
        self.add_revenue.grid(row=2, column=1, padx=10, pady=10, sticky='E')
        self.add_revenue.configure(anchor='w', background='#FFFFCC')

        self.add_profit = ttk.Label(frame_break, text = "")
        self.add_profit.grid(row=3, column=1, padx=10, pady=10, sticky='E')
        self.add_profit.configure(anchor='w', background='#FFFFCC')

        self.add_breakeven = ttk.Label(frame_break, text = "")
        self.add_breakeven.grid(row=4, column=1, padx=10, pady=10, sticky='E')
        self.add_breakeven.configure(anchor='w', background='#FFFFCC')

        self.add_efficiency = ttk.Label(frame_break, text = "")
        self.add_efficiency.grid(row=5, column=1, padx=10, pady=10, sticky='E')
        self.add_efficiency.configure(anchor='w', background='#FFFFCC')

        self.unit_totalcost = ttk.Label(frame_break, text = "บาท")
        self.unit_totalcost.grid(row=1, column=2, padx=10, pady=10)
        self.unit_totalcost.configure(anchor='e', background='#ADD8E6')

        self.unit_revenue = ttk.Label(frame_break, text = "บาท")
        self.unit_revenue.grid(row=2, column=2, padx=10, pady=10)
        self.unit_revenue.configure(anchor='e', background='#ADD8E6')

        self.unit_profit = ttk.Label(frame_break, text = "บาท")
        self.unit_profit.grid(row=3, column=2, padx=10, pady=10)
        self.unit_profit.configure(anchor='e', background='#ADD8E6')

        self.unit_breakeven = ttk.Label(frame_break, text = "หน่วย")
        self.unit_breakeven.grid(row=4, column=2, padx=10, pady=10)
        self.unit_breakeven.configure(anchor='e', background='#ADD8E6')

        self.unit_efficiency = ttk.Label(frame_break, text = "%")
        self.unit_efficiency.grid(row=5, column=2, padx=10, pady=10)
        self.unit_efficiency.configure(anchor='e', background='#ADD8E6')

        # Frame Breakeven_point 2
        frame_break2 = ttk.Frame(self, borderwidth=1, relief="ridge", style="My.TFrame")
        frame_break2.grid(row=1, column=2, sticky='NSWE')

        self.break_profile2 = ttk.Label(frame_break2, text = "", borderwidth=1, relief="ridge")
        self.break_profile2.grid(row=0, column=0, columnspan=3, sticky='NSWE')
        self.break_profile2.configure(anchor='center')
        
        self.totalcost2 = ttk.Label(frame_break2, text = "ต้นทุนรวม")
        self.totalcost2.grid(row=1, column=0, padx=10, pady=10, sticky='W')
        self.totalcost2.configure(anchor='w', background='#ADD8E6')

        self.revenue2 = ttk.Label(frame_break2, text = "รายได้")
        self.revenue2.grid(row=2, column=0, padx=10, pady=10, sticky='W')
        self.revenue2.configure(anchor='w', background='#ADD8E6')
        
        self.profit2 = ttk.Label(frame_break2, text = "กำไร")
        self.profit2.grid(row=3, column=0, padx=10, pady=10, sticky='W')
        self.profit2.configure(anchor='w', background='#ADD8E6')
        
        self.breakeven2 = ttk.Label(frame_break2, text = "ปริมาณผลิตที่จุดคุ้มทุน")
        self.breakeven2.grid(row=4, column=0, padx=10, pady=10, sticky='W')
        self.breakeven2.configure(anchor='w', background='#ADD8E6')

        self.efficiency2 = ttk.Label(frame_break2, text = "ประสิทธิภาพการผลิต")
        self.efficiency2.grid(row=5, column=0, padx=10, pady=10, sticky='W')
        self.efficiency2.configure(anchor='w', background='#ADD8E6')

        self.add_totalcost2 = ttk.Label(frame_break2, text = "")
        self.add_totalcost2.grid(row=1, column=1, padx=10, pady=10, sticky='E')
        self.add_totalcost2.configure(anchor='w', background='#FFFFCC')

        self.add_revenue2 = ttk.Label(frame_break2, text = "")
        self.add_revenue2.grid(row=2, column=1, padx=10, pady=10, sticky='E')
        self.add_revenue2.configure(anchor='w', background='#FFFFCC')

        self.add_profit2 = ttk.Label(frame_break2, text = "")
        self.add_profit2.grid(row=3, column=1, padx=10, pady=10, sticky='E')
        self.add_profit2.configure(anchor='w', background='#FFFFCC')

        self.add_breakeven2 = ttk.Label(frame_break2, text = "")
        self.add_breakeven2.grid(row=4, column=1, padx=10, pady=10, sticky='E')
        self.add_breakeven2.configure(anchor='w', background='#FFFFCC')

        self.add_efficiency2 = ttk.Label(frame_break2, text = "")
        self.add_efficiency2.grid(row=5, column=1, padx=10, pady=10, sticky='E')
        self.add_efficiency2.configure(anchor='w', background='#FFFFCC')

        self.unit_totalcost2 = ttk.Label(frame_break2, text = "บาท")
        self.unit_totalcost2.grid(row=1, column=2, padx=10, pady=10)
        self.unit_totalcost2.configure(anchor='e', background='#ADD8E6')

        self.unit_revenue2 = ttk.Label(frame_break2, text = "บาท")
        self.unit_revenue2.grid(row=2, column=2, padx=10, pady=10)
        self.unit_revenue2.configure(anchor='e', background='#ADD8E6')

        self.unit_profit2 = ttk.Label(frame_break2, text = "บาท")
        self.unit_profit2.grid(row=3, column=2, padx=10, pady=10)
        self.unit_profit2.configure(anchor='e', background='#ADD8E6')

        self.unit_breakeven2 = ttk.Label(frame_break2, text = "หน่วย")
        self.unit_breakeven2.grid(row=4, column=2, padx=10, pady=10)
        self.unit_breakeven2.configure(anchor='e', background='#ADD8E6')

        self.unit_efficiency2 = ttk.Label(frame_break2, text = "%")
        self.unit_efficiency2.grid(row=5, column=2, padx=10, pady=10)
        self.unit_efficiency2.configure(anchor='e', background='#ADD8E6')

        self.add_button_tooltips()

    def add_button_tooltips(self):
        ToolTipController(self.export_button, "ส่งออกไปยัง Excel")
        ToolTipController(self.return_button, "กลับไปยังหน้าหลัก")
        
    def back(self):
        self.controller.back_main()

    def set_breakpoint_data(self, breakpoint_data1, breakpoint_data2):
        revenue1 = None
        revenue2 = None
    
        if breakpoint_data1:
            fixed_cost, variable_cost, number_of_units, unit_price, product_efficiency = breakpoint_data1[0]
            total_cost1 = fixed_cost + (variable_cost * number_of_units)
            revenue1 = unit_price * number_of_units
            profit1 = revenue1 - total_cost1
            breakeven1 = fixed_cost / (unit_price - variable_cost)
        
            self.add_totalcost.config(text=f"{total_cost1:.2f}")
            self.add_revenue.config(text=f"{revenue1:.2f}")
            self.add_profit.config(text=f"{profit1:.2f}")
            self.add_breakeven.config(text=f"{breakeven1:.2f}")
            self.add_efficiency.config(text=f"{product_efficiency:.2f}")
        
        else:
            self.add_totalcost.config(text="-")
            self.add_revenue.config(text="-")
            self.add_profit.config(text="-")
            self.add_breakeven.config(text="-")
            self.add_efficiency.config(text="-")

        if breakpoint_data2:
            fixed_cost, variable_cost, number_of_units, unit_price, product_efficiency = breakpoint_data2[0]
            total_cost2 = fixed_cost + (variable_cost * number_of_units)
            revenue2 = unit_price * number_of_units
            profit2 = revenue2 - total_cost2
            breakeven2 = fixed_cost / (unit_price - variable_cost)
        
            self.add_totalcost2.config(text=f"{total_cost2:.2f}")
            self.add_revenue2.config(text=f"{revenue2:.2f}")
            self.add_profit2.config(text=f"{profit2:.2f}")
            self.add_breakeven2.config(text=f"{breakeven2:.2f}")
            self.add_efficiency2.config(text=f"{product_efficiency:.2f}")
        
        else:
            self.add_totalcost2.config(text="-")
            self.add_revenue2.config(text="-")
            self.add_profit2.config(text="-")
            self.add_breakeven2.config(text="-")
            self.add_efficiency2.config(text="-")

        # คำนวณและแสดงความแตกต่างเปอร์เซ็นต์ในรายได้หากมีทั้งสองรายได้ที่พร้อมใช้งาน
        if revenue1 is not None and revenue2 is not None:
            percentage_difference = ((revenue2 - revenue1) / revenue1) * 100
            if percentage_difference >= 0:
                self.add_dif_percent.config(text=f"+{percentage_difference:.2f}%")
            else:
                self.add_dif_percent.config(text=f"{percentage_difference:.2f}%")
        else:
            self.add_dif_percent.config(text="-")

    def setCompareGraph(self, profile1, profile2):
        # สร้างภาพ Matplotlib
        figure = Figure(figsize=(6.5, 3.25), dpi=70)
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

        

        # สร้างกราฟแท่งโดยใช้สีต่าง ๆ สำหรับแต่ละแท่ง
        subplot.bar(range(len(x_labels)), y_values, color=['blue', 'green'], width=0.1, align='center')

        # เพิ่มเส้นกริด
        subplot.grid(True, linestyle='--', linewidth=0.2)

        # เพิ่มหัวเรื่อง
        subplot.set_title('Comparison of Profiles', fontsize=8, fontweight='bold', color='black')

        
        subplot.set_ylabel('KgCO2eq', fontsize=8, color='black')

        # ปรับแต่งเส้นขอบ
        subplot.spines['top'].set_visible(False)
        subplot.spines['right'].set_visible(False)
        subplot.spines['left'].set_color('black')
        subplot.spines['bottom'].set_color('black')

        # กำหนดแบบอักษรและสีของเส้น
        subplot.tick_params(axis='both', which='major', labelsize=8, colors='black')

         # กำหนดระยะห่างระหว่างแท่ง
        subplot.set_xticks(range(len(x_labels)))

        # กำหนดแท่งใหม่เป็นชื่อของแต่ละ profile
        subplot.set_xticklabels(x_labels)

        # สร้างเฟรมสำหรับกราฟ
        frame = tk.Frame(self, highlightbackground='black', highlightthickness=1, borderwidth=1, relief="ridge")
        frame.grid(row=0, column=0, sticky="NSWE")

        # สร้างวิดเจ็ต FigureCanvasTkAgg
        canvas = FigureCanvasTkAgg(figure, master=frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    def setBreakevenGraph(self, profile1, profile2):
        # สร้างภาพ Matplotlib
        figure = Figure(figsize=(6.5, 3.25), dpi=70)
        subplot = figure.add_subplot(111)

        # สร้างข้อมูลเพื่อเปรียบเทียบ
        x_labels = [profile1, profile2]
        
        # ตรวจสอบว่าข้อมูลไม่ใช่ค่าว่าง
        if self.add_revenue.cget("text").strip() == "":
            revenue1 = 0.0
        else:
            revenue1 = float(self.add_revenue.cget("text"))

        if self.add_revenue2.cget("text").strip() == "":
            revenue2 = 0.0
        else:
            revenue2 = float(self.add_revenue2.cget("text"))

        # นำค่าจาก add_revenue และ add_revenue2 มาใช้เป็น y_values
        y_values = [revenue1, revenue2]

        # สร้างกราฟแท่งเปรียบเทียบ
        subplot.bar(range(len(x_labels)), y_values, color=['blue', 'green'], width=0.1, align='center')

        # เพิ่มเส้นกริด
        subplot.grid(True, linestyle='--', linewidth=0.2)

        # เพิ่มหัวเรื่อง
        subplot.set_title('Comparison of Revenue', fontsize=8, fontweight='bold', color='black')

        # กำหนด label แกน x และ y
        subplot.set_ylabel('Bath', fontsize=8, color='black')

        # ปรับแต่งเส้นขอบ
        subplot.spines['top'].set_visible(False)
        subplot.spines['right'].set_visible(False)
        subplot.spines['left'].set_color('black')
        subplot.spines['bottom'].set_color('black')

        # กำหนดแบบอักษรและสีของเส้น
        subplot.tick_params(axis='both', which='major', labelsize=8, colors='black')

        # กำหนดระยะห่างระหว่างแท่ง
        subplot.set_xticks(range(len(x_labels)))

        # กำหนดแท่งใหม่เป็นชื่อของแต่ละ profile
        subplot.set_xticklabels(x_labels)

        # สร้างเฟรมสำหรับกราฟ
        frame = tk.Frame(self, highlightbackground='black', highlightthickness=1, borderwidth=1, relief="ridge")
        frame.grid(row=0, column=1, sticky="NSWE")

        # สร้างวิดเจ็ต FigureCanvasTkAgg
        canvas = FigureCanvasTkAgg(figure, master=frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    def show_profile(self, profile1, profile2, rawmats_1, transpots_1,
                      performances_1, rawmats_2, transpots_2, performances_2, breakpoint_data1, breakpoint_data2):

        # Check if any of the data is None
        if rawmats_1 is None or transpots_1 is None or performances_1 is None or rawmats_2 is None or transpots_2 is None or performances_2 is None:
            messagebox.showerror("Error", "Data is missing")
            return

        # แสดงข้อมูลโปรไฟล์ที่เลือกใน Label
        self.label_profile1.config(text=profile1)
        self.label_profile2.config(text=profile2)
        self.break_profile1.config(text=profile1)
        self.break_profile2.config(text=profile2)

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
        self.setBreakevenGraph(profile1, profile2)
        self.set_breakpoint_data(breakpoint_data1, breakpoint_data2)
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

        # Format the percentage difference with a leading "+" if positive
        percentage_text = f"{percentage_difference:+.2f}%" if percentage_difference >= 0 else f"{percentage_difference:.2f}%"

        # Update the label with the percentage difference
        self.label_cf.config(text=percentage_text)

    def export(self):
        wb = openpyxl.Workbook()  # สร้างอ็อบเจ็กต์สมุดงานใหม่
        sheet = wb.active  # รับแผ่นงานที่กำลังใช้งาน

        profile1 = []
        profile2 = [] 
        
    
        for category, _, name, amount, unit in self.items:
            if category == 'Material':
                profile1.append((name, amount, unit))              
            elif category == 'Transpotation':
                profile2.append((name, amount, unit))

        # วาดกราฟ
        figure = Figure(figsize=(5, 3), dpi=70)
        subplot = figure.add_subplot(111)

        x = [item[0] for item in profile1]
        y = [float(item[1]) for item in profile2]

        subplot.tick_params(axis='x', labelrotation=90, labelfontfamily="tahoma")
        subplot.plot(x, y)

        buffer = BytesIO()
        figure.savefig(buffer, format="png")
        img = openpyxl.drawing.image.Image(buffer)
        sheet.add_image(img, f"A{len(profile1) + 5}")

        align = openpyxl.styles.Alignment(horizontal="center")

        sheet.merge_cells("A1:C1")
        sheet["A1"].value = "โปรไฟล์ที่หนึ่ง"
        sheet["A1"].alignment = align
        sheet.merge_cells("D1:F1")
        sheet["D1"].value = "โปรไฟล์ที่สอง"
        sheet["D1"].alignment = align
        sheet.merge_cells("G1:I1")

        data = profile1 + profile2

        for row_index, row in enumerate(data):
            for col_index, value in enumerate(row):
                sheet.cell(row=row_index + 2, column=col_index + 1, value=value)

        file_path = filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[("ไฟล์ Excel", "*.xlsx")])

        if file_path:
            wb.save(file_path) 
            print(f"บันทึกไฟล์ที่: {file_path}")
        else:
            print("การบันทึกไฟล์ถูกยกเลิก")
        

    
    
