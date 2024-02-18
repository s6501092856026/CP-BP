import tkinter as tk
from tkinter import ttk

#controller = None

class DetailView(ttk.Frame):

    def __init__(self, controller, app):
        super().__init__(app)
        self.controller = controller

        self.label_name_select = ttk.Label(self, text = "Name Select")
        self.label_name_select.grid(row=0, column=0, padx=10, pady=10)

        self.label_unit = ttk.Label(self, text = "Unit")
        self.label_unit.grid(row=0, column=3, padx=10, pady=10)

        self.entry_total_number = ttk.Entry(self, width=30)
        self.entry_total_number.grid(row=0, column=1,columnspan=2, padx=10, pady=10)
        
        self.accept_button = ttk.Button(self, text = "Accept")
        self.accept_button.grid(row=3, column=0, columnspan=2, padx=10, pady=10)

        self.cancel_button = ttk.Button(self, text = "Cancel")
        self.cancel_button.grid(row=3, column=2, columnspan=2, padx=10, pady=10)

# สร้าง root window
#root = tk.Tk()
#root.title("Detail View")

# สร้างอ็อบเจกต์ของ BreakpointView แล้วแสดงหน้าต่าง
#detail_view = DetailView(controller=None, app=root)
#detail_view.pack()

# เริ่ม main loop
#root.mainloop()