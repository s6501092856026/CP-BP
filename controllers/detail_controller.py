from views.detail_view import DetailView
from utils.window import getCenterPosition
#from utils.database import DatabaseUtil

class DetailController:
    width = 350
    height = 200

    def __init__(self, app):
        self.app = app
        self.detail_view = DetailView(self, app)

    def show_detail_view(self):
        self.detail_view.pack(padx=10, pady=10)
        x, y = getCenterPosition(self.app,width=self.width, height=self.height)
        self.app.geometry(f"{self.width}x{self.height}+{x}+{y}")
        self.detail_view.pack(padx=10, pady=10, expand=True)
    
    def accept(self):
        self.detail_view.pack_forget()
        self.app.show_newprofile()
    
    # def cancel(self):
        # self.detail_view.pack_forget()
        # self.app.show_newprofile()
    
    