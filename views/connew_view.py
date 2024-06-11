import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import matplotlib.widgets as ZoomPan
import openpyxl.drawing
import openpyxl.drawing.image
import openpyxl.styles
from openpyxl.styles import Border, Side
import pandas as pd
import openpyxl
from io import BytesIO

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
        self.label_totalcf = ttk.Label(frame_labels, justify='center', text="ค่าคาร์บอนทั้งหมด", font=('bold'))
        self.label_totalcf.grid(row=0, column=0, padx=10, pady=20, sticky='E')
        self.label_totalcf.configure(anchor='e', background='#ADD8E6')

        # Label ที่สอง
        self.label_cf = ttk.Label(frame_labels, justify='center', text="", width=15, font=('bold'))
        self.label_cf.grid(row=0, column=1, padx=15, pady=20)
        self.label_cf.configure(anchor='center', background='#FFFFCC')

        # Label ที่สาม
        self.label_unit = ttk.Label(frame_labels, justify='center', text="KgCO2eq", font=('bold'))
        self.label_unit.grid(row=0, column=2, padx=10, pady=20)
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
        self.input_treeview.heading("Carbon", text="คาร์บอนเทียบเท่า (Y)")
        self.input_treeview.column("Carbon", width=text_width * 5)
        # self.input_treeview.heading("Unit", text="หน่วย")
        # self.input_treeview.column("Unit", width=60, stretch=True)
        self.input_treeview.grid(row=0, column=0)

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
        self.process_treeview.heading("Carbon", text="คาร์บอนเทียบเท่า (Y)")
        self.process_treeview.column("Carbon", width=text_width * 5)
        # self.process_treeview.heading("Unit", text="หน่วย")
        # self.process_treeview.column("Unit", width=60, stretch=True)
        self.process_treeview.grid(row=0, column=0)

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
    
    def setInputGraph(self, items):
        # Create a Matplotlib figure
        figure = Figure(figsize=(6.9, 3), dpi=70)
        subplot = figure.add_subplot(111)
    
        # Line data
        x = []
        y = []
        for item in items:
            x.append(item[0])
            y.append(float(item[1]))

        # Set font
        subplot.tick_params(axis='x', labelrotation=0, labelsize=10, colors='white')
    
        # Create graph
        subplot.plot(x, y)
    
        # Add grid
        subplot.grid(True, linestyle='--', linewidth=0.5)

        # Add title
        subplot.set_title('Input', fontsize=12, fontweight='bold')

        # Add labels to axes
        subplot.set_ylabel('KgCO2eq', fontsize=10)

        # Customize tick labels
        subplot.tick_params(axis='both', which='major', labelsize=8)
    
        # Customize borders
        subplot.spines['top'].set_visible(False)
        subplot.spines['right'].set_visible(False)

        # Create a Frame for the canvas with a border
        frame = tk.Frame(self, highlightbackground='black', highlightthickness=1, borderwidth=1, relief="ridge")
        frame.grid(row=1, column=0, sticky='NSWE')

        # Create a FigureCanvasTkAgg widget
        canvas = FigureCanvasTkAgg(figure, master=frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    def setProcessGraph(self, items):
        # Create a Matplotlib figure
        figure = Figure(figsize=(6.9, 3), dpi=70)
        subplot = figure.add_subplot(111)
    
        # Line data
        x = []
        y = []
        for item in items:
            x.append(item[0])
            y.append(float(item[1]))

        # Set font
        subplot.tick_params(axis='x', labelrotation=0, labelsize=10, colors='white')
    
        # Create graph
        subplot.plot(x, y)
    
        # Add grid
        subplot.grid(True, linestyle='--', linewidth=0.5)

        # Add title
        subplot.set_title('Process', fontsize=12, fontweight='bold')

        # Add labels to axes
        subplot.set_ylabel('KgCO2eq', fontsize=10)

        # Customize tick labels
        subplot.tick_params(axis='both', which='major', labelsize=8)
    
        # Customize borders
        subplot.spines['top'].set_visible(False)
        subplot.spines['right'].set_visible(False)

        # Create a Frame for the canvas with a border
        frame = tk.Frame(self, highlightbackground='black', highlightthickness=1, borderwidth=1, relief="ridge")
        frame.grid(row=1, column=1, sticky='NSWE')

        # Create a FigureCanvasTkAgg widget
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

    def set_breakpoint_data(self, breakpoint_data):
        if breakpoint_data:
            fixed_cost, variable_cost, number_of_units, unit_price, product_efficiency = breakpoint_data[0]
            total_cost = fixed_cost + (variable_cost * number_of_units)
            revenue = unit_price * number_of_units
            profit = revenue - total_cost
            breakeven = fixed_cost / (unit_price - variable_cost)
        
            self.add_totalcost.config(text=f"{total_cost:.2f}")
            self.add_revenue.config(text=f"{revenue:.2f}")
            self.add_profit.config(text=f"{profit:.2f}")
            self.add_breakeven.config(text=f"{breakeven:.2f}")
            self.add_efficiency.config(text=f"{product_efficiency:.2f}")
        
        else:
            self.add_totalcost.config(text="-")
            self.add_revenue.config(text="-")
            self.add_profit.config(text="-")
            self.add_breakeven.config(text="-")
            self.add_efficiency.config(text="-")

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
        wb = openpyxl.Workbook()  # สร้างอ็อบเจ็กต์ Workbook ใหม่
        sheet = wb.active  # ดึงแผ่นที่กำลังใช้งาน

        input = []
        process = [] 
        # output = []
        for item in self.items:
            category, _, name, carbon_per, amount, unit = item
        
            if category == 'Material':
                process.append((name, carbon_per, amount, unit))  # เพิ่มข้อมูลลงในรายการ process              
            elif category == 'Transpotation':
                input.append((name, carbon_per, amount, unit))  # เพิ่มข้อมูลลงในรายการ input
                # output.append((name, amount, unit))
            elif category == 'Performance':
                process.append((name, carbon_per, amount, unit))  # เพิ่มข้อมูลลงในรายการ process

        # วาดกราฟ
        figure_input = Figure(figsize=None, dpi=80)
        subplot_input = figure_input.add_subplot(111)

        x_input = []
        y_input = []
        for item in input:
            x_input.append(item[0])
            y_input.append(float(item[1]) * float(item[2]))

        subplot_input.tick_params(axis='x', labelrotation=90, labelfontfamily="tahoma", colors='white')
        subplot_input.set_ylabel('KgCO2eq', fontsize=10)  # เพิ่ม label ที่แกน y สำหรับกราฟข้อมูลนำเข้า
        subplot_input.plot(x_input, y_input)
        subplot_input.set_title('Input', fontsize=10, fontweight='bold')  # กำหนดชื่อกราฟของข้อมูลนำเข้า

        buffer_input = BytesIO()
        figure_input.savefig(buffer_input, format="png")
        img_input = openpyxl.drawing.image.Image(buffer_input)
        sheet.add_image(img_input, f"A{max(len(input), len(process)) + 20}")

        # วาดกราฟของ Process
        figure_process = Figure(figsize=None, dpi=80)
        subplot_process = figure_process.add_subplot(111)

        x_process = []
        y_process = []
        for item in process:
            x_process.append(item[0])
            y_process.append(float(item[1]) * float(item[2]))

        subplot_process.tick_params(axis='x', labelrotation=90, labelfontfamily="tahoma", colors='white')
        subplot_process.set_ylabel('KgCO2eq', fontsize=10)  # เพิ่ม label ที่แกน y สำหรับกราฟข้อมูลกระบวนการ
        subplot_process.plot(x_process, y_process)
        subplot_process.set_title('Process', fontsize=12, fontweight='bold')  # กำหนดชื่อกราฟของข้อมูลกระบวนการ

        buffer_process = BytesIO()
        figure_process.savefig(buffer_process, format="png")
        img_process = openpyxl.drawing.image.Image(buffer_process)
        sheet.add_image(img_process, f"E{max(len(input), len(process)) + 20}")

        align = openpyxl.styles.Alignment(horizontal="center", vertical="center")

        # กำหนดค่าที่จะเป็นกรอบ
        border = Border(left=Side(border_style='medium', color='000000'),
                    right=Side(border_style='medium', color='000000'),
                    top=Side(border_style='medium', color='000000'),
                    bottom=Side(border_style='medium', color='000000'))
    
        # กำหนดหัวคอลัมน์
        sheet['A2'] = "Name"
        sheet['A2'].border = border
        sheet['A2'].alignment = align
        
        sheet['B2'] = "Emission Factor"
        sheet['B2'].border = border
        sheet['B2'].alignment = align

        sheet['C2'] = "Amount"
        sheet['C2'].border = border
        sheet['C2'].alignment = align

        sheet['D2'] = "Unit"
        sheet['D2'].border = border
        sheet['D2'].alignment = align

        sheet['E2'] = "Name"
        sheet['E2'].border = border
        sheet['E2'].alignment = align

        sheet['F2'] = "Emission Factor"
        sheet['F2'].border = border
        sheet['F2'].alignment = align

        sheet['G2'] = "Amount"
        sheet['G2'].border = border
        sheet['G2'].alignment = align

        sheet['H2'] = "Unit"
        sheet['H2'].border = border
        sheet['H2'].alignment = align

        # กำหนดความกว้างของคอลัมน์
        max_lengths = {
            "A": max(len("Name"), max(len(item[0]) for item in input)),
            "B": max(len("Emission Factor"), max(len(str(item[1])) for item in input)),
            "C": max(len("Amount"), max(len(str(item[2])) for item in input)),
            "D": max(len("Unit"), max(len(item[3]) for item in input)),
            "E": max(len("Name"), max(len(item[0]) for item in process)),
            "F": max(len("Emission Factor"), max(len(str(item[1])) for item in process)),
            "G": max(len("Amount"), max(len(str(item[2])) for item in process)),
            "H": max(len("Unit"), max(len(item[3]) for item in process)),}

        for col, width in max_lengths.items():
            sheet.column_dimensions[col].width = width + 2  # เพิ่มความกว้างเพิ่มเติมสำหรับการเติม

        # ผสานเซลล์
        sheet.merge_cells("A1:D1")
        sheet["A1"].value = "Input"
        sheet["A1"].alignment = align

        sheet.merge_cells("E1:H1")
        sheet["E1"].value = "Process"
        sheet["E1"].alignment = align

        # ใส่กรอบเฉพาะขอบด้านนอกของช่วงเซลล์ A3:D20 และ E3:H20
        def apply_outer_border(sheet, min_row, max_row, min_col, max_col, border):
            rows = list(sheet.iter_rows(min_row=min_row, max_row=max_row, min_col=min_col, max_col=max_col))
            for row in rows:
                for cell in row:
                    if cell.row == min_row:
                        cell.border = cell.border + Border(top=border.top)
                    if cell.row == max_row:
                        cell.border = cell.border + Border(bottom=border.bottom)
                    if cell.column == min_col:
                        cell.border = cell.border + Border(left=border.left)
                    if cell.column == max_col:
                        cell.border = cell.border + Border(right=border.right)

        medium_border = Side(style='medium')
        outer_border = Border(left=medium_border, right=medium_border, top=medium_border, bottom=medium_border)

        # ใส่กรอบด้านนอกให้กับช่วงเซลล์ A1:D20 และ E1:H20
        apply_outer_border(sheet, 1, 20, 1, 4, outer_border)
        apply_outer_border(sheet, 1, 20, 5, 8, outer_border)

        data = []
        for i in range(max(len(input), len(process))):
            if i + 1 > len(input): 
                input.append(('', '', '', ''))
            if i + 1 > len(process):
                process.append(('', '', '', ''))
            data.append(input[i] + process[i])

        for row_index, row in enumerate(data):
            for col_index, value in enumerate(row):
                sheet.cell(row=row_index + 3, column=col_index + 1, value=value)

        # ซูมหน้า Excel เป็น 50%
        sheet.sheet_view.zoomScale = 70

        file_path = filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[("Excel files", "*.xlsx")])
    
        if file_path:
            wb.save(file_path) 
            print(f"บันทึกไฟล์ที่: {file_path}")
        else:
            print("การบันทึกไฟล์ถูกยกเลิก")

    
