import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
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

        self.style = ttk.Style()
        self.style.configure("My.TFrame", background='#ADD8E6')

        self.frame_break_visible = True
        self.frame_break2_visible = True

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

        self.export_button = ttk.Button(self, text="Export to Excel", command=self.export)
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
        self.profile1_treeview.grid(row=1, column=0)

        self.profile2_treeview = ttk.Treeview(self, columns=("Name", "Carbon", "Unit"), show="headings")
        self.profile2_treeview.heading("Name", text="ชื่อ")
        self.profile2_treeview.column("Name", width=310, stretch=True)
        text_width = len("ค่าคาร์บอนเทียบเท่า (Y)")  # คำนวณความยาวของข้อความ
        self.profile2_treeview.heading("Carbon", text="คาร์บอนเทียบเท่า (Y)")
        self.profile2_treeview.column("Carbon", width=text_width * 5)
        self.profile2_treeview.heading("Unit", text="หน่วย")
        self.profile2_treeview.column("Unit", width=60, stretch=True)
        self.profile2_treeview.grid(row=1, column=1)

        # Frame Breakeven_point 1
        frame_break = ttk.Frame(self, borderwidth=1, relief="ridge")
        frame_break.grid(row=0, column=2, sticky='NSWE')

        self.break_profile1 = ttk.Label(frame_break, text = "", borderwidth=1, relief="ridge")
        self.break_profile1.grid(row=0, column=0, columnspan=3, sticky='NSWE')
        self.break_profile1.configure(anchor='center', background='#ADD8E6')
        
        self.label_totalcost = ttk.Label(frame_break, text = "ต้นทุนรวม")
        self.label_totalcost.grid(row=1, column=0, padx=10, pady=10, sticky='W')

        self.label_revenue = ttk.Label(frame_break, text = "รายได้")
        self.label_revenue.grid(row=2, column=0, padx=10, pady=10, sticky='W')
        
        self.profit = ttk.Label(frame_break, text = "กำไร")
        self.profit.grid(row=3, column=0, padx=10, pady=10, sticky='W')
        
        self.breakeven = ttk.Label(frame_break, text = "ปริมาณผลิตที่จุดคุ้มทุน")
        self.breakeven.grid(row=4, column=0, padx=10, pady=10, sticky='W')

        self.efficiency = ttk.Label(frame_break, text = "ประสิทธิภาพการผลิต")
        self.efficiency.grid(row=5, column=0, padx=10, pady=10, sticky='W')

        self.add_totalcost = ttk.Label(frame_break, text = "")
        self.add_totalcost.grid(row=1, column=1, padx=10, pady=10, sticky='W')

        self.add_revenue = ttk.Label(frame_break, text = "")
        self.add_revenue.grid(row=2, column=1, padx=10, pady=10, sticky='W')

        self.add_profit = ttk.Label(frame_break, text = "")
        self.add_profit.grid(row=3, column=1, padx=10, pady=10, sticky='W')

        self.add_breakeven = ttk.Label(frame_break, text = "")
        self.add_breakeven.grid(row=4, column=1, padx=10, pady=10, sticky='W')

        self.add_efficiency = ttk.Label(frame_break, text = "")
        self.add_efficiency.grid(row=5, column=1, padx=10, pady=10, sticky='W')

        self.unit_totalcost = ttk.Label(frame_break, text = "บาท")
        self.unit_totalcost.grid(row=1, column=2, padx=10, pady=10, sticky='W')

        self.unit_revenue = ttk.Label(frame_break, text = "บาท")
        self.unit_revenue.grid(row=2, column=2, padx=10, pady=10, sticky='W')

        self.unit_profit = ttk.Label(frame_break, text = "บาท")
        self.unit_profit.grid(row=3, column=2, padx=10, pady=10, sticky='W')

        self.unit_breakeven = ttk.Label(frame_break, text = "บาท")
        self.unit_breakeven.grid(row=4, column=2, padx=10, pady=10, sticky='W')

        self.unit_efficiency = ttk.Label(frame_break, text = "%")
        self.unit_efficiency.grid(row=5, column=2, padx=10, pady=10, sticky='W')

        # Frame Breakeven_point 2
        frame_break2 = ttk.Frame(self, borderwidth=1, relief="ridge")
        frame_break2.grid(row=1, column=2, sticky='NSWE')

        self.break_profile2 = ttk.Label(frame_break2, text = "", borderwidth=1, relief="ridge")
        self.break_profile2.grid(row=0, column=0, columnspan=3, sticky='NSWE')
        self.break_profile2.configure(anchor='center', background='#ADD8E6')
        
        self.label_totalcost = ttk.Label(frame_break2, text = "ต้นทุนรวม")
        self.label_totalcost.grid(row=1, column=0, padx=10, pady=10, sticky='W')

        self.label_revenue = ttk.Label(frame_break2, text = "รายได้")
        self.label_revenue.grid(row=2, column=0, padx=10, pady=10, sticky='W')
        
        self.profit = ttk.Label(frame_break2, text = "กำไร")
        self.profit.grid(row=3, column=0, padx=10, pady=10, sticky='W')
        
        self.breakeven = ttk.Label(frame_break2, text = "ปริมาณผลิตที่จุดคุ้มทุน")
        self.breakeven.grid(row=4, column=0, padx=10, pady=10, sticky='W')

        self.efficiency = ttk.Label(frame_break2, text = "ประสิทธิภาพการผลิต")
        self.efficiency.grid(row=5, column=0, padx=10, pady=10, sticky='W')

        self.add_totalcost2 = ttk.Label(frame_break2, text = "")
        self.add_totalcost2.grid(row=1, column=1, padx=10, pady=10, sticky='W')

        self.add_revenue2 = ttk.Label(frame_break2, text = "")
        self.add_revenue2.grid(row=2, column=1, padx=10, pady=10, sticky='W')

        self.add_profit2 = ttk.Label(frame_break2, text = "")
        self.add_profit2.grid(row=3, column=1, padx=10, pady=10, sticky='W')

        self.add_breakeven2 = ttk.Label(frame_break2, text = "")
        self.add_breakeven2.grid(row=4, column=1, padx=10, pady=10, sticky='W')

        self.add_efficiency2 = ttk.Label(frame_break2, text = "")
        self.add_efficiency2.grid(row=5, column=1, padx=10, pady=10, sticky='W')

        self.unit_totalcost2 = ttk.Label(frame_break2, text = "บาท")
        self.unit_totalcost2.grid(row=1, column=2, padx=10, pady=10, sticky='W')

        self.unit_revenue2 = ttk.Label(frame_break2, text = "บาท")
        self.unit_revenue2.grid(row=2, column=2, padx=10, pady=10, sticky='W')

        self.unit_profit2 = ttk.Label(frame_break2, text = "บาท")
        self.unit_profit2.grid(row=3, column=2, padx=10, pady=10, sticky='W')

        self.unit_breakeven2 = ttk.Label(frame_break2, text = "บาท")
        self.unit_breakeven2.grid(row=4, column=2, padx=10, pady=10, sticky='W')

        self.unit_efficiency2 = ttk.Label(frame_break2, text = "%")
        self.unit_efficiency2.grid(row=5, column=2, padx=10, pady=10, sticky='W')
        
    def back(self):
        self.controller.back_main()

    def set_breakpoint_data(self, breakpoint_data1, breakpoint_data2):
        if breakpoint_data1:
            fixed_cost, variable_cost, number_of_units, unit_price, product_efficiency = breakpoint_data1[0]
            total_cost = fixed_cost + (variable_cost * number_of_units)
            revenue = unit_price * number_of_units
            profit = revenue - total_cost
            breakeven = fixed_cost / (unit_price - variable_cost)
        
            self.add_totalcost.config(text=f"{total_cost:.3f}")
            self.add_revenue.config(text=f"{revenue:.3f}")
            self.add_profit.config(text=f"{profit:.3f}")
            self.add_breakeven.config(text=f"{breakeven:.3f}")
            self.add_efficiency.config(text=f"{int(product_efficiency)}")
        
        else:
            self.add_totalcost.config(text="-")
            self.add_revenue.config(text="-")
            self.add_profit.config(text="-")
            self.add_breakeven.config(text="-")
            self.add_efficiency.config(text="-")

        if breakpoint_data2:
            fixed_cost, variable_cost, number_of_units, unit_price, product_efficiency = breakpoint_data2[0]
            total_cost = fixed_cost + (variable_cost * number_of_units)
            revenue = unit_price * number_of_units
            profit = revenue - total_cost
            breakeven = fixed_cost / (unit_price - variable_cost)
        
            self.add_totalcost2.config(text=f"{total_cost:.3f}")
            self.add_revenue2.config(text=f"{revenue:.3f}")
            self.add_profit2.config(text=f"{profit:.3f}")
            self.add_breakeven2.config(text=f"{breakeven:.3f}")
            self.add_efficiency2.config(text=f"{int(product_efficiency)}")

        else:
            self.add_totalcost2.config(text="-")
            self.add_revenue2.config(text="-")
            self.add_profit2.config(text="-")
            self.add_breakeven2.config(text="-")
            self.add_efficiency2.config(text="-")

    def setCompareGraph(self, profile1, profile2):
        # สร้างภาพ Matplotlib
        figure = Figure(figsize=(6.5, 3), dpi=70)
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
        subplot.bar(x_labels, y_values, color=bar_colors, width=0.1)

        # เพิ่มเส้นกริด
        subplot.grid(True, linestyle='--', linewidth=0.5)

        # เพิ่มหัวเรื่อง
        subplot.set_title('Comparison of Profiles', fontsize=8, fontweight='bold', color='black')

        
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
        frame.grid(row=0, column=0, sticky="NSWE")

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

        # Update the label with the percentage difference
        self.label_cf.config(text=f"{percentage_difference:.2f}%")

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
        

    
    
