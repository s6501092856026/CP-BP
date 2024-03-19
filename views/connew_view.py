import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt

# controller = None

class ConnewView(ttk.Frame):

    def __init__(self, controller, app):
        super().__init__(app)
        self.controller = controller

       # Window

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

        # self.complete_button = ttk.Button(self, text="Export")
        # self.complete_button.grid(row=5, column=1, padx=10, pady=10, ipadx=10, ipady=10)

        # Budgets

        # Input Graph Frame (new)
        # self.input_graph_frame = ttk.Frame(self)
        # self.input_graph_frame.grid(row=1, rowspan=2, column=0)

        # Placeholder label for the graph (initially)
        # self.input_graph_label = ttk.Label(self.input_graph_frame, text="Input Graph")
        # self.input_graph_label.grid(row=0, rowspan=2, column=0, sticky='nsew')

        self.input_treeview = ttk.Treeview(self, columns=("Graph"), show="headings")
        self.input_treeview.heading("Graph", text="Graph" )
        self.input_treeview.grid(row=1, rowspan=2, column=0)
        self.input_treeview.insert("", "end")

        self.detail1_treeview = ttk.Treeview(self, columns=("Input"), show="headings")
        self.detail1_treeview.heading("Input", text="Input" )
        self.detail1_treeview.grid(row=3, rowspan=2, column=0)
        
        self.process_treeview = ttk.Treeview(self, columns=("Graph"), show="headings")
        self.process_treeview.heading("Graph", text="Graph" )
        self.process_treeview.grid(row=1, rowspan=2, column=1)

        self.detail2_treeview = ttk.Treeview(self, columns=("Process"), show="headings")
        self.detail2_treeview.heading("Process", text="Process" )
        self.detail2_treeview.grid(row=3, rowspan=2, column=1)

        self.output_treeview = ttk.Treeview(self, columns=("Graph"), show="headings")
        self.output_treeview.heading("Graph", text="Graph" )
        self.output_treeview.grid(row=1, rowspan=2, column=2)

        self.detail3_treeview = ttk.Treeview(self, columns=("Output"), show="headings")
        self.detail3_treeview.heading("Output", text="Output" )
        self.detail3_treeview.grid(row=3, rowspan=2, column=2)

        # self.listbreakeven_treeview = ttk.Treeview(self, columns=("Detail"), show="headings")
        # self.listbreakeven_treeview.heading("Detail", text="Detail" )
        # self.listbreakeven_treeview.grid(row=5, rowspan=2, column=0)
        # self.listbreakeven_treeview.insert("", "end")
        
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