import tkinter as tk
from tkinter import ttk

# controller = None

class ConprepareView(ttk.Frame):

    def __init__(self, controller, app):
        super().__init__(app)
        self.controller = controller

       # Window

        self.label_totalcf = ttk.Label(self, text = "Total CF", justify='center')
        self.label_totalcf.grid(row=4,column=0, padx=10, pady=10)

        self.label_cf = ttk.Label(self, text = "CF", justify='center')
        self.label_cf.grid(row=4,column=1, padx=10, pady=10)

        self.label_unit = ttk.Label(self, text = "Unit", justify='center')
        self.label_unit.grid(row=4,column=2, padx=10, pady=10)
        
        self.backtomain_button = ttk.Button(self, text="Return to Profile")
        self.backtomain_button.grid(row=5, column=2, padx=10, pady=10, ipadx=10, ipady=10)

        # self.complete_button = ttk.Button(self, text="Export")
        # self.complete_button.grid(row=5, column=1, padx=10, pady=10, ipadx=10, ipady=10)

        # Budgets
        self.listmat_treeview = ttk.Treeview(self, columns=("Detail"), show="headings")
        self.listmat_treeview.heading("Detail", text="Detail" )
        self.listmat_treeview.grid(row=0, rowspan=2, column=0, padx=5, pady=5)
        self.listmat_treeview.insert("", "end")

        self.listtranspot_treeview = ttk.Treeview(self, columns=("Detail"), show="headings")
        self.listtranspot_treeview.heading("Detail", text="Detail" )
        self.listtranspot_treeview.grid(row=0, rowspan=2, column=1, padx=5, pady=5)
        self.listtranspot_treeview.insert("", "end")

        self.listbreakeven_treeview = ttk.Treeview(self, columns=("Detail"), show="headings")
        self.listbreakeven_treeview.heading("Detail", text="Detail" )
        self.listbreakeven_treeview.grid(row=2, rowspan=2, column=0, columnspan=2 , padx=5, pady=5)
        self.listbreakeven_treeview.insert("", "end")
        
# สร้าง root window
# root = tk.Tk()
# root.title("Conprepare View")

# สร้างอ็อบเจกต์ของ BreakpointView แล้วแสดงหน้าต่าง
# conprepare_view = ConprepareView(controller=None, app=root)
# conprepare_view.pack()

# เริ่ม main loop
# root.mainloop()