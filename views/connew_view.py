import tkinter as tk
from tkinter import ttk

# controller = None

class ConnewView(ttk.Frame):

    def __init__(self, controller, app):
        super().__init__(app)
        self.controller = controller

       # Window

        self.entry_input = ttk.Entry(self, text = "Input", justify='center')
        self.entry_profile1.grid(row=3, column=3, padx=10, pady=10, sticky='N')

        self.entry_input = ttk.Entry(self, text = "Process", justify='center')
        self.entry_profile1.grid(row=3, column=4, padx=10, pady=10, sticky='N')

        self.label_totalcf = ttk.Label(self, text = "Total CF", justify='center')
        self.label_totalcf.grid(row=5,column=0, padx=10, pady=10)

        self.label_cf = ttk.Label(self, text = "CF", justify='center')
        self.label_cf.grid(row=5,column=1, padx=10, pady=10)

        self.label_unit = ttk.Label(self, text = "Unit", justify='center')
        self.label_unit.grid(row=5,column=2, padx=10, pady=10)
        
        self.backtomain_button = ttk.Button(self, text="Return to Profile", command=self.back)
        self.backtomain_button.grid(row=6, column=2, padx=10, pady=10, ipadx=10, ipady=10)

        # self.complete_button = ttk.Button(self, text="Export")
        # self.complete_button.grid(row=5, column=1, padx=10, pady=10, ipadx=10, ipady=10)

        # Budgets
        self.listmat_treeview = ttk.Treeview(self, columns=("Detail"), show="headings")
        self.listmat_treeview.heading("Detail", text="Detail" )
        self.listmat_treeview.grid(row=1, rowspan=2, column=0, padx=5, pady=5)
        self.listmat_treeview.insert("", "end")

        self.listtranspot_treeview = ttk.Treeview(self, columns=("Detail"), show="headings")
        self.listtranspot_treeview.heading("Detail", text="Detail" )
        self.listtranspot_treeview.grid(row=1, rowspan=2, column=1, padx=5, pady=5)
        self.listtranspot_treeview.insert("", "end")

        self.listbreakeven_treeview = ttk.Treeview(self, columns=("Detail"), show="headings")
        self.listbreakeven_treeview.heading("Detail", text="Detail" )
        self.listbreakeven_treeview.grid(row=3, rowspan=2, column=0, columnspan=2 , padx=5, pady=5)
        self.listbreakeven_treeview.insert("", "end")
        
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