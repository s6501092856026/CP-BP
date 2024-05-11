import tkinter as tk
from tkinter import ttk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# controller = None

class ConnewView(ttk.Frame):

    def __init__(self, controller, app):
        super().__init__(app)
        self.controller = controller

        # Window
        self.main_frame =  ttk.Frame(self)

        self.label_input = ttk.Label(self, text = "Input", justify='center', foreground="black", font=("Times New Roman", 10, "bold"))
        self.label_input.grid(row=0, column=0, padx=10, pady=10, sticky='N')

        self.label_process = ttk.Label(self, text = "Process", justify='center', foreground="black", font=("Times New Roman", 10, "bold"))
        self.label_process.grid(row=0, column=1, padx=10, pady=10, sticky='N')

        self.label_output = ttk.Label(self, text = "Output", justify='center', foreground="black", font=("Times New Roman", 10, "bold"))
        self.label_output.grid(row=0, column=2, padx=10, pady=10, sticky='N')

        self.label_totalcf = ttk.Label(self, text = "Total CF", justify='center', foreground="black", font=("Times New Roman", 10, "bold"))
        self.label_totalcf.grid(row=7,column=0, padx=10, pady=10)

        self.label_cf = ttk.Label(self, text = "CF", justify='center', foreground="black", font=("Times New Roman", 10, "bold"))
        self.label_cf.grid(row=7,column=1, padx=10, pady=10)

        self.label_unit = ttk.Label(self, text = "Unit", justify='center', foreground="black", font=("Times New Roman", 10, "bold"))
        self.label_unit.grid(row=7,column=2, padx=10, pady=10)
        
        self.return_button = ttk.Button(self, text="Return to Profile", command=self.back)
        self.return_button.grid(row=8, column=3, padx=10, pady=10, ipadx=10, ipady=10)

        
        # GRAPH



        # self.process_treeview = ttk.Treeview(self, columns=("Graph"), show="headings")
        # self.process_treeview.heading("Graph", text="Graph" )
        # self.process_treeview.grid(row=1, rowspan=2, column=1)

        # self.output_treeview = ttk.Treeview(self, columns=("Graph"), show="headings")
        # self.output_treeview.heading("Graph", text="Graph" )
        # self.output_treeview.grid(row=1, rowspan=2, column=2)


        # TREE VIEW
        self.detail1_treeview = ttk.Treeview(self, columns=("Input"), show="headings")
        self.detail1_treeview.heading("Input", text="Input" )
        self.detail1_treeview.grid(row=3, rowspan=2, column=0)

        self.detail2_treeview = ttk.Treeview(self, columns=("Process"), show="headings")
        self.detail2_treeview.heading("Process", text="Process" )
        self.detail2_treeview.grid(row=3, rowspan=2, column=1)

        self.detail3_treeview = ttk.Treeview(self, columns=("Output"), show="headings")
        self.detail3_treeview.heading("Output", text="Output" )
        self.detail3_treeview.grid(row=3, rowspan=2, column=2)

        # self.listbreakeven_treeview = ttk.Treeview(self, columns=("Detail"), show="headings")
        # self.listbreakeven_treeview.heading("Detail", text="Detail" )
        # self.listbreakeven_treeview.grid(row=5, rowspan=2, column=0)
        # self.listbreakeven_treeview.insert("", "end")
        self.setInputGraph()
        self.setOutputGraph()
        self.setProcessGraph()

    def setProcessGraph(self):

        # Create a Matplotlib figure
        figure = Figure(figsize=(4,2), dpi=70)
        subplot = figure.add_subplot(111)

        # Query from database
        # Line data
        x = ["รถตู้", "รถกระบะ", "รถตู้พ่วง"]
        y = [2, 4, 1]

        # Create graph
        subplot.plot(x,y)

        # Create a FigurecanvasTkAgg widget
        canvas = FigureCanvasTkAgg(figure, master=self)
        canvas.draw()
        canvas.get_tk_widget().grid(row=1, rowspan=2, column=1) 
        

    def setOutputGraph(self):

        # Create a Matplotlib figure
        figure = Figure(figsize=(4,2), dpi=70)
        subplot = figure.add_subplot(111)

        # Query from database
        # Line data
        x = ["รถตู้", "รถกระบะ", "รถตู้พ่วง"]
        y = [2, 4, 1]

        # Create graph
        subplot.plot(x,y)

        # Create a FigurecanvasTkAgg widget
        canvas = FigureCanvasTkAgg(figure, master=self)
        canvas.draw()
        canvas.get_tk_widget().grid(row=1, rowspan=2, column=2) 
        

    def setInputGraph(self):

        # Create a Matplotlib figure
        figure = Figure(figsize=(4,2), dpi=70)
        subplot = figure.add_subplot(111)

        # Query from database
        # Line data
        x = ["รถตู้", "รถกระบะ", "รถตู้พ่วง"]
        y = [2, 4, 1]

        # Create graph
        subplot.plot(x,y)

        # Create a FigurecanvasTkAgg widget
        canvas = FigureCanvasTkAgg(figure, master=self)
        canvas.draw()
        canvas.get_tk_widget().grid(row=1, rowspan=2, column=0) 
        

    def breakeven(self):
        self.controller.show_break()

    def back(self):
        self.controller.back_main()

# สร้าง root window
# root = tk.Tk()
# root.title("Connew View")

# สร้างอ็อบเจกต์ของ BreakpointView แล้วแสดงหน้าต่าง
# connew_view = ConnewView(controller=None, app=root)
# connew_view.pack()

# เริ่ม main loop
# root.mainloop()