from views.connew_view import ConnewView
from utils.database import DatabaseUtil
from utils.window import getCenterPosition
class ConnewController:
    width = 1000
    height = 625

    def __init__(self, app):
        self.app = app

        self.connew_view = ConnewView(self, app)

    def show_connew(self, items):
        self.connew_view.pack_forget()
        x, y = getCenterPosition(self.app,width=self.width, height=self.height)
        self.app.geometry(f"{self.width}x{self.height}+{x}+{y}")
        self.connew_view.pack(padx=10, pady=10)
        self.connew_view.setConclusion(items)
    
    def back_main(self):
        self.connew_view.pack_forget()
        self.app.show_main()