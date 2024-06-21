import tkinter as tk
from tkinter import ttk, filedialog
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import locale
# import matplotlib.widgets as ZoomPan
import openpyxl.drawing
import openpyxl.drawing.image
from openpyxl.drawing.image import Image
from openpyxl.utils import get_column_letter
import openpyxl.styles
from openpyxl.styles import Alignment, Border, Side, Font, PatternFill, PatternFill
# import pandas as pd
import openpyxl
from io import BytesIO
from controllers.tooltip_controller import ToolTipController

# ตั้งค่าภาษาและภูมิภาค
locale.setlocale(locale.LC_ALL, 'th_TH.UTF-8')

class ConnewView(ttk.Frame):

    def __init__(self, controller, app):
        super().__init__(app)
        self.controller = controller
        self.items = []

        self.style = ttk.Style()
        self.style.configure("My.TFrame", background='#ADD8E6')

        # Window
        self.main_frame =  ttk.Frame(self)

        self.label_profile = ttk.Label(self, borderwidth=1, relief="ridge", text = "", font=('bold'))
        self.label_profile.grid(row=0, column=0, columnspan=2, sticky='NSWE')
        self.label_profile.configure(anchor='center', background='#ADD8E6')

        # สร้าง Frame เพิ่มเติมเพื่อควบคุมการวางและกรอบสามเหลี่ยม
        frame_labels = ttk.Frame(self, borderwidth=1, relief="ridge", style="My.TFrame")
        frame_labels.grid(row=3, column=1, sticky='NSWE')

        # Label แรก
        self.label_totalcf = ttk.Label(frame_labels, justify='center', text="ค่าคาร์บอนรวม", font=('bold'))
        self.label_totalcf.grid(row=0, column=0, padx=10, pady=20, sticky='E')
        self.label_totalcf.configure(anchor='e', background='#ADD8E6')

        # Label ที่สอง
        self.label_cf = ttk.Label(frame_labels, justify='center', text="", width=15, font=('bold'))
        self.label_cf.grid(row=0, column=1, padx=15, pady=20)
        self.label_cf.configure(anchor='center', background='#FFFFCC')

        # Label ที่สาม
        self.label_unit = ttk.Label(frame_labels, justify='center', text="KgCO2eq", font=('bold'))
        self.label_unit.grid(row=0, column=2, padx=5, pady=20)
        self.label_unit.configure(anchor='w', background='#ADD8E6')
        
        self.return_button = ttk.Button(self, text="Return to Profile", command=self.back)
        self.return_button.grid(row=4, column=1, padx=10, pady=10, ipadx=10, ipady=10, sticky = 'W')

        self.export_button = ttk.Button(self, text="Export to Excel", command=self.export)
        self.export_button.grid(row=4, column=1, padx=10, pady=10, ipadx=10, ipady=10, sticky = 'E')

        # Frame Input Treeview
        frame_input = ttk.Frame(self, borderwidth=1, relief="ridge", style="My.TFrame")
        frame_input.grid(row=2, column=0, sticky='NSWE')

        # TREE VIEW
        self.input_treeview = ttk.Treeview(frame_input, columns=("Name", "Carbon"), show="headings") # , "Unit"
        self.input_treeview.heading("Name", text="ชื่อ")
        self.input_treeview.column("Name", width=370, stretch=True)
        text_width = len("ค่าคาร์บอนเทียบเท่า (Y)")  # คำนวณความยาวของข้อความ
        self.input_treeview.heading("Carbon", text="ค่าคาร์บอน (Y)")
        self.input_treeview.column("Carbon", width=text_width * 5)
        # self.input_treeview.heading("Unit", text="หน่วย")
        # self.input_treeview.column("Unit", width=60, stretch=True)
        self.input_treeview.grid(row=0, column=0, sticky='WE')

        # สร้าง Scrollbar แนวแกน Y
        scroll_y = ttk.Scrollbar(frame_input, orient='vertical', command=self.input_treeview.yview)
        self.input_treeview.configure(yscrollcommand=scroll_y.set)
        scroll_y.grid(row=0, column=1, sticky='NS')

        self.grid_rowconfigure(0, weight=1)

         # Frame Process Treeview
        frame_process = ttk.Frame(self, borderwidth=1, relief="ridge", style="My.TFrame")
        frame_process.grid(row=2, column=1, sticky='NSWE')

        self.process_treeview = ttk.Treeview(frame_process, columns=("Name", "Carbon"), show="headings")
        self.process_treeview.heading("Name", text="ชื่อ (X)")
        self.process_treeview.column("Name", width=370, stretch=True)
        text_width = len("ค่าคาร์บอนเทียบเท่า (Y)")  # คำนวณความยาวของข้อความ
        self.process_treeview.heading("Carbon", text="ค่าคาร์บอน (Y)")
        self.process_treeview.column("Carbon", width=text_width * 5)
        # self.process_treeview.heading("Unit", text="หน่วย")
        # self.process_treeview.column("Unit", width=60, stretch=True)
        self.process_treeview.grid(row=0, column=0, sticky='WE')

        # สร้าง Scrollbar แนวแกน Y
        scroll_y = ttk.Scrollbar(frame_process, orient='vertical', command=self.process_treeview.yview)
        self.process_treeview.configure(yscrollcommand=scroll_y.set)
        scroll_y.grid(row=0, column=1, sticky='NS')

        self.grid_rowconfigure(0, weight=1)

        # Frame Breakeven_point
        frame_break = ttk.Frame(self, borderwidth=1, relief="ridge", style='My.TFrame')
        frame_break.grid(row=3, rowspan=2, column=0, sticky='NSWE')
        
        self.totalcost = ttk.Label(frame_break, text = "ต้นทุนรวม")
        self.totalcost.grid(row=0, column=0, padx=30, pady=5, sticky='W')
        self.totalcost.configure(anchor='w', background='#ADD8E6')

        self.revenue = ttk.Label(frame_break, text = "รายได้")
        self.revenue.grid(row=1, column=0, padx=30, pady=5, sticky='W')
        self.revenue.configure(anchor='w', background='#ADD8E6')
        
        self.profit = ttk.Label(frame_break, text = "กำไร")
        self.profit.grid(row=2, column=0, padx=30, pady=5, sticky='W')
        self.profit.configure(anchor='w', background='#ADD8E6')
        
        self.breakeven = ttk.Label(frame_break, text = "ปริมาณผลิตที่จุดคุ้มทุน")
        self.breakeven.grid(row=3, column=0, padx=30, pady=5, sticky='W')
        self.breakeven.configure(anchor='w', background='#ADD8E6')

        self.efficiency = ttk.Label(frame_break, text = "ประสิทธิภาพการผลิต")
        self.efficiency.grid(row=4, column=0, padx=30, pady=5, sticky='W')
        self.efficiency.configure(anchor='w', background='#ADD8E6')

        self.add_totalcost = ttk.Label(frame_break, text = "")
        self.add_totalcost.grid(row=0, column=1, padx=40, pady=5, sticky='E')
        self.add_totalcost.configure(anchor='w', background='#FFFFCC')

        self.add_revenue = ttk.Label(frame_break, text = "")
        self.add_revenue.grid(row=1, column=1, padx=40, pady=5, sticky='E')
        self.add_revenue.configure(anchor='w', background='#FFFFCC')

        self.add_profit = ttk.Label(frame_break, text = "")
        self.add_profit.grid(row=2, column=1, padx=40, pady=5, sticky='E')
        self.add_profit.configure(anchor='w', background='#FFFFCC')

        self.add_breakeven = ttk.Label(frame_break, text = "")
        self.add_breakeven.grid(row=3, column=1, padx=40, pady=5, sticky='E')
        self.add_breakeven.configure(anchor='w', background='#FFFFCC')

        self.add_efficiency = ttk.Label(frame_break, text = "")
        self.add_efficiency.grid(row=4, column=1, padx=40, pady=5, sticky='E')
        self.add_efficiency.configure(anchor='w', background='#FFFFCC')

        self.unit_totalcost = ttk.Label(frame_break, text = "บาท")
        self.unit_totalcost.grid(row=0, column=2, padx=40, pady=5)
        self.unit_totalcost.configure(anchor='e', background='#ADD8E6')

        self.unit_revenue = ttk.Label(frame_break, text = "บาท")
        self.unit_revenue.grid(row=1, column=2, padx=40, pady=5)
        self.unit_revenue.configure(anchor='e', background='#ADD8E6')

        self.unit_profit = ttk.Label(frame_break, text = "บาท")
        self.unit_profit.grid(row=2, column=2, padx=40, pady=5)
        self.unit_profit.configure(anchor='e', background='#ADD8E6')

        self.unit_breakeven = ttk.Label(frame_break, text = "หน่วย")
        self.unit_breakeven.grid(row=3, column=2, padx=40, pady=5)
        self.unit_breakeven.configure(anchor='e', background='#ADD8E6')

        self.unit_efficiency = ttk.Label(frame_break, text = "%")
        self.unit_efficiency.grid(row=4, column=2, padx=40, pady=5)
        self.unit_efficiency.configure(anchor='e', background='#ADD8E6')
        
        # self.output_treeview = ttk.Treeview(self, columns=("Name", "Carbon", "Unit"), show="headings")
        # self.output_treeview.heading("Name", text="ชื่อ")
        # self.output_treeview.column("Name", width=310)
        # self.output_treeview.heading("Carbon", text="ค่าคาร์บอนเทียบเท่า")
        # self.output_treeview.column("Carbon", width=95)
        # self.output_treeview.heading("Unit", text="หน่วย")
        # self.output_treeview.column("Unit", width=60)
        # self.output_treeview.grid(row=3, rowspan=2, column=2, padx=5, pady=5)

        self.add_button_tooltips()
    
    def add_button_tooltips(self):
        ToolTipController(self.export_button, "ส่งออกไปยัง Excel")
        ToolTipController(self.return_button, "กลับไปยังหน้าหลัก")

    def setInputGraph(self, items):
        # สร้างรูปภาพ Matplotlib
        figure = Figure(figsize=(6.9, 3), dpi=70)
        subplot = figure.add_subplot(111)

        # ข้อมูลเส้นกราฟ
        x = []
        y = []
        for item in items:
            x.append(item[0])
            y.append(float(item[1]))

        # ตั้งค่าฟอนต์
        subplot.tick_params(axis='x', labelrotation=0, labelsize=10, colors='white')

        # สร้างกราฟด้วยสีส้ม
        subplot.plot(x, y, color='blue')

        # เพิ่มจุดบ่งบอกตำแหน่งด้วยสีส้ม
        subplot.scatter(x, y, color='blue')

        # เพิ่มตัวเลขกำกับ
        for i, txt in enumerate(y):
            subplot.annotate(f'{txt}', (x[i], y[i]), textcoords="offset points", xytext=(0,10), ha='center', fontsize=8)

        # เพิ่มกริด
        subplot.grid(True, linestyle='--', linewidth=0.5)

        # เพิ่มชื่อกราฟ
        subplot.set_title('Input', fontsize=12, fontweight='bold')

        # เพิ่มป้ายกำกับแกน
        subplot.set_ylabel('KgCO2eq', fontsize=10)

        # ปรับแต่งป้ายกำกับ
        subplot.tick_params(axis='both', which='major', labelsize=8)

        # ปรับแต่งขอบ
        subplot.spines['top'].set_visible(False)
        subplot.spines['right'].set_visible(False)

        # สร้างกรอบสำหรับแคนวาสพร้อมเส้นขอบ
        frame = tk.Frame(self, highlightbackground='black', highlightthickness=1, borderwidth=1, relief="ridge")
        frame.grid(row=1, column=0, sticky='NSWE')

        # สร้างวิดเจ็ต FigureCanvasTkAgg
        canvas = FigureCanvasTkAgg(figure, master=frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    def setProcessGraph(self, items):
        # สร้างรูปภาพ Matplotlib
        figure = Figure(figsize=(6.9, 3), dpi=70)
        subplot = figure.add_subplot(111)

        # ข้อมูลเส้นกราฟ
        x = []
        y = []
        for item in items:
            x.append(item[0])
            y.append(float(item[1]))

        # ตั้งค่าฟอนต์
        subplot.tick_params(axis='x', labelrotation=0, labelsize=10, colors='white')

        # สร้างกราฟด้วยสีส้ม
        subplot.plot(x, y, color='orange')

        # เพิ่มจุดบ่งบอกตำแหน่งด้วยสีส้ม
        subplot.scatter(x, y, color='orange')

        # เพิ่มตัวเลขกำกับ
        for i, txt in enumerate(y):
            subplot.annotate(f'{txt}', (x[i], y[i]), textcoords="offset points", xytext=(0,10), ha='center', fontsize=8)

        # เพิ่มกริด
        subplot.grid(True, linestyle='--', linewidth=0.5)

        # เพิ่มชื่อกราฟ
        subplot.set_title('Process', fontsize=12, fontweight='bold')

        # เพิ่มป้ายกำกับแกน
        subplot.set_ylabel('KgCO2eq', fontsize=10)

        # ปรับแต่งป้ายกำกับ
        subplot.tick_params(axis='both', which='major', labelsize=8)

        # ปรับแต่งขอบ
        subplot.spines['top'].set_visible(False)
        subplot.spines['right'].set_visible(False)

        # สร้างกรอบสำหรับแคนวาสพร้อมเส้นขอบ
        frame = tk.Frame(self, highlightbackground='black', highlightthickness=1, borderwidth=1, relief="ridge")
        frame.grid(row=1, column=1, sticky='NSWE')

        # สร้างวิดเจ็ต FigureCanvasTkAgg
        canvas = FigureCanvasTkAgg(figure, master=frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    # def setOutputGraph(self, items):
    #     # Create a Matplotlib figure
    #     figure = Figure(figsize=(6.5, 3), dpi=70)
    #     subplot = figure.add_subplot(111)
    
    #     # Query from database
    #     # Line data
    #     x = []
    #     y = []
    #     for item in items:
    #         x.append(item[0])
    #         y.append(float(item[1]))

    #     # Set font
    #     subplot.tick_params(axis='x', labelrotation=90, labelfontfamily="Tahoma")
    
    #     # Create graph
    #     subplot.plot(x, y)
    
    #     # Add grid
    #     subplot.grid(True, linestyle='--', linewidth=0.5)

    #     # Add title
    #     subplot.set_title('Output', fontsize=14, fontweight='bold')

    #     # Customize tick labels
    #     subplot.tick_params(axis='both', which='major', labelsize=8)
    
    #     # Add labels to axes
    #     subplot.set_xlabel('X Axis Label', fontsize=10)
    #     subplot.set_ylabel('Y Axis Label', fontsize=10)

    #     # # Add legend
    #     # subplot.legend(['Legend'], loc='upper right', fontsize=8)

    #     # Customize borders
    #     subplot.spines['top'].set_visible(False)
    #     subplot.spines['right'].set_visible(False)

    #     # Create a FigureCanvasTkAgg widget
    #     canvas = FigureCanvasTkAgg(figure, master=self)
    #     canvas.draw()
    #     canvas.get_tk_widget().grid(row=1, rowspan=2, column=2, padx=5, pady=5)

    def back(self):
        self.controller.back_main()
    
    def format_currency(self, value):
        return locale.currency(value, grouping=True)

    def set_breakpoint_data(self, breakpoint_data):
        if breakpoint_data:
            fixed_cost, variable_cost, number_of_units, unit_price, product_efficiency = breakpoint_data[0]
            total_cost = fixed_cost + (variable_cost * number_of_units)
            revenue = unit_price * number_of_units
            profit = revenue - total_cost
            breakeven = fixed_cost / (unit_price - variable_cost)
            
            # อัปเดตค่า total cost
            self.add_totalcost.config(text=self.format_currency(total_cost))
            # อัปเดตค่า revenue
            self.add_revenue.config(text=self.format_currency(revenue))
            # อัปเดตค่า profit
            self.add_profit.config(text=self.format_currency(profit),foreground="red" if profit < 0 else "black")
            # อัปเดตค่า breakeven
            self.add_breakeven.config(text=f"{breakeven:.2f}",foreground="red" if breakeven < 0 else "black")
            # อัปเดตค่า efficiency
            self.add_efficiency.config(text=f"{product_efficiency:.2f}")
            
        else:
            self.add_totalcost.config(text="-", foreground="black")
            self.add_revenue.config(text="-", foreground="black")
            self.add_profit.config(text="-", foreground="black")
            self.add_breakeven.config(text="-", foreground="black")
            self.add_efficiency.config(text="-", foreground="black")

    # def set_breakpoint_data(self, breakpoint_data):
    #     if breakpoint_data:
    #         fixed_cost, variable_cost, number_of_units, unit_price, product_efficiency = breakpoint_data[0]
    #         total_cost = fixed_cost + (variable_cost * number_of_units)
    #         revenue = unit_price * number_of_units
    #         profit = revenue - total_cost
    #         breakeven = fixed_cost / (unit_price - variable_cost)
        
    #         self.add_totalcost.config(text=f"{total_cost:.2f}")
    #         self.add_revenue.config(text=f"{revenue:.2f}")
    #         self.add_profit.config(text=f"{profit:.2f}")
    #         self.add_breakeven.config(text=f"{breakeven:.2f}")
    #         self.add_efficiency.config(text=f"{product_efficiency:.2f}")
        
    #     else:
    #         self.add_totalcost.config(text="-")
    #         self.add_revenue.config(text="-")
    #         self.add_profit.config(text="-")
    #         self.add_breakeven.config(text="-")
    #         self.add_efficiency.config(text="-")

    def setConclusion(self, profile_name, items, breakpoint_data) :
        self.input_treeview.delete(*self.input_treeview.get_children())
        self.process_treeview.delete(*self.process_treeview.get_children())
        # self.output_treeview.delete(*self.output_treeview.get_children())
        inputGraph = []
        outputGraph = []
        processGraph = []

        total_cf = 0  # ผลรวมของค่า Carbon

        for item in items:
            category, _, name, factor, amount, _ = item
            
            # self.input_treeview
            if category == 'Material':
                processGraph.append((name, round(float(factor) * float(amount), 3)))
                self.process_treeview.insert("", "end", values=(name, round(float(factor) * float(amount), 3))) # , "KgCO2eq"
                total_cf += float(factor) * float(amount)  # เพิ่มค่า Carbon ลงในผลรวม

            elif category == 'Transpotation':
                inputGraph.append((name, round(float(factor) * float(amount), 3)))
                outputGraph.append((name, round(float(factor) * float(amount), 3)))
                self.input_treeview.insert("", "end", values=(name, round(float(factor) * float(amount), 3)))
                # self.output_treeview.insert("", "end", values=(name, round(float(factor) * float(amount), 3), "KgCO2eq"))
                total_cf += float(factor) * float(amount)  # เพิ่มค่า Carbon ลงในผลรวม

            elif category == 'Performance':
                processGraph.append((name, round(float(factor) * float(amount), 3)))
                self.process_treeview.insert("", "end", values=(name, round(float(factor) * float(amount), 3)))
                total_cf += float(factor) * float(amount)  # เพิ่มค่า Carbon ลงในผลรวม

        self.label_cf.config(text="{:.3f}".format(total_cf))  # กำหนดผลรวมของค่า Carbon ลงใน label_cf

        self.setInputGraph(inputGraph)
        # self.setOutputGraph(outputGraph)
        self.setProcessGraph(processGraph)
        self.set_breakpoint_data(breakpoint_data)
        self.items = items
        self.label_profile.config(text=profile_name)

    def export(self):
        wb = openpyxl.Workbook()
        sheet = wb.active
        sheet.title = "Carbon Footprint Report"

        input_data = []
        process_data = []

        for item in self.items:
            category, _, name, carbon_per, amount, unit = item
            carbon_footprint = round(float(carbon_per) * float(amount), 2)  # Round to 2 decimal places

            if category == 'Material':
                process_data.append((name, carbon_per, amount, unit, carbon_footprint))
            elif category == 'Transpotation':
                input_data.append((name, carbon_per, amount, unit, carbon_footprint))
            elif category == 'Performance':
                process_data.append((name, carbon_per, amount, unit, carbon_footprint))

        total_input_carbon_footprint = round(sum(item[4] for item in input_data), 2)
        total_process_carbon_footprint = round(sum(item[4] for item in process_data), 2)
        total_carbon_footprint = round(total_input_carbon_footprint + total_process_carbon_footprint, 2)

        # Calculate percentage difference
        if total_input_carbon_footprint > 0:
            percentage_difference = round(((total_process_carbon_footprint - total_input_carbon_footprint) / total_input_carbon_footprint) * 100, 2)
        else:
            percentage_difference = 0

        # Styles
        align_center = Alignment(horizontal="center", vertical="center")
        border_style = Border(left=Side(border_style='medium', color='000000'),
                            right=Side(border_style='medium', color='000000'),
                            top=Side(border_style='medium', color='000000'),
                            bottom=Side(border_style='medium', color='000000'))
        header_font = Font(bold=True, color='FFFFFF')
        header_fill = PatternFill(start_color="4F81BD", end_color="4F81BD", fill_type="solid")

        # Header
        sheet.merge_cells("A1:E1")
        sheet["A1"].value = "Carbon Footprint Report"
        sheet["A1"].alignment = align_center
        sheet["A1"].font = Font(size=14, bold=True)

        # Table headers
        headers = ["Name", "Emission Factor", "Amount", "Unit", "Carbon Footprint"]
        for col_num, header in enumerate(headers, start=1):
            cell = sheet.cell(row=2, column=col_num)
            cell.value = header
            cell.border = border_style
            cell.alignment = align_center
            cell.font = header_font
            cell.fill = header_fill

        # Data rows
        row_num = 3
        for data in input_data:
            for col_num, value in enumerate(data, start=1):
                cell = sheet.cell(row=row_num, column=col_num)
                cell.value = value
                cell.border = border_style
                if col_num in [2, 3, 5]:  # Emission Factor, Amount, and Carbon Footprint columns
                    cell.number_format = '0.00'
            row_num += 1

        for data in process_data:
            for col_num, value in enumerate(data, start=1):
                cell = sheet.cell(row=row_num, column=col_num)
                cell.value = value
                cell.border = border_style
                if col_num in [2, 3, 5]:  # Emission Factor, Amount, and Carbon Footprint columns
                    cell.number_format = '0.00'
            row_num += 1

        # Summary
        summary_row = row_num
        sheet[f"A{summary_row}"] = "Total Emission Factor"
        sheet[f"A{summary_row}"].border = border_style
        sheet[f"B{summary_row}"] = total_carbon_footprint
        sheet[f"B{summary_row}"].border = border_style
        sheet[f"B{summary_row}"].number_format = '0.00'  # Apply number format
        sheet[f"C{summary_row}"] = "KgCO2eq"
        sheet[f"C{summary_row}"].border = border_style
        sheet[f"C{summary_row}"].alignment = align_center

        # Additional details
        sheet[f"A{summary_row + 2}"] = "Total Cost"
        total_cost_cell = sheet[f"B{summary_row + 2}"]
        total_cost_cell.value = float(self.add_totalcost.cget("text"))
        total_cost_cell.border = border_style
        total_cost_cell.number_format = '0.00'  # Apply number format

        # Add percentage difference summary 5 rows below Total Cost
        percentage_diff_row = summary_row + 7
        sheet[f"A{percentage_diff_row}"] = "Percentage difference between Process and Input"
        sheet[f"B{percentage_diff_row}"] = f"{percentage_difference:.2f}%"

        # Additional details continue
        sheet[f"B{summary_row + 3}"] = self.add_revenue.cget("text")
        sheet[f"B{summary_row + 3}"].border = border_style
        sheet[f"B{summary_row + 4}"] = self.add_profit.cget("text")
        sheet[f"B{summary_row + 4}"].border = border_style
        sheet[f"B{summary_row + 5}"] = self.add_breakeven.cget("text")
        sheet[f"B{summary_row + 5}"].border = border_style
        sheet[f"B{summary_row + 6}"] = self.add_efficiency.cget("text")
        sheet[f"B{summary_row + 6}"].border = border_style

        # Add new details at A16, A17, A18, and A19
        sheet[f"A16"] = "Revenue"
        sheet[f"B16"] = self.add_revenue.cget("text")
        sheet[f"B16"].border = border_style

        sheet[f"A17"] = "Profit"
        sheet[f"B17"] = self.add_profit.cget("text")
        sheet[f"B17"].border = border_style

        sheet[f"A18"] = "Break-even Point"
        sheet[f"B18"] = self.add_breakeven.cget("text")
        sheet[f"B18"].border = border_style

        sheet[f"A19"] = "Production Efficiency"
        sheet[f"B19"] = self.add_efficiency.cget("text")
        sheet[f"B19"].border = border_style

        # Auto fit column widths
        for column_cells in sheet.columns:
            max_length = 0
            column = get_column_letter(column_cells[0].column)  # Get the column name
            for cell in column_cells:
                try:
                    if cell.value:
                        max_length = max(max_length, len(str(cell.value)))
                except:
                    pass
            adjusted_width = (max_length - 30) if column == 'A' else (max_length + 0)
            sheet.column_dimensions[column].width = adjusted_width

        # Set wrap text for all cells in column A
        for row in sheet.iter_rows(min_col=1, max_col=1, min_row=1, max_row=sheet.max_row):
            for cell in row:
                cell.alignment = Alignment(wrap_text=True, vertical='center')

        # Combined chart for Input and Process
        def create_combined_chart(input_data, process_data, title):
            figure = Figure(figsize=None, dpi=80)
            subplot = figure.add_subplot(111)

            input_x = [item[0] for item in input_data]
            input_y = [item[4] for item in input_data]
            process_x = [item[0] for item in process_data]
            process_y = [item[4] for item in process_data]

            # Plot input data
            subplot.plot(input_x, input_y, marker='o', label='Input')
            for i, txt in enumerate(input_y):
                subplot.annotate(f"{txt:.2f}", (input_x[i], input_y[i]), textcoords="offset points", xytext=(0, 10), ha='center')

            # Plot process data
            subplot.plot(process_x, process_y, marker='x', label='Process')
            for i, txt in enumerate(process_y):
                subplot.annotate(f"{txt:.2f}", (process_x[i], process_y[i]), textcoords="offset points", xytext=(0, 10), ha='center')

            subplot.set_ylabel('KgCO2eq', fontsize=10)
            subplot.set_title(title, fontsize=12, fontweight='bold')
            subplot.legend()

            # Remove x-axis labels
            subplot.set_xticklabels([])

            buffer = BytesIO()
            figure.savefig(buffer, format="png")
            buffer.seek(0)
            img = Image(buffer)
            return img

        combined_chart = create_combined_chart(input_data, process_data, "Combined Carbon Footprint")
        sheet.add_image(combined_chart, f"A{percentage_diff_row + 5}")

        # Save the workbook
        file_path = filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[("Excel files", "*.xlsx")])
        if file_path:
            wb.save(file_path)
            print(f"File saved at: {file_path}")
        else:
            print("File save canceled")

    # def export(self):
    #     wb = openpyxl.Workbook()
    #     sheet = wb.active
    #     sheet.title = "Carbon Footprint Report"

    #     input_data = []
    #     process_data = []

    #     for item in self.items:
    #         category, _, name, carbon_per, amount, unit = item
    #         carbon_footprint = round(float(carbon_per) * float(amount), 2)  # ปัดเป็นทศนิยม 2 ตำแหน่ง

    #         if category == 'Material':
    #             process_data.append((name, carbon_per, amount, unit, carbon_footprint))
    #         elif category == 'Transportation':
    #             input_data.append((name, carbon_per, amount, unit, carbon_footprint))
    #         elif category == 'Performance':
    #             process_data.append((name, carbon_per, amount, unit, carbon_footprint))

    #     total_input_carbon_footprint = round(sum(item[4] for item in input_data), 2)
    #     total_process_carbon_footprint = round(sum(item[4] for item in process_data), 2)
    #     total_carbon_footprint = round(total_input_carbon_footprint + total_process_carbon_footprint, 2)

    #     # คำนวณความแตกต่างเป็นเปอร์เซ็นต์
    #     if total_input_carbon_footprint > 0:
    #         percentage_difference = round(((total_process_carbon_footprint - total_input_carbon_footprint) / total_input_carbon_footprint) * 100, 2)
    #     else:
    #         percentage_difference = 0

    #     # สไตล์
    #     align_center = Alignment(horizontal="center", vertical="center")
    #     border_style = Border(left=Side(border_style='medium', color='000000'),
    #                         right=Side(border_style='medium', color='000000'),
    #                         top=Side(border_style='medium', color='000000'),
    #                         bottom=Side(border_style='medium', color='000000'))
    #     header_font = Font(bold=True, color='FFFFFF')
    #     header_fill = PatternFill(start_color="4F81BD", end_color="4F81BD", fill_type="solid")
    #     angsana_font = Font(name='AngsanaUPC', size=14)

    #     # หัวเรื่อง
    #     sheet.merge_cells("A1:E1")
    #     sheet["A1"].value = "Carbon Footprint Report"
    #     # sheet["A1"].alignment = align_center
    #     # sheet["A1"].font = Font(size=16, bold=True)

    #     # หัวตาราง
    #     headers = ["Name", "Emission Factor", "Amount", "Unit", "Carbon Footprint"]
    #     for col_num, header in enumerate(headers, start=1):
    #         cell = sheet.cell(row=2, column=col_num)
    #         cell.value = header
    #         cell.border = border_style
    #         cell.alignment = align_center
    #         cell.font = header_font
    #         cell.fill = header_fill

    #     # แถวข้อมูล
    #     row_num = 3
    #     for data in input_data:
    #         for col_num, value in enumerate(data, start=1):
    #             cell = sheet.cell(row=row_num, column=col_num)
    #             cell.value = value
    #             cell.border = border_style
    #             cell.font = angsana_font
    #             if col_num in [2, 3, 5]:  # คอลัมน์ Emission Factor, Amount และ Carbon Footprint
    #                 cell.number_format = '0.00'
    #         row_num += 1

    #     for data in process_data:
    #         for col_num, value in enumerate(data, start=1):
    #             cell = sheet.cell(row=row_num, column=col_num)
    #             cell.value = value
    #             cell.border = border_style
    #             cell.font = angsana_font
    #             if col_num in [2, 3, 5]:  # คอลัมน์ Emission Factor, Amount และ Carbon Footprint
    #                 cell.number_format = '0.00'
    #         row_num += 1

    #     # สรุป
    #     summary_row = row_num
    #     sheet[f"A{summary_row}"] = "Total Emission Factor"
    #     sheet[f"A{summary_row}"].border = border_style
    #     sheet[f"A{summary_row}"].font = angsana_font
    #     sheet[f"B{summary_row}"] = total_carbon_footprint
    #     sheet[f"B{summary_row}"].border = border_style
    #     sheet[f"B{summary_row}"].font = angsana_font
    #     sheet[f"B{summary_row}"].number_format = '0.00'  # ใช้รูปแบบตัวเลข
    #     sheet[f"C{summary_row}"] = "KgCO2eq"
    #     sheet[f"C{summary_row}"].border = border_style
    #     sheet[f"C{summary_row}"].alignment = align_center
    #     sheet[f"C{summary_row}"].font = angsana_font

    #     # รายละเอียดเพิ่มเติม
    #     sheet[f"A{summary_row + 2}"] = "Total Cost"
    #     sheet[f"A{summary_row + 2}"].font = angsana_font
    #     sheet[f"B{summary_row + 2}"].border = border_style
    #     sheet[f"C{summary_row + 2}"] = "Bath"
    #     sheet[f"C{summary_row + 2}"].border = border_style
    #     sheet[f"C{summary_row + 2}"].font = angsana_font
    #     total_cost_cell = sheet[f"B{summary_row + 2}"]
    #     total_cost_cell.value = float(self.add_totalcost.cget("text"))
    #     total_cost_cell.border = border_style
    #     total_cost_cell.font = angsana_font
    #     total_cost_cell.number_format = '0.00'  # ใช้รูปแบบตัวเลข

    #     # เพิ่มสรุปความแตกต่างเป็นเปอร์เซ็นต์ 5 แถวถัดจาก Total Cost
    #     percentage_diff_row = summary_row + 7
    #     sheet[f"A{percentage_diff_row}"] = "Percentage difference between Process and Input"
    #     sheet[f"A{percentage_diff_row}"].font = angsana_font
    #     sheet[f"B{percentage_diff_row}"] = f"{percentage_difference:.2f}"
    #     sheet[f"B{percentage_diff_row}"].border = border_style
    #     sheet[f"B{percentage_diff_row}"].font = angsana_font

    #     # รายละเอียดเพิ่มเติม
    #     sheet[f"A{summary_row + 3}"] = "Revene"
    #     # sheet[f"A{summary_row + 3}"].border = border_style
    #     sheet[f"A{summary_row + 3}"].font = angsana_font
    #     sheet[f"B{summary_row + 3}"] = self.add_revenue.cget("text")
    #     sheet[f"B{summary_row + 3}"].border = border_style
    #     sheet[f"B{summary_row + 3}"].font = angsana_font
    #     sheet[f"C{summary_row + 3}"] = "Bath"
    #     sheet[f"C{summary_row + 3}"].border = border_style
    #     sheet[f"C{summary_row + 3}"].font = angsana_font

    #     sheet[f"A{summary_row + 4}"] = "Profit"
    #     # sheet[f"A{summary_row + 4}"].border = border_style
    #     sheet[f"A{summary_row + 4}"].font = angsana_font
    #     sheet[f"B{summary_row + 4}"] = self.add_profit.cget("text")
    #     sheet[f"B{summary_row + 4}"].border = border_style
    #     sheet[f"B{summary_row + 4}"].font = angsana_font
    #     sheet[f"C{summary_row + 4}"] = "Bath"
    #     sheet[f"C{summary_row + 4}"].border = border_style
    #     sheet[f"C{summary_row + 4}"].font = angsana_font
        
    #     sheet[f"A{summary_row + 5}"] = "Break-even Point"
    #     # sheet[f"A{summary_row + 5}"].border = border_style
    #     sheet[f"A{summary_row + 5}"].font = angsana_font
    #     sheet[f"B{summary_row + 5}"] = self.add_breakeven.cget("text")
    #     sheet[f"B{summary_row + 5}"].border = border_style
    #     sheet[f"B{summary_row + 5}"].font = angsana_font
    #     sheet[f"C{summary_row + 5}"] = "Unit"
    #     sheet[f"C{summary_row + 5}"].border = border_style
    #     sheet[f"C{summary_row + 5}"].font = angsana_font
        
    #     sheet[f"A{summary_row + 6}"] = "Production Efficiency"
    #     # sheet[f"A{summary_row + 6}"].border = border_style
    #     sheet[f"A{summary_row + 6}"].font = angsana_font
    #     sheet[f"B{summary_row + 6}"] = self.add_efficiency.cget("text")
    #     sheet[f"B{summary_row + 6}"].border = border_style
    #     sheet[f"B{summary_row + 6}"].font = angsana_font
    #     sheet[f"C{summary_row + 6}"] = "%"
    #     sheet[f"C{summary_row + 6}"].border = border_style
    #     sheet[f"C{summary_row + 6}"].font = angsana_font

    #     # ปรับความกว้างของคอลัมน์ตามรายการที่ยาวที่สุดในแต่ละคอลัมน์
    #     for column_cells in sheet.columns:
    #         max_length = 0
    #         column = get_column_letter(column_cells[0].column)  # รับชื่อคอลัมน์
    #         for cell in column_cells:
    #             try:
    #                 if cell.value:
    #                     max_length = max(max_length, len(str(cell.value)))
    #             except:
    #                 pass
    #         adjusted_width = (max_length - 30) if column == 'A' else (max_length + 0)
    #         sheet.column_dimensions[column].width = adjusted_width

    #     # ตั้งค่าการห่อข้อความสำหรับเซลล์ทั้งหมดในคอลัมน์ A
    #     for row in sheet.iter_rows(min_col=1, max_col=1, min_row=1, max_row=sheet.max_row):
    #         for cell in row:
    #             cell.alignment = Alignment(wrap_text=True, vertical='center')
    #             # cell.font = angsana_font
    #             sheet["A1"].alignment = align_center
    #             sheet["A1"].font = Font(name='AngsanaUPC', size=16, bold=True)
    #             sheet["A2"].alignment = align_center
    #             sheet["A2"].font = Font(name='AngsanaUPC', size=14, bold=True, color='FFFFFF')
    #             sheet["B2"].font = Font(name='AngsanaUPC', size=14, bold=True, color='FFFFFF')
    #             sheet["C2"].font = Font(name='AngsanaUPC', size=14, bold=True, color='FFFFFF')
    #             sheet["D2"].font = Font(name='AngsanaUPC', size=14, bold=True, color='FFFFFF')
    #             sheet["E2"].font = Font(name='AngsanaUPC', size=14, bold=True, color='FFFFFF')


    #     # กราฟรวมสำหรับ Input และ Process
    #     def create_combined_chart(input_data, process_data, title):
    #         figure = Figure(figsize=None, dpi=80)
    #         subplot = figure.add_subplot(111)

    #         input_x = [item[0] for item in input_data]
    #         input_y = [item[4] for item in input_data]
    #         process_x = [item[0] for item in process_data]
    #         process_y = [item[4] for item in process_data]

    #         # วาดกราฟข้อมูล input
    #         subplot.plot(input_x, input_y, marker='o', label='Input')
    #         for i, txt in enumerate(input_y):
    #             subplot.annotate(f"{txt:.2f}", (input_x[i], input_y[i]), textcoords="offset points", xytext=(0, 10), ha='center')

    #         # วาดกราฟข้อมูล process
    #         subplot.plot(process_x, process_y, marker='x', label='Process')
    #         for i, txt in enumerate(process_y):
    #             subplot.annotate(f"{txt:.2f}", (process_x[i], process_y[i]), textcoords="offset points", xytext=(0, 10), ha='center')

    #         subplot.set_ylabel('KgCO2eq', fontsize=10)
    #         subplot.set_title(title, fontsize=12, fontweight='bold')
    #         subplot.legend()

    #         # ลบป้ายชื่อแกน x
    #         subplot.set_xticklabels([])

    #         buffer = BytesIO()
    #         figure.savefig(buffer, format="png")
    #         buffer.seek(0)
    #         img = Image(buffer)
    #         return img

    #     combined_chart = create_combined_chart(input_data, process_data, "Combined Carbon Footprint")
    #     sheet.add_image(combined_chart, f"A{percentage_diff_row + 5}")

    #     # บันทึกไฟล์ workbook
    #     file_path = filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[("Excel files", "*.xlsx")])
    #     if file_path:
    #         wb.save(file_path)
    #         print(f"File saved at: {file_path}")
    #     else:
    #         print("File save canceled")