import tkinter as tk
from tkinter import messagebox
from views.breakpoint_view import BreakpointView
from utils.window import getCenterPosition
from utils.database import DatabaseUtil

class BreakController:

    def __init__(self, app):
        self.app = app
        self.breakpoint_view = BreakpointView(self, app)

    def show_break(self, profile_name):
        self.update_label_add(profile_name)  # อัปเดตข้อมูลใน entry_add
        self.breakpoint_view.pack_forget()  # ลบการแพ็ควิดเจต์ breakpoint_view เพื่อลบออกจากหน้าต่าง (หากมีการแสดงผลอยู่ก่อนหน้านี้)
        self.breakpoint_view.pack(padx=10, pady=10, expand=True)  # แสดงวิดเจต์ breakpoint_view พร้อมกับการขยายตัวเต็มขอบเต็มหน้าจอ
        self.load_breakpoint_data(profile_name)  # โหลดข้อมูลจากฐานข้อมูลถ้ามี
        self.app.update_idletasks()  # อัพเดตวิดเจต์
        width = self.breakpoint_view.winfo_reqwidth() + 20  # เพิ่มขอบเขตบางส่วน
        height = self.breakpoint_view.winfo_reqheight() + 20  # เพิ่มขอบเขตบางส่วน
        x, y = getCenterPosition(self.app, width=width, height=height)
        self.app.geometry(f"{width}x{height}+{x}+{y}")

    def update_label_add(self, profile_name):
        self.breakpoint_view.label_add.config(text=profile_name)
    
    def back_main(self):
        self.breakpoint_view.pack_forget()
        self.app.show_main()

    def load_breakpoint_data(self, profile_name):
        try:
            db = DatabaseUtil.getInstance()
            existing_product = db.fetch_data("SELECT product_id FROM product WHERE product_name = %s", (profile_name,))
            if existing_product:
                product_id = existing_product[0][0]
                # ค้นหาข้อมูลจากตาราง breakeven_point ที่เกี่ยวข้องกับ product_id
                breakpoint_data = db.fetch_data("SELECT fixed_cost, variable_cost, number_of_units, unit_price, product_efficiency FROM breakeven_point WHERE product_id = %s", (product_id,))
                if breakpoint_data:
                    fixed_cost, variable_cost, number_of_units, unit_price, product_efficiency = breakpoint_data[0]
                    self.breakpoint_view.entry_fixedcost.delete(0, tk.END)
                    self.breakpoint_view.entry_fixedcost.insert(0, fixed_cost)
                    self.breakpoint_view.entry_variablecost.delete(0, tk.END)
                    self.breakpoint_view.entry_variablecost.insert(0, variable_cost)
                    self.breakpoint_view.entry_number.delete(0, tk.END)
                    self.breakpoint_view.entry_number.insert(0, number_of_units)
                    self.breakpoint_view.entry_price.delete(0, tk.END)
                    self.breakpoint_view.entry_price.insert(0, unit_price)
                    self.breakpoint_view.entry_efficieny.delete(0, tk.END)
                    self.breakpoint_view.entry_efficieny.insert(0, product_efficiency)
        except Exception as e:
            messagebox.showerror("ข้อผิดพลาด", f"เกิดข้อผิดพลาดในขณะที่พยายามโหลดข้อมูล: {str(e)}")

    # def save_as(self):
    #     profile_name = self.breakpoint_view.label_add.cget("text")
    #     fixed_cost = self.breakpoint_view.entry_fixedcost.get()
    #     variable_cost = self.breakpoint_view.entry_variablecost.get()
    #     number_of_units = self.breakpoint_view.entry_number.get()
    #     price = self.breakpoint_view.entry_price.get()
    #     efficiency = self.breakpoint_view.entry_efficieny.get()

    #     # ตรวจสอบความสมบูรณ์ของข้อมูล
    #     if not all((profile_name, fixed_cost, variable_cost, number_of_units, price, efficiency)):
    #         messagebox.showwarning("คำเตือน", "กรุณากรอกข้อมูลให้ครบถ้วน")
    #         return

    #     try:
    #         db = DatabaseUtil.getInstance()

    #         # ค้นหา product_id จากชื่อโปรไฟล์
    #         existing_product = db.fetch_data("SELECT product_id FROM product WHERE product_name = %s", (profile_name,))
    #         if existing_product:
    #             product_id = existing_product[0][0]
    #             # ตรวจสอบว่าต้องการทำการบันทึกทับข้อมูลเดิมหรือไม่
    #             confirm_overwrite = messagebox.askyesno("ยืนยันการทับข้อมูล", "มีข้อมูลนี้อยู่แล้ว ต้องการทำการบันทึกทับข้อมูลเดิมหรือไม่?")
    #             if not confirm_overwrite:
    #                 return
    #         else:
    #             # หากไม่พบชื่อโปรไฟล์ ให้แสดง messagebox เตือน
    #             messagebox.showwarning("คำเตือน", "ไม่พบชื่อโปรไฟล์")
    #             return

    #         # บันทึกข้อมูลลงในตาราง breakeven_point
    #         query = "REPLACE INTO breakeven_point (product_id, fixed_cost, variable_cost, number_of_units, unit_price, product_efficiency) VALUES (%s, %s, %s, %s, %s, %s)"
    #         db.execute_query(query, (product_id, fixed_cost, variable_cost, number_of_units, price, efficiency))

    #         messagebox.showinfo("ความสำเร็จ", "บันทึกจุดคุ้มทุนสำเร็จ")
    #     except Exception as e:
    #         messagebox.showerror("ข้อผิดพลาด", f"เกิดข้อผิดพลาดในขณะที่พยายามทำการบันทึก: {str(e)}")

    def save_as(self):
        profile_name = self.breakpoint_view.label_add.cget("text")
        fixed_cost = self.breakpoint_view.entry_fixedcost.get()
        variable_cost = self.breakpoint_view.entry_variablecost.get()
        number_of_units = self.breakpoint_view.entry_number.get()
        price = self.breakpoint_view.entry_price.get()
        efficiency = self.breakpoint_view.entry_efficieny.get()

        # ตรวจสอบความสมบูรณ์ของข้อมูล
        if not all((profile_name, fixed_cost, variable_cost, number_of_units, price, efficiency)):
            messagebox.showwarning("คำเตือน", "กรุณากรอกข้อมูลให้ครบถ้วน")
            return

        try:
            db = DatabaseUtil.getInstance()

            # ค้นหา product_id จากชื่อโปรไฟล์
            existing_product = db.fetch_data("SELECT product_id FROM product WHERE product_name = %s", (profile_name,))
            if existing_product:
                product_id = existing_product[0][0]

                # ตรวจสอบว่ามีข้อมูลในตาราง breakeven_point อยู่แล้วหรือไม่
                existing_breakeven = db.fetch_data("SELECT * FROM breakeven_point WHERE product_id = %s", (product_id,))
                if existing_breakeven:
                    # ตรวจสอบว่าต้องการทำการบันทึกทับข้อมูลเดิมหรือไม่
                    confirm_overwrite = messagebox.askyesno("ยืนยันการทับข้อมูล", "มีข้อมูลนี้อยู่แล้ว ต้องการบันทึกทับข้อมูลเดิมหรือไม่?")
                    if not confirm_overwrite:
                        return

                    # อัปเดตข้อมูลในตาราง breakeven_point
                    query = "UPDATE breakeven_point SET fixed_cost = %s, variable_cost = %s, number_of_units = %s, unit_price = %s, product_efficiency = %s WHERE product_id = %s"
                    db.execute_query(query, (fixed_cost, variable_cost, number_of_units, price, efficiency, product_id))
                else:
                    # แทรกข้อมูลใหม่ลงในตาราง breakeven_point
                    query = "INSERT INTO breakeven_point (product_id, fixed_cost, variable_cost, number_of_units, unit_price, product_efficiency) VALUES (%s, %s, %s, %s, %s, %s)"
                    db.execute_query(query, (product_id, fixed_cost, variable_cost, number_of_units, price, efficiency))

                messagebox.showinfo("ความสำเร็จ", "บันทึกจุดคุ้มทุนสำเร็จ")
            else:
                # หากไม่พบชื่อโปรไฟล์ ให้แสดง messagebox เตือน
                messagebox.showwarning("คำเตือน", "ไม่พบชื่อโปรไฟล์")
        except Exception as e:
            messagebox.showerror("ข้อผิดพลาด", f"เกิดข้อผิดพลาดในขณะที่พยายามทำการบันทึก: {str(e)}")


