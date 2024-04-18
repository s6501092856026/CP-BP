from views.conprepare_view import ConprepareView
from utils.database import DatabaseUtil
from utils.window import getCenterPosition
class ConprepareController:
    width = 1000
    height = 625

    def __init__(self, app):
        self.app = app

        self.conprepare_view = ConprepareView(self, app)

    def show_conprepare(self):
        self.conprepare_view.pack_forget()
        x, y = getCenterPosition(self.app,width=self.width, height=self.height)
        self.app.geometry(f"{self.width}x{self.height}+{x}+{y}")
        self.conprepare_view.pack(padx=10, pady=10)

    def back_main(self):
        self.conprepare_view.pack_forget()
        self.app.show_main()