import tkinter as tk
from tkinter import ttk

class BreakpointView(ttk.Frame):

    def __init__(self, controller, app):
        super().__init__(app)
        self.controller = controller

        self.back_button = ttk.Button(self, text="Back", command=self.back)
        self.back_button.grid(row=0, column=0, padx=5, pady=10, sticky='W')

        self.label_profile = ttk.Label(self, text = "Profile", foreground="black", font=("Times New Roman", 10, "bold"))
        self.label_profile.grid(row=0, column=0, padx=10, pady=10, sticky='E')

        self.label_add = ttk.Label(self, text = "", foreground="black", font=("Times New Roman", 10, "bold"))
        self.label_add.grid(row=0, column=1, columnspan=2, padx=10, pady=10, sticky='')
        
        self.label_fixedcost = ttk.Label(self, text = "Fixed Cost", foreground="black", font=("Times New Roman", 10, "bold"))
        self.label_fixedcost.grid(row=1, column=0, padx=10, pady=10)

        self.label_variablecost = ttk.Label(self, text = "Variable Cost", foreground="black", font=("Times New Roman", 10, "bold"))
        self.label_variablecost.grid(row=3, column=0, padx=10, pady=10)

        self.label_number = ttk.Label(self, text = "Number of Unit", foreground="black", font=("Times New Roman", 10, "bold"))
        self.label_number.grid(row=5, column=0, padx=10, pady=10)
        
        self.label_price = ttk.Label(self, text = "Price", foreground="black", font=("Times New Roman", 10, "bold"))
        self.label_price.grid(row=7, column=0, padx=10, pady=10)
        
        self.label_efficieny = ttk.Label(self, text = "Product Efficiency", foreground="black", font=("Times New Roman", 10, "bold"))
        self.label_efficieny.grid(row=9, column=0, padx=10, pady=10)
        
        self.label_amount = ttk.Label(self, text = "Amount of material per product", foreground="black", font=("Times New Roman", 10, "bold"))
        self.label_amount.grid(row=11, column=0, padx=10, pady=10)

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
        
        self.entry_amount = ttk.Entry(self, width=30)
        self.entry_amount.grid(row=11, column=1, columnspan=2, padx=10, pady=10)

        self.label_fixedcost_unit = ttk.Label(self, text = "Bath", foreground="black", font=("Times New Roman", 10))
        self.label_fixedcost_unit.grid(row=1, column=3, padx=10, pady=10)
        
        self.label_variablecost_unit = ttk.Label(self, text = "Bath", foreground="black", font=("Times New Roman", 10))
        self.label_variablecost_unit.grid(row=3, column=3, padx=10, pady=10)
        
        self.label_number_unit = ttk.Label(self, text = "Unit", foreground="black", font=("Times New Roman", 10))
        self.label_number_unit.grid(row=5, column=3, padx=10, pady=10)
        
        self.label_price_unit = ttk.Label(self, text = "Bath", foreground="black", font=("Times New Roman", 10))
        self.label_price_unit.grid(row=7, column=3, padx=10, pady=10)
        
        self.label_efficieny_unit = ttk.Label(self, text = "%", foreground="black", font=("Times New Roman", 10))
        self.label_efficieny_unit.grid(row=9, column=3, padx=10, pady=10)
        
        self.label_amount_unit = ttk.Label(self, text = "Unit", foreground="black", font=("Times New Roman", 10))
        self.label_amount_unit.grid(row=11, column=3, padx=10, pady=10)

        self.save_as_button = ttk.Button(self, text = "Save as")
        self.save_as_button.grid(row=12, column=3, columnspan=2, padx=10, pady=10)

    def back(self):
        self.controller.back_main()