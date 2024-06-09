import tkinter as tk
from tkinter import ttk, filedialog
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

        self.label_totalcf = ttk.Label(self, text = "Total CF", justify='center', foreground="black", font=("Times New Roman", 10, "bold"))
        self.label_totalcf.grid(row=7,column=0, padx=10, pady=10)

        self.label_cf = ttk.Label(self, text = "CF")
        self.label_cf.grid(row=7,column=1, padx=10, pady=10, sticky = 'W')

        self.label_unit = ttk.Label(self, text = "Unit", foreground="black", font=("Times New Roman", 10, "bold"))
        self.label_unit.grid(row=7,column=1, padx=10, pady=10, sticky = 'E')
        
        self.return_button = ttk.Button(self, text="Return to Profile", command=self.back)
        self.return_button.grid(row=8, column=0, padx=10, pady=10, ipadx=10, ipady=10, sticky = 'W')

        self.export_button = ttk.Button(self, text="Export to Excel", command=self.export)
        self.export_button.grid(row=8, column=1, padx=10, pady=10, ipadx=10, ipady=10, sticky = 'E')

        # TREE VIEW
        self.profile01_treeview = ttk.Treeview(self, columns=("Name", "Amount", "Unit"), show="headings")
        self.profile01_treeview.heading("Name", text="Name")
        self.profile01_treeview.column("Name", width=310)
        self.profile01_treeview.heading("Amount", text="Amount")
        self.profile01_treeview.column("Amount", width=100)
        self.profile01_treeview.heading("Unit", text="Unit")
        self.profile01_treeview.column("Unit", width=40)
        self.profile01_treeview.grid(row=3, rowspan=2, column=0, padx=5, pady=5)

        self.profile02_treeview = ttk.Treeview(self, columns=("Name", "Amount", "Unit"), show="headings")
        self.profile02_treeview.heading("Name", text="Name")
        self.profile02_treeview.column("Name", width=310)
        self.profile02_treeview.heading("Amount", text="Amount")
        self.profile02_treeview.column("Amount", width=100)
        self.profile02_treeview.heading("Unit", text="Unit")
        self.profile02_treeview.column("Unit", width=40)
        self.profile02_treeview.grid(row=3, rowspan=2, column=1, padx=5, pady=5)

       
        # self.listbreakeven_treeview = ttk.Treeview(self, columns=("Detail"), show="headings")
        # self.listbreakeven_treeview.heading("Detail", text="Detail" )
        # self.listbreakeven_treeview.grid(row=5, rowspan=2, column=0)
        # self.listbreakeven_treeview.insert("", "end")

    def setCompareGraph(self, items):

        # Create a Matplotlib figure
        figure = Figure(figsize=(8,4), dpi=70)
        subplot = figure.add_subplot(111)

        # Query from database
        # Line data
        # x = ["รถตู้", "รถกระบะ", "รถตู้พ่วง"]
        # y = [2, 4, 1]
        x = []
        y = []
        for item in items:
            x.append(item[0])
            y.append(float(item[1]))

        #  Set font
        subplot.tick_params(axis='x', labelrotation=90, labelfontfamily="tahoma")
        
        # Create graph
        subplot.plot(x,y)

        # Create a FigurecanvasTkAgg widget
        canvas = FigureCanvasTkAgg(figure, master=self)
        canvas.draw()
        canvas.get_tk_widget().grid(row=1, rowspan=2, column=1, padx=5, pady=5) 
        

    def breakeven(self):
        self.controller.show_break()

    def back(self):
        self.controller.back_main()

    def setConclusion(self, items) :
        self.profile01_treeview.delete(*self.profile01_treeview.get_children())
        self.profile02_treeview.delete(*self.profile02_treeview.get_children())
        inputGraph = []
        outputGraph = []
        processGraph = []

        for item in items:
            category, _, name, amount, unit = item
            
            # self.profile01_treeview
            if category == 'Material':
                processGraph.append((name, amount))
                self.profile01_treeview.insert("", "end", values=(name, amount, unit))
            elif category == 'Transpotation':
                inputGraph.append((name, amount))
                outputGraph.append((name, amount))
                self.profile01_treeview.insert("", "end", values=(name, amount, unit))
                self.output_treeview.insert("", "end", values=(name, amount, unit))
            elif category == 'Performance':
                processGraph.append((name, amount))
                self.profile01_treeview.insert("", "end", values=(name, amount, unit))
        self.setCompareGraph(processGraph)
        self.items = items

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
        sheet["A1"].value = "Input"
        sheet["A1"].alignment = align
        sheet.merge_cells("D1:F1")
        sheet["D1"].value = "Process"
        sheet["D1"].alignment = align
        sheet.merge_cells("G1:I1")
        sheet['G1'].value = "Output"
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