from views.main_view import MainView
from views.compare_view import CompareView
from views.newprofile_view import NewprofileView
from utils.database import DatabaseUtil
from utils.window import getCenterPosition
class MainController:
    width = 800
    height = 425

    def __init__(self, app):
        self.app = app

        self.main_view = MainView(self, app)
        self.compare_view = CompareView(self, app)
        self.newprofile_view = NewprofileView(self, app)
        self.show_profile()
        # self.show_detail()
        self.show_profile_name(1, '')

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
        x, y = getCenterPosition(self.app,width=1260, height=450)
        self.app.geometry(f"{1260}x{450}+{x}+{y}")
        self.newprofile_view.pack(padx=10, pady=10)

    def show_compare(self):
        self.main_view.pack_forget()
        self.newprofile_view.pack_forget()
        x, y = getCenterPosition(self.app,width=815, height=450)
        self.app.geometry(f"{815}x{450}+{x}+{y}")
        self.compare_view.pack(padx=10, pady=10)

    def show_break(self):
        self.main_view.pack_forget()
        self.newprofile_view.pack_forget()
        self.compare_view.pack_forget()
        self.app.show_break()

    def show_connew(self):
        self.main_view.pack_forget()
        self.newprofile_view.pack_forget()
        self.compare_view.pack_forget()
        self.app.show_connew()
    
    def show_conprepare(self):
        self.main_view.pack_forget()
        self.newprofile_view.pack_forget()
        self.compare_view.pack_forget()
        self.app.show_conprepare()

    def show_detail_view(self):
        self.newprofile_view.pack_forget()
        self.app.show_detail_view()

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
        rawmats = db.fetch_data("select name_raw from product p, product_rawmat pr, raw_mat r where p.product_id = pr.product_id and pr.rawmat_id = r.rawmat_id and p.product_id = " + product_id)
        transpots = db.fetch_data("select transpot_name from product p, product_transpotation pt, transpotation t where p.product_id = pt.product_id and pt.transpot_id = t.transpot_id and p.product_id = "+ product_id)
        self.main_view.set_detail(rawmats, transpots)
        self.compare_view.set_detail(rawmats, transpots)
    
    def show_profile_name(self, filter_cate, filter_type):
        db = DatabaseUtil.getInstance()
        rawmats = []
        type_rawmats = []
        transpots = []
        performances = []
        type_performances = []
        if filter_cate == 1:
            if filter_type != '' :
                rawmats = db.fetch_data("SELECT rawmat_id, name_raw FROM raw_mat where type_raw = '" + filter_type +"'")
            else: 
                rawmats = db.fetch_data("SELECT rawmat_id, name_raw FROM raw_mat")

            type_rawmats = db.fetch_data("SELECT distinct(type_raw) FROM raw_mat")
        elif filter_cate == 2:
            transpots = db.fetch_data("SELECT transpot_id, transpot_name FROM transpotation")
        elif filter_cate == 3:
            if filter_type  != '':
                performances = db.fetch_data("SELECT performance_id, performance_name FROM performance where type_performance = '" +  filter_type +"'")
            else:
                performances = db.fetch_data("SELECT performance_id, performance_name FROM performance")
            type_performances = db.fetch_data("SELECT distinct(type_performance) FROM performance")
        
        self.newprofile_view.set_profile_name(rawmats, type_rawmats, transpots, performances, type_performances)