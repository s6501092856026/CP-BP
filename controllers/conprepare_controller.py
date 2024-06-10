from tkinter import messagebox
from views.conprepare_view import ConprepareView
from utils.database import DatabaseUtil
from utils.window import getCenterPosition

class ConprepareController:
    width = 1000
    height = 625

    def __init__(self, app):
        self.app = app

        self.conprepare_view = ConprepareView(self, app)
    
    def show_conprepare(self, profile1, profile2, raw_data_1, trans_data_1, perf_data_1, raw_data_2, trans_data_2, perf_data_2):
        self.conprepare_view.pack_forget()
        self.conprepare_view.show_profile(profile1, profile2, raw_data_1, trans_data_1, perf_data_1, raw_data_2, trans_data_2, perf_data_2)
        self.conprepare_view.pack(padx=10, pady=10, fill="both", expand=True)
        self.app.update_idletasks()
        widget_width = self.conprepare_view.winfo_reqwidth() + 20  # เพิ่ม padding
        widget_height = self.conprepare_view.winfo_reqheight() + 20  # เพิ่ม padding
        x, y = getCenterPosition(self.app, width=widget_width, height=widget_height)
        self.app.geometry(f"{widget_width}x{widget_height}+{x}+{y}")


    # def show_conprepare(self, profile1, profile2):

    #     self.conprepare_view.pack_forget()
    #     self.conprepare_view.show_profile(profile1, profile2)
    #     # แสดง ConprepareView และปรับขนาดหน้าต่าง
    #     self.conprepare_view.pack(padx=10, pady=10, fill="both", expand=True)
    #     self.app.update_idletasks()
    #     widget_width = self.conprepare_view.winfo_reqwidth() + 20  # เพิ่ม padding
    #     widget_height = self.conprepare_view.winfo_reqheight() + 20  # เพิ่ม padding
    #     x, y = getCenterPosition(self.app, width=widget_width, height=widget_height)
    #     self.app.geometry(f"{widget_width}x{widget_height}+{x}+{y}")

    def back_main(self):
        self.conprepare_view.pack_forget()
        self.app.show_main()

    # def show_treeview(self, product_name):
    #     db = DatabaseUtil.getInstance()
    #     existing_product = db.fetch_data("SELECT product_id FROM product WHERE product_name = %s", (product_name,))
    
    #     # ตรวจสอบว่ามีผลิตภัณฑ์ที่ตรงกับชื่อหรือไม่
    #     if existing_product:
    #         product_id = existing_product[0][0]
        
    #         # ดึงข้อมูล raw materials ที่เกี่ยวข้องกับผลิตภัณฑ์
    #         rawmats = db.fetch_data("SELECT name_raw, carbon_per_raw, amount, unit_raw FROM product p, product_rawmat pr, raw_mat r WHERE p.product_id = pr.product_id AND pr.rawmat_id = r.rawmat_id AND p.product_id = "+ product_id)
        
    #         # ดึงข้อมูล transportation ที่เกี่ยวข้องกับผลิตภัณฑ์
    #         transpots = db.fetch_data("SELECT transpot_name, carbon_per_transpot, amount, unit_transpot FROM product p, product_transpotation pt, transpotation t WHERE p.product_id = pt.product_id AND pt.transpot_id = t.transpot_id AND p.product_id = "+ product_id)
        
    #         # ดึงข้อมูล performances ที่เกี่ยวข้องกับผลิตภัณฑ์
    #         performances = db.fetch_data("SELECT performance_name, carbon_per_performance, amount, unit_performance FROM product p, product_performance pf, performance f WHERE p.product_id = pf.product_id AND pf.performance_id = f.performance_id AND p.product_id = "+ product_id)
        
    #         # อัปเดต view ด้วยข้อมูลที่ดึงมา
    #         self.conprepare_view.show_profile(rawmats, transpots, performances)
