from views.breakpoint_view import BreakpointView
from utils.window import getCenterPosition
from utils.database import DatabaseUtil

class BreakController:
    width = 550
    height = 350

    def __init__(self, app):
        self.app = app
        self.breakpoint_view = BreakpointView(self, app)

    def show_break(self, profile_name):
        self.breakpoint_view.pack(padx=10, pady=10)
        x, y = getCenterPosition(self.app,width=self.width, height=self.height)
        self.app.geometry(f"{self.width}x{self.height}+{x}+{y}")
        # self.breakpoint_view.set_selected_profile(profile_name)
        self.breakpoint_view.pack(padx=10, pady=10, expand=True)
    
    def back_main(self):
        self.breakpoint_view.pack_forget()
        self.app.show_main()
    
    # def show_nameprofile(self):
        # db = DatabaseUtil.getInstance()
        # result = db.fetch_data("SELECT product_name FROM product")
        # self.breakpoint_view.set_nameprofile(result)