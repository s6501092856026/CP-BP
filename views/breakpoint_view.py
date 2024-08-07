import tkinter as tk
from tkinter import ttk, messagebox
from controllers.tooltip_controller import ToolTipController

class BreakpointView(ttk.Frame):

    def __init__(self, controller, app):
        super().__init__(app)
        self.controller = controller

        self.back_button = ttk.Button(self, text="Back", command=self.back)
        self.back_button.grid(row=12, column=0, padx=5, pady=10, sticky='W')

        self.label_profile = ttk.Label(self, text = "Profile Name", font=('Tohama', 11, 'bold'), background='white')
        self.label_profile.grid(row=0, column=0, padx=10, pady=10, sticky='W')

        self.label_add = ttk.Label(self, text="", font=('Tohama', 11), background='white')
        self.label_add.grid(row=0, column=1, columnspan=2, padx=10, pady=10, sticky='')
        
        self.label_fixedcost = ttk.Label(self, text = "Fixed cost", font=('Tohama', 11, 'bold'), background='white')
        self.label_fixedcost.grid(row=1, column=0, padx=10, pady=10, sticky='W')

        self.label_variablecost = ttk.Label(self, text = "Variable cost", font=('Tohama', 11, 'bold'), background='white')
        self.label_variablecost.grid(row=3, column=0, padx=10, pady=10, sticky='W')

        self.label_number = ttk.Label(self, text = "Number of Unit", font=('Tohama', 11, 'bold'), background='white')
        self.label_number.grid(row=5, column=0, padx=10, pady=10, sticky='W')
        
        self.label_price = ttk.Label(self, text = "Price of Unit", font=('Tohama', 11, 'bold'), background='white')
        self.label_price.grid(row=7, column=0, padx=10, pady=10, sticky='W')
        
        self.label_efficieny = ttk.Label(self, text = "Production Efficieny", font=('Tohama', 11, 'bold'), background='white')
        self.label_efficieny.grid(row=9, column=0, padx=10, pady=10, sticky='W')

        self.entry_fixedcost = ttk.Entry(self, width=30, font=('Tohama', 11))
        self.entry_fixedcost.grid(row=1, column=1, columnspan=2, padx=10, pady=10)
        self.entry_fixedcost.bind("<FocusOut>", self.format_currency)
        
        self.entry_variablecost = ttk.Entry(self, width=30, font=('Tohama', 11))
        self.entry_variablecost.grid(row=3, column=1, columnspan=2, padx=10, pady=10)
        self.entry_variablecost.bind("<FocusOut>", self.format_currency)
        
        self.entry_number = ttk.Entry(self, width=30, font=('Tohama', 11))
        self.entry_number.grid(row=5, column=1, columnspan=2, padx=10, pady=10)
        self.entry_number.bind("<FocusOut>", self.format_currency)
        
        self.entry_price = ttk.Entry(self, width=30, font=('Tohama', 11))
        self.entry_price.grid(row=7, column=1, columnspan=2, padx=10, pady=10)
        self.entry_price.bind("<FocusOut>", self.format_currency)
        
        self.entry_efficieny = ttk.Entry(self, width=30, font=('Tohama', 11))
        self.entry_efficieny.grid(row=9, column=1, columnspan=2, padx=10, pady=10)

        self.label_fixedcost_unit = ttk.Label(self, text = "Baht", font=('Tohama', 11, 'bold'), background='white')
        self.label_fixedcost_unit.grid(row=1, column=3, padx=10, pady=10)
        
        self.label_variablecost_unit = ttk.Label(self, text = "Baht", font=('Tohama', 11, 'bold'), background='white')
        self.label_variablecost_unit.grid(row=3, column=3, padx=10, pady=10)
        
        self.label_number_unit = ttk.Label(self, text = "Unit", font=('Tohama', 11, 'bold'), background='white')
        self.label_number_unit.grid(row=5, column=3, padx=10, pady=10)
        
        self.label_price_unit = ttk.Label(self, text = "Baht", font=('Tohama', 11, 'bold'), background='white')
        self.label_price_unit.grid(row=7, column=3, padx=10, pady=10)
        
        self.label_efficiecy_unit = ttk.Label(self, text = "%", font=('Tohama', 11, 'bold'), background='white')
        self.label_efficiecy_unit.grid(row=9, column=3, padx=10, pady=10)
        
        self.save_as_button = ttk.Button(self, text = "Save As", command=controller.save_as)
        self.save_as_button.grid(row=12, column=3, columnspan=2, padx=10, pady=10)

        self.add_button_tooltips()

    def add_button_tooltips(self):
        ToolTipController(self.save_as_button, "บันทึกรายการ")
        ToolTipController(self.back_button, "กลับไปยังหน้าหลัก")

    def back(self):
        self.controller.back_main()

    def format_currency(self, event):
        try:
            widget = event.widget
            value = float(widget.get().replace(',', ''))
            formatted_value = "{:,.2f}".format(value)
            widget.delete(0, tk.END)
            widget.insert(0, formatted_value)
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter a valid number.")