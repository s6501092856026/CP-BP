from views.main_view import MainView
from views.compare_view import CompareView
from views.newprofile_view import NewprofileView
from utils.database import DatabaseUtil
from utils.window import getCenterPosition
class MainController:
    width = 975
    height = 450

    def __init__(self, app):
        self.app = app

        self.main_view = MainView(self, app)
        self.compare_view = CompareView(self, app)
        self.newprofile_view = NewprofileView(self, app)
        self.show_profile()
        self.show_detail()



    def show_main(self):
        self.main_view.pack(padx=10, pady=10)
        x, y = getCenterPosition(self.app,width=self.width, height=self.height)
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
        x, y = getCenterPosition(self.app,width=self.width, height=self.height)
        self.app.geometry(f"{self.width}x{self.height}+{x}+{y}")
        self.newprofile_view.pack(padx=10, pady=10)

    def show_compare(self):
        self.main_view.pack_forget()
        self.newprofile_view.pack_forget()
        x, y = getCenterPosition(self.app,width=self.width, height=self.height)
        self.app.geometry(f"{self.width}x{self.height}+{x}+{y}")
        self.compare_view.pack(padx=10, pady=10)

    def show_break(self):
        self.main_view.pack_forget()
        self.app.show_break()
    
    def show_profile(self):
        db = DatabaseUtil.getInstance()
        result = db.fetch_data("SELECT product_id, product_name FROM product")
        self.main_view.set_profile(result)

    def show_detail(self):
        db = DatabaseUtil.getInstance()
        rawmats = db.fetch_data("select name_raw from product p, product_rawmat pr, raw_mat r where p.product_id = pr.product_id and pr.rawmat_id = r.rawmat_id")
        transpots = db.fetch_data("select transpot_name from product p, product_transpotation pt, transpotation t where p.product_id = pt.product_id and pt.transpot_id = t.transpot_id")
        self.main_view.set_detail(rawmats, transpots)

        # p.product_id, r.rawmat_id,
        # p.product_id, pt.transpot_id,
    
    def show_profile_new(self):
        db = DatabaseUtil.getInstance()
        rawmats = db.fetch_data("SELECT rawmat_id, name_raw FROM raw_mat")
        transpots = db.fetch_data("SELECT transpot_id, transpot_name FROM transpotation")
        self.newprofile_view.set_profile_new(rawmats, transpots)