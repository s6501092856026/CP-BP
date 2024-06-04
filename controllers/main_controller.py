import tkinter as tk
from views.main_view import MainView
from views.compare_view import CompareView
from views.newprofile_view import NewprofileView
from utils.database import DatabaseUtil
from utils.window import getCenterPosition
class MainController:
    width = 1000
    height = 425

    def __init__(self, app):
        self.app = app

        self.main_view = MainView(self, app)
        self.compare_view = CompareView(self, app)
        self.newprofile_view = NewprofileView(self, app)
        self.show_profile()
        self.show_profile_name(1, '')

    def show_main(self):
        self.main_view.pack(padx=10, pady=10)
        x, y = getCenterPosition(self.app,width=self.width, height=550)
        self.app.geometry(f"{self.width}x{self.height}+{x}+{y}")
        self.main_view.pack(padx=10, pady=10)
    
    def back_main(self):
        self.compare_view.pack_forget()
        self.newprofile_view.pack_forget()
        x, y = getCenterPosition(self.app,width=self.width, height=self.height)
        self.app.geometry(f"{self.width}x{self.height}+{x}+{y}")
        self.main_view.pack(padx=10, pady=10)
    
    def show_newprofile(self):
        self.compare_view.pack_forget()
        self.main_view.pack_forget()
        x, y = getCenterPosition(self.app,width=1300, height=450)
        self.app.geometry(f"{1300}x{450}+{x}+{y}")

        # Clear the entry_name field
        self.newprofile_view.entry_name.delete(0, tk.END)

        self.newprofile_view.pack(padx=10, pady=10)

    def show_editprofile(self, product_id):
        self.compare_view.pack_forget()
        self.main_view.pack_forget()
        x, y = getCenterPosition(self.app,width=1300, height=450)
        self.app.geometry(f"{1300}x{450}+{x}+{y}")
        db = DatabaseUtil.getInstance()
        product = db.fetch_data("select product_name from product where product_id = " + product_id)
        rawmats = db.fetch_data("select 'Material', r.rawmat_id ,name_raw, amount, unit_raw from product p, product_rawmat pr, raw_mat r where p.product_id = pr.product_id and pr.rawmat_id = r.rawmat_id and p.product_id = " + product_id)
        transpots = db.fetch_data("select 'Transpotation', t.transpot_id, transpot_name, amount, unit_transpot from product p, product_transpotation pt, transpotation t where p.product_id = pt.product_id and pt.transpot_id = t.transpot_id and p.product_id = "+ product_id)
        performances = db.fetch_data("select 'Performance', f.performance_id, performance_name, amount, unit_performance from product p, product_performance pf, performance f where p.product_id = pf.product_id and pf.performance_id = f.performance_id and p.product_id = "+ product_id)
        
        # Clear the entry_name field
        self.newprofile_view.entry_name.delete(0, tk.END)

        self.newprofile_view.set_select(product, rawmats, transpots, performances)
        self.newprofile_view.pack(padx=10, pady=10)

    def show_compare(self):
        self.main_view.pack_forget()
        self.newprofile_view.pack_forget()
        x, y = getCenterPosition(self.app,width=1050, height=450)
        self.app.geometry(f"{1050}x{450}+{x}+{y}")
        self.compare_view.pack(padx=10, pady=10)

    def show_break(self):
        self.main_view.pack_forget()
        self.newprofile_view.pack_forget()
        self.compare_view.pack_forget()
        self.app.show_break()

    def show_connew(self, items):
        self.main_view.pack_forget()
        self.newprofile_view.pack_forget()
        self.compare_view.pack_forget()
        self.app.show_connew(items)
    
    def show_conprepare(self):
        self.main_view.pack_forget()
        self.newprofile_view.pack_forget()
        self.compare_view.pack_forget()
        self.app.show_conprepare()

    def delete_profile(self, product_id):
        print(product_id)
        db = DatabaseUtil.getInstance()
        params = (product_id,)
        delete = db.execute_query("DELETE FROM product WHERE product_id = %s", params)

    def show_profile(self):
        db = DatabaseUtil.getInstance()
        result = db.fetch_data("SELECT product_id, product_name FROM product")
        self.main_view.set_profile(result)
        self.compare_view.set_profile(result)

    def show_detail(self, product_id):
        db = DatabaseUtil.getInstance()
        rawmats = db.fetch_data("select name_raw, amount, unit_raw from product p, product_rawmat pr, raw_mat r where p.product_id = pr.product_id and pr.rawmat_id = r.rawmat_id and p.product_id = " + product_id)
        transpots = db.fetch_data("select transpot_name, amount, unit_transpot from product p, product_transpotation pt, transpotation t where p.product_id = pt.product_id and pt.transpot_id = t.transpot_id and p.product_id = "+ product_id)
        performances = db.fetch_data("select performance_name, amount, unit_performance from product p, product_performance pf, performance f where p.product_id = pf.product_id and pf.performance_id = f.performance_id and p.product_id = "+ product_id)
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
                performances = db.fetch_data("SELECT performance_id, performance_name FROM performance")
            type_performances = db.fetch_data("SELECT distinct(type_performance) FROM performance")
        
        self.newprofile_view.set_profile_name(rawmats, type_rawmats, transpots, performances, type_performances)