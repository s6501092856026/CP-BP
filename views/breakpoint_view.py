from tkinter import ttk
from controllers.tooltip_controller import ToolTipController

class BreakpointView(ttk.Frame):

    def __init__(self, controller, app):
        super().__init__(app)
        self.controller = controller

        self.back_button = ttk.Button(self, text="ย้อนกลับ", command=self.back)
        self.back_button.grid(row=12, column=0, padx=5, pady=10, sticky='W')

        self.label_profile = ttk.Label(self, text = "ชื่อโปรไฟล์")
        self.label_profile.grid(row=0, column=0, padx=10, pady=10, sticky='W')

        self.label_add = ttk.Label(self, text="")
        self.label_add.grid(row=0, column=1, columnspan=2, padx=10, pady=10, sticky='')
        
        self.label_fixedcost = ttk.Label(self, text = "ต้นทุนคงที่")
        self.label_fixedcost.grid(row=1, column=0, padx=10, pady=10, sticky='W')

        self.label_variablecost = ttk.Label(self, text = "ต้นทุนผันแปร")
        self.label_variablecost.grid(row=3, column=0, padx=10, pady=10, sticky='W')

        self.label_number = ttk.Label(self, text = "ปริมาณการผลิต")
        self.label_number.grid(row=5, column=0, padx=10, pady=10, sticky='W')
        
        self.label_price = ttk.Label(self, text = "ราคาขายต่อหน่วย")
        self.label_price.grid(row=7, column=0, padx=10, pady=10, sticky='W')
        
        self.label_efficieny = ttk.Label(self, text = "กำลังการผลิต")
        self.label_efficieny.grid(row=9, column=0, padx=10, pady=10, sticky='W')

        self.entry_fixedcost = ttk.Entry(self, width=30)
        self.entry_fixedcost.grid(row=1, column=1, columnspan=2, padx=10, pady=10)
        
        self.entry_variablecost = ttk.Entry(self, width=30)
        self.entry_variablecost.grid(row=3, column=1, columnspan=2, padx=10, pady=10)
        
        self.entry_number = ttk.Entry(self, width=30)
        self.entry_number.grid(row=5, column=1, columnspan=2, padx=10, pady=10)
        
        self.entry_price = ttk.Entry(self, width=30)
        self.entry_price.grid(row=7, column=1, columnspan=2, padx=10, pady=10)
        
        self.entry_efficieny = ttk.Entry(self, width=30)
        self.entry_efficieny.grid(row=9, column=1, columnspan=2, padx=10, pady=10)

        self.label_fixedcost_unit = ttk.Label(self, text = "บาท")
        self.label_fixedcost_unit.grid(row=1, column=3, padx=10, pady=10)
        
        self.label_variablecost_unit = ttk.Label(self, text = "บาท")
        self.label_variablecost_unit.grid(row=3, column=3, padx=10, pady=10)
        
        self.label_number_unit = ttk.Label(self, text = "หน่วย")
        self.label_number_unit.grid(row=5, column=3, padx=10, pady=10)
        
        self.label_price_unit = ttk.Label(self, text = "บาท")
        self.label_price_unit.grid(row=7, column=3, padx=10, pady=10)
        
        self.label_efficieny_unit = ttk.Label(self, text = "%")
        self.label_efficieny_unit.grid(row=9, column=3, padx=10, pady=10)
        
        self.save_as_button = ttk.Button(self, text = "บันทึกเป็น", command=controller.save_as)
        self.save_as_button.grid(row=12, column=3, columnspan=2, padx=10, pady=10)

        self.add_button_tooltips()

    def add_button_tooltips(self):
        ToolTipController(self.save_as_button, "บันทึกรายการ")
        ToolTipController(self.back_button, "กลับไปยังหน้าหลัก")

    def back(self):
        self.controller.back_main()