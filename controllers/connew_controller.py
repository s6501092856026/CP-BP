import tkinter as tk
from tkinter import messagebox
from views.connew_view import ConnewView
from utils.database import DatabaseUtil
from utils.window import getCenterPosition

class ConnewController:

    def __init__(self, app):
        self.app = app
        self.connew_view = ConnewView(self, app)

    def show_connew(self, profile_name, items, breakpoint_data):
        self.connew_view.pack_forget()
        self.connew_view.setConclusion(profile_name, items, breakpoint_data)
        self.connew_view.pack(padx=10, pady=10, fill="both", expand=True)
        self.app.update_idletasks()
        widget_width = self.connew_view.winfo_reqwidth() + 20  # เพิ่ม padding
        widget_height = self.connew_view.winfo_reqheight() + 20  # เพิ่ม padding
        x, y = getCenterPosition(self.app, width=widget_width, height=widget_height)
        self.app.geometry(f"{widget_width}x{widget_height}+{x}+{y}")
    
    def back_main(self):
        self.connew_view.pack_forget()
        self.app.show_main()

    # def load_breakpoint_data(self, profile_name):
    #         db = DatabaseUtil.getInstance()
    #         existing_product = db.fetch_data("SELECT product_id FROM product WHERE product_name = %s", (profile_name,))
    #         if existing_product:
    #             product_id = existing_product[0][0]
    #             # ค้นหาข้อมูลจากตาราง breakeven_point ที่เกี่ยวข้องกับ product_id
    #             breakpoint_data = db.fetch_data("SELECT fixed_cost, variable_cost, number_of_units, unit_price, product_efficiency FROM breakeven_point WHERE product_id = %s", (product_id,))
    #             if breakpoint_data:
    #                 fixed_cost, variable_cost, number_of_units, unit_price, product_efficiency = breakpoint_data[0]
                    
    #                 # ใส่ค่าลงใน Label ผ่าน connew_view
    #                 self.connew_view.add_totalcost.config(float(fixed_cost) + (float(variable_cost) * float(number_of_units)))
    #                 self.connew_view.add_revenue.config(float(unit_price)* float(number_of_units))
    #                 self.connew_view.add_profit.config((float(unit_price)* float(number_of_units)) - (float(fixed_cost) + (float(variable_cost) * float(number_of_units))))
    #                 self.connew_view.add_breakeven.config(float(fixed_cost) / (float(unit_price) - float(variable_cost))) 
    #                 self.connew_view.add_efficiency.config(float(product_efficiency))

    def load_breakpoint_data(self, profile_name):
        db = DatabaseUtil.getInstance()
        existing_product = db.fetch_data("SELECT product_id FROM product WHERE product_name = %s", (profile_name,))
        print("Existing Product Data:", existing_product)
        if existing_product:
            product_id = existing_product[0][0]
            # Fetch data from the breakeven_point table related to product_id
            breakpoint_data = db.fetch_data("SELECT fixed_cost, variable_cost, number_of_units, unit_price, product_efficiency FROM breakeven_point WHERE product_id = %s", (product_id,))
            if breakpoint_data:
                self.show_connew(breakpoint_data)
            else:
                messagebox.showinfo("Break Even Point Not Found", f"No break even point found for product: {profile_name}")
        else:
            messagebox.showinfo("Product Not Found", f"No product found with name: {profile_name}")