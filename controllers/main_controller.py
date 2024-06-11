import tkinter as tk
from tkinter import messagebox
from views.main_view import MainView
from views.compare_view import CompareView
from views.newprofile_view import NewprofileView
from utils.database import DatabaseUtil
from utils.window import getCenterPosition

class MainController:

    def __init__(self, app):
        self.app = app

        self.main_view = MainView(self, app)
        self.compare_view = CompareView(self, app)
        self.newprofile_view = NewprofileView(self, app)

        self.show_profile()
        self.show_profile_name(1, '')

    def show_main(self):
        self.main_view.pack(padx=10, pady=10, fill="both", expand=True)
        self.app.update_idletasks()  # อัพเดตวิดเจ็ต
        width = self.main_view.winfo_reqwidth() + 20  # เพิ่มขอบเขตบางส่วน
        height = self.main_view.winfo_reqheight() + 20  # เพิ่มขอบเขตบางส่วน
        x, y = getCenterPosition(self.app, width=width, height=height)
        self.app.geometry(f"{width}x{height}+{x}+{y}")

    def back_main(self):
        self.compare_view.pack_forget()
        self.newprofile_view.pack_forget()
        self.main_view.pack_forget()  # ลบการแพ็คของวิดเจต์ main_view เพื่อลบออกจากหน้าต่าง
        self.main_view.pack(padx=10, pady=10, fill="both", expand=True)  # แพ็ควิดเจต์ main_view ใหม่ พร้อมกับ Padding
        self.app.update_idletasks()  # อัพเดตวิดเจต์
        width = self.main_view.winfo_reqwidth() + 20 # เพิ่มขอบเขตบางส่วน
        height = self.main_view.winfo_reqheight() + 20 # เพิ่มขอบเขตบางส่วน
        x, y = getCenterPosition(self.app, width=width, height=height)
        self.app.geometry(f"{width}x{height}+{x}+{y}")
 
    def show_newprofile(self):
        self.compare_view.pack_forget()
        self.main_view.pack_forget()
        self.newprofile_view.pack_forget()  # ลบการแพ็คของวิดเจต์ newprofile_view เพื่อลบออกจากหน้าต่าง
        self.newprofile_view.pack(padx=10, pady=10, fill="both", expand=True)  # แพ็ควิดเจต์ newprofile_view ใหม่ พร้อมกับ Padding
        self.app.update_idletasks()  # อัพเดตวิดเจต์
        width = self.newprofile_view.winfo_reqwidth() + 20  # เพิ่มขอบเขตบางส่วน
        height = self.newprofile_view.winfo_reqheight() + 20  # เพิ่มขอบเขตบางส่วน
        x, y = getCenterPosition(self.app, width=width, height=height)
        self.app.geometry(f"{width}x{height}+{x}+{y}")

        # ล้างข้อมูลในช่องข้อมูลทั้งหมด
        self.newprofile_view.entry_amount.delete(0, tk.END)
        self.newprofile_view.entry_name.delete(0, tk.END)

    def show_editprofile(self, product_id):
        self.compare_view.pack_forget()
        self.main_view.pack_forget()

        db = DatabaseUtil.getInstance()
        product = db.fetch_data("select product_name from product where product_id = " + product_id)
        rawmats = db.fetch_data("select 'Material', r.rawmat_id ,name_raw, carbon_per_raw, amount, unit_raw from product p, product_rawmat pr, raw_mat r where p.product_id = pr.product_id and pr.rawmat_id = r.rawmat_id and p.product_id = " + product_id)
        transpots = db.fetch_data("select 'Transpotation', t.transpot_id, transpot_name, carbon_per_transpot, amount, unit_transpot from product p, product_transpotation pt, transpotation t where p.product_id = pt.product_id and pt.transpot_id = t.transpot_id and p.product_id = "+ product_id)
        performances = db.fetch_data("select 'Performance', f.performance_id, performance_name, carbon_per_performance, amount, unit_performance from product p, product_performance pf, performance f where p.product_id = pf.product_id and pf.performance_id = f.performance_id and p.product_id = "+ product_id)
        
        self.newprofile_view.pack_forget()  # ลบการแพ็คของวิดเจต์ newprofile_view เพื่อลบออกจากหน้าต่าง
        self.newprofile_view.pack(padx=10, pady=10, fill="both", expand=True)  # แพ็ควิดเจต์ newprofile_view ใหม่ พร้อมกับ Padding
        self.app.update_idletasks()  # อัพเดตวิดเจต์
        width = self.newprofile_view.winfo_reqwidth() + 20  # เพิ่มขอบเขตบางส่วน
        height = self.newprofile_view.winfo_reqheight() + 20  # เพิ่มขอบเขตบางส่วน
        x, y = getCenterPosition(self.app, width=width, height=height)
        self.app.geometry(f"{width}x{height}+{x}+{y}")

        # ล้างข้อมูลที่อยู่ในช่องข้อมูลทั้งหมด
        self.newprofile_view.entry_amount.delete(0, tk.END)
        self.newprofile_view.entry_name.delete(0, tk.END)
        
        self.newprofile_view.set_select(product, rawmats, transpots, performances)

    def show_compare(self):
        self.main_view.pack_forget()
        self.newprofile_view.pack_forget()
        self.compare_view.pack_forget()  # ลบการแพ็ควิดเจต์ compare_view เพื่อลบออกจากหน้าต่าง
        self.compare_view.pack(padx=10, pady=10, fill="both", expand=True)  # แพ็ควิดเจต์ compare_view ใหม่ พร้อมกับ Padding
        self.app.update_idletasks()  # อัพเดตวิดเจต์
        width = self.compare_view.winfo_reqwidth() + 20  # เพิ่มขอบเขตบางส่วน
        height = self.compare_view.winfo_reqheight() + 20  # เพิ่มขอบเขตบางส่วน
        x, y = getCenterPosition(self.app, width=width, height=height)
        self.app.geometry(f"{width}x{height}+{x}+{y}")

    def show_break(self, profile_name):
        self.main_view.pack_forget()
        self.newprofile_view.pack_forget()
        self.compare_view.pack_forget()
        self.app.show_break(profile_name)

    def show_connew(self, profile_name, items, breakpoint_data):
        self.main_view.pack_forget()
        self.newprofile_view.pack_forget()
        self.compare_view.pack_forget()
        self.app.show_connew(profile_name, items, breakpoint_data)
    
    def show_conprepare(self, profile1, profile2, raw_data_1, trans_data_1,
                         perf_data_1, raw_data_2, trans_data_2, perf_data_2, breakpoint_data1, breakpoint_data2):
        self.main_view.pack_forget()
        self.newprofile_view.pack_forget()
        self.compare_view.pack_forget()
        self.app.show_conprepare(profile1, profile2, raw_data_1,
                                  trans_data_1, perf_data_1, raw_data_2, trans_data_2, perf_data_2, breakpoint_data1, breakpoint_data2)

    def delete_profile(self, product_id):
        db = DatabaseUtil.getInstance()

        # ลบข้อมูลที่เกี่ยวข้องในตาราง product_rawmat, product_transpotation, product_performance และ breakeven_point
        db.execute_query("DELETE FROM product_rawmat WHERE product_id = %s", (product_id,))
        db.execute_query("DELETE FROM product_transpotation WHERE product_id = %s", (product_id,))
        db.execute_query("DELETE FROM product_performance WHERE product_id = %s", (product_id,))
        db.execute_query("DELETE FROM breakeven_point WHERE product_id = %s", (product_id,))

        # ลบโปรไฟล์เอง
        db.execute_query("DELETE FROM product WHERE product_id = %s", (product_id,))

        # อัพเดตการแสดงผลโปรไฟล์หลังการลบ
        self.show_profile()
        messagebox.showinfo("ความสำเร็จ", "ลบโปรไฟล์สำเร็จแล้ว")

    def show_profile(self):
        db = DatabaseUtil.getInstance()
        result = db.fetch_data("SELECT product_id, product_name FROM product")
        self.main_view.set_profile(result)
        self.compare_view.set_profile(result)

    def show_detail(self, product_id):
        db = DatabaseUtil.getInstance()
        rawmats = db.fetch_data("select name_raw, carbon_per_raw, amount, unit_raw from product p, product_rawmat pr, raw_mat r where p.product_id = pr.product_id and pr.rawmat_id = r.rawmat_id and p.product_id = "+ product_id)
        transpots = db.fetch_data("select transpot_name, carbon_per_transpot, amount, unit_transpot from product p, product_transpotation pt, transpotation t where p.product_id = pt.product_id and pt.transpot_id = t.transpot_id and p.product_id = "+ product_id)
        performances = db.fetch_data("select performance_name, carbon_per_performance, amount, unit_performance from product p, product_performance pf, performance f where p.product_id = pf.product_id and pf.performance_id = f.performance_id and p.product_id = "+ product_id)
        self.main_view.set_detail(rawmats, transpots, performances)
        self.compare_view.set_detail(rawmats, transpots, performances)
    
    def show_profile_name(self, filter_cate, filter_type):
        db = DatabaseUtil.getInstance()
        rawmats = []
        type_rawmats = []
        transpots = []
        performances = []
        type_performances = []
        if filter_cate == 1:
            if filter_type != '' :
                rawmats = db.fetch_data("SELECT rawmat_id, name_raw, carbon_per_raw, unit_raw FROM raw_mat where type_raw = '" + filter_type +"'")
            else: 
                rawmats = db.fetch_data("SELECT rawmat_id, name_raw, carbon_per_raw, unit_raw FROM raw_mat")

            type_rawmats = db.fetch_data("SELECT distinct(type_raw) FROM raw_mat")
        elif filter_cate == 2:
            transpots = db.fetch_data("SELECT transpot_id, transpot_name, carbon_per_transpot, unit_transpot FROM transpotation")
        elif filter_cate == 3:
            if filter_type  != '':
                performances = db.fetch_data("SELECT performance_id, performance_name, carbon_per_performance, unit_performance FROM performance where type_performance = '" +  filter_type +"'")
            else:
                performances = db.fetch_data("SELECT performance_id, performance_name, carbon_per_performance, unit_performance FROM performance")
            type_performances = db.fetch_data("SELECT distinct(type_performance) FROM performance")
        
        self.newprofile_view.set_profile_name(rawmats, type_rawmats, transpots, performances, type_performances)

    def save_as_profile(self, profile_name, items):
        if not profile_name:
            messagebox.showwarning("คำเตือน", "กรุณาใส่ชื่อในช่องข้อมูลชื่อโปรไฟล์")
            return

        db = DatabaseUtil.getInstance()

        # Check if the product_name already exists
        existing_product = db.fetch_data("SELECT product_id FROM product WHERE product_name = %s", (profile_name,))
        if existing_product:
            product_id = existing_product[0][0]
            overwrite = messagebox.askyesno("บันทึกทับ", "ชื่อโปรไฟล์มีอยู่แล้ว คุณต้องการบันทึกทับหรือไม่?")
            if overwrite:
                # Delete existing records
                db.execute_query("DELETE FROM product_rawmat WHERE product_id = %s", (product_id,))
                db.execute_query("DELETE FROM product_transpotation WHERE product_id = %s", (product_id,))
                db.execute_query("DELETE FROM product_performance WHERE product_id = %s", (product_id,))

                # Update the product name (if necessary, this step can be skipped if only associated data is updated)
                db.execute_query("UPDATE product SET product_name = %s WHERE product_id = %s", (profile_name, product_id))
            else:
                return
        else:
            # Get the last inserted product_id and increment it by 1
            last_product_id = db.fetch_data("SELECT MAX(product_id) FROM product")[0][0]
            if last_product_id is None:
                new_product_id = 1
            else:
                new_product_id = last_product_id + 1

            # Insert the new profile into the product table with the new product_id
            insert_product_query = "INSERT INTO product (product_id, product_name) VALUES (%s, %s)"
            db.execute_query(insert_product_query, (new_product_id, profile_name))
            product_id = new_product_id

        # Insert the related materials, transportations, and performances
        for item in items:
            item_type, item_id, _, _, amount, _ = item

            if item_type == 'Material':
                insert_rawmat_query = "INSERT INTO product_rawmat (product_id, rawmat_id, amount) VALUES (%s, %s, %s)"
                db.execute_query(insert_rawmat_query, (product_id, item_id, amount))
            elif item_type == 'Transpotation':
                insert_transpot_query = "INSERT INTO product_transpotation (product_id, transpot_id, amount) VALUES (%s, %s, %s)"
                db.execute_query(insert_transpot_query, (product_id, item_id, amount))
            elif item_type == 'Performance':
                insert_performance_query = "INSERT INTO product_performance (product_id, performance_id, amount) VALUES (%s, %s, %s)"
                db.execute_query(insert_performance_query, (product_id, item_id, amount))

        messagebox.showinfo("ความสำเร็จ", "บันทึกโปรไฟล์สำเร็จ")

        # รีเฟรชการแสดงผลโปรไฟล์ใน main_view
        self.show_profile()