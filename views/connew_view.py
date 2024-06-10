import tkinter as tk
from tkinter import ttk, filedialog
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import matplotlib.widgets as ZoomPan
import openpyxl.drawing
import openpyxl.drawing.image
import openpyxl.styles
import pandas as pd
import openpyxl
from io import BytesIO

class ConnewView(ttk.Frame):

    def __init__(self, controller, app):
        super().__init__(app)
        self.controller = controller
        self.items = []

        # Window
        self.main_frame =  ttk.Frame(self)

        self.label_name = ttk.Label(self, text = "ชื่อโปรไฟล์", font=(8))
        self.label_name.grid(row=0, column=0, padx=10, pady=10, sticky='NE')

        self.label_profile = ttk.Label(self, text = "", font=(8))
        self.label_profile.grid(row=0, column=1, padx=10, pady=10, sticky='NW')

        self.label_totalcf = ttk.Label(self, text = "ปริมาณค่าคาร์บอนเทียบเท่าทั้งหมด")
        self.label_totalcf.grid(row=7,column=0, padx=10, pady=10, sticky='W')

        self.label_cf = ttk.Label(self, text = "")
        self.label_cf.grid(row=7,column=1, padx=10, pady=10, sticky='W')

        self.label_unit = ttk.Label(self, text = "หน่วย")
        self.label_unit.grid(row=7,column=1, padx=10, pady=10, sticky='E')
        
        self.return_button = ttk.Button(self, text="Return to Profile", command=self.back)
        self.return_button.grid(row=8, column=0, padx=10, pady=10, ipadx=10, ipady=10, sticky = 'W')

        self.export_button = ttk.Button(self, text="Export to Excel", command=self.export)
        self.export_button.grid(row=8, column=1, padx=10, pady=10, ipadx=10, ipady=10, sticky = 'E')

        # TREE VIEW
        self.input_treeview = ttk.Treeview(self, columns=("Name", "Carbon", "Unit"), show="headings")
        self.input_treeview.heading("Name", text="ชื่อ")
        self.input_treeview.column("Name", width=310)
        self.input_treeview.heading("Carbon", text="ค่าคาร์บอนเทียบเท่า")
        self.input_treeview.column("Carbon", width=95)
        self.input_treeview.heading("Unit", text="หน่วย")
        self.input_treeview.column("Unit", width=60)
        self.input_treeview.grid(row=3, rowspan=2, column=0, padx=5, pady=5)

        self.process_treeview = ttk.Treeview(self, columns=("Name", "Carbon", "Unit"), show="headings")
        self.process_treeview.heading("Name", text="ชื่อ")
        self.process_treeview.column("Name", width=310)
        self.process_treeview.heading("Carbon", text="ค่าคาร์บอนเทียบเท่า")
        self.process_treeview.column("Carbon", width=95)
        self.process_treeview.heading("Unit", text="หน่วย")
        self.process_treeview.column("Unit", width=60)
        self.process_treeview.grid(row=3, rowspan=2, column=1, padx=5, pady=5)

        # self.output_treeview = ttk.Treeview(self, columns=("Name", "Carbon", "Unit"), show="headings")
        # self.output_treeview.heading("Name", text="ชื่อ")
        # self.output_treeview.column("Name", width=310)
        # self.output_treeview.heading("Carbon", text="ค่าคาร์บอนเทียบเท่า")
        # self.output_treeview.column("Carbon", width=95)
        # self.output_treeview.heading("Unit", text="หน่วย")
        # self.output_treeview.column("Unit", width=60)
        # self.output_treeview.grid(row=3, rowspan=2, column=2, padx=5, pady=5)

    def setProcessGraph(self, items):
        # Create a Matplotlib figure
        # figure = Figure(figsize=(6.5, 4), dpi=70)
        figure = plt.Figure(figsize=None, dpi=70)
        subplot = figure.add_subplot(111)
    
        # Query from database
        # Line data
        x = []
        y = []
        for item in items:
            x.append(item[0])
            y.append(float(item[1]))

        # Set font
        subplot.tick_params(axis='x', labelrotation=0, labelfontfamily="Tahoma", colors='white')
    
        # Create graph
        subplot.plot(x, y)
    
        # Add grid
        subplot.grid(True, linestyle='--', linewidth=0.5)

        # Add title
        subplot.set_title('Process', fontsize=12, fontweight='bold')

        # Customize tick labels
        subplot.tick_params(axis='both', which='major', labelsize=8)
    
        # Add labels to axes
        subplot.set_xlabel('Material and Performane', fontsize=8)
        subplot.set_ylabel('Emission factor', fontsize=8)

        # # Add legend
        # subplot.legend([''], loc='upper right', fontsize=8)

        # Customize borders
        subplot.spines['top'].set_visible(False)
        subplot.spines['right'].set_visible(False)

        # Create a FigureCanvasTkAgg widget
        canvas = FigureCanvasTkAgg(figure, master=self)
        canvas.draw()
        canvas.get_tk_widget().grid(row=1, rowspan=2, column=1, padx=5, pady=5)

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
        
    def setInputGraph(self, items):
        # Create a Matplotlib figure
        # figure = Figure(figsize=(6.5, 4), dpi=70)
        figure = plt.figure(figsize=None, dpi=70)
        subplot = figure.add_subplot(111)
    
        # Query from database
        # Line data
        x = []
        y = []
        for item in items:
            x.append(item[0])
            y.append(float(item[1]))

        # Set font
        subplot.tick_params(axis='x', labelrotation=0, labelfontfamily="Tahoma", colors='white')
    
        # Create graph
        subplot.plot(x, y)
    
        # Add grid
        subplot.grid(True, linestyle='--', linewidth=0.5)

        # Add title
        subplot.set_title('Input', fontsize=12, fontweight='bold')

        # Customize tick labels
        subplot.tick_params(axis='both', which='major', labelsize=8)
    
        # Add labels to axes
        subplot.set_xlabel('Transpotation', fontsize=8)
        subplot.set_ylabel('Emission factor', fontsize=8)

        # # Add legend
        # subplot.legend(['Legend'], loc='upper right', fontsize=8)

        # Customize borders
        subplot.spines['top'].set_visible(False)
        subplot.spines['right'].set_visible(False)

        # Create a FigureCanvasTkAgg widget
        canvas = FigureCanvasTkAgg(figure, master=self)
        canvas.draw()
        canvas.get_tk_widget().grid(row=1, rowspan=2, column=0, padx=5, pady=5)

    def back(self):
        self.controller.back_main()

    def setConclusion(self, profile_name, items) :
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
                self.process_treeview.insert("", "end", values=(name, round(float(factor) * float(amount), 3), "KgCO2eq"))
                total_cf += float(factor) * float(amount)  # เพิ่มค่า Carbon ลงในผลรวม

            elif category == 'Transpotation':
                inputGraph.append((name, round(float(factor) * float(amount), 3)))
                outputGraph.append((name, round(float(factor) * float(amount), 3)))
                self.input_treeview.insert("", "end", values=(name, round(float(factor) * float(amount), 3), "KgCO2eq"))
                # self.output_treeview.insert("", "end", values=(name, round(float(factor) * float(amount), 3), "KgCO2eq"))
                total_cf += float(factor) * float(amount)  # เพิ่มค่า Carbon ลงในผลรวม

            elif category == 'Performance':
                processGraph.append((name, round(float(factor) * float(amount), 3)))
                self.process_treeview.insert("", "end", values=(name, round(float(factor) * float(amount), 3), "KgCO2eq"))
                total_cf += float(factor) * float(amount)  # เพิ่มค่า Carbon ลงในผลรวม

        self.label_cf.config(text="{:.3f}".format(total_cf))  # กำหนดผลรวมของค่า Carbon ลงใน label_cf

        self.setInputGraph(inputGraph)
        # self.setOutputGraph(outputGraph)
        self.setProcessGraph(processGraph)
        self.items = items
        self.label_profile.config(text=profile_name)

    def export(self):
        wb = openpyxl.Workbook()  # Creates a new workbook object
        sheet = wb.active  # Get the active sheet

        input = []
        process = [] 
        output = []
        for item in self.items:
            category, _, name, amount, unit = item
            
            if category == 'Material':
                process.append((name, amount, unit))              
            elif category == 'Transpotation':
                input.append((name, amount, unit))
                output.append((name, amount, unit))
            elif category == 'Performance':
                process.append((name, amount, unit))

        # Draw Graph
        figure = Figure(figsize=(5,3), dpi=70)
        subplot = figure.add_subplot(111)

        x = []
        y = []
        for item in input:
            x.append(item[0])
            y.append(float(item[1]))

        subplot.tick_params(axis='x', labelrotation=90, labelfontfamily="tahoma")
        subplot.plot(x,y)

        buffer = BytesIO()
        figure.savefig(buffer, format="png")
        img = openpyxl.drawing.image.Image(buffer)
        sheet.add_image(img, f"A{max( len(input), len(process), len(output)) + 5}")
      
        align = openpyxl.styles.Alignment(horizontal="center")
        
        sheet.merge_cells("A1:C1")
        sheet["A1"].value = "วัตถุดิบนำเข้า"
        sheet["A1"].alignment = align
        sheet.merge_cells("D1:F1")
        sheet["D1"].value = "กระบวนการผลิต"
        sheet["D1"].alignment = align
        sheet.merge_cells("G1:I1")
        sheet['G1'].value = "ส่งออกสินค้า"
        sheet["G1"].alignment = align

        data = []
        for i in range(max( len(input), len(process), len(output))):
            if i + 1  > len(input): 
                input.append(('', '', ''))
            if i + 1 > len(process):
                process.append(('', '', ''))
            if i + 1 > len(output):
                output.append(('', '', ''))
            data.append(input[i] + process[i] + output[i])

        print(data)        

        for row_index, row in enumerate(data):
            for col_index, value in enumerate(row):
                sheet.cell(row=row_index + 2, column=col_index + 1, value=value)
        
        file_path = filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[("Excel files", "*.xlsx")])
        
        if file_path:
            wb.save(file_path) 
            print(f"บันทึกไฟล์ที่: {file_path}")
        else:
            print("การบันทึกไฟล์ถูกยกเลิก")