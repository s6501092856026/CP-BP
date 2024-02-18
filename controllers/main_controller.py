from views.main_view import MainView
from views.compare_view import CompareView
from views.newprofile_view import NewprofileView
#from utils.database import DatabaseUtil
from utils.window import getCenterPosition
class MainController:
    width = 975
    height = 450

    def __init__(self, app):
        self.app = app

        self.main_view = MainView(self, app)
        self.compare_view = CompareView(self, app)
        self.newprofile_view = NewprofileView(self, app)
    
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
        self.app.show_break()
    
    