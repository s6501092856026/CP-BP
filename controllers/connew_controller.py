from views.connew_view import ConnewView
from utils.database import DatabaseUtil
from utils.window import getCenterPosition
class ConnewController:
    width = 1450
    height = 700

    def __init__(self, app):
        self.app = app
        self.connew_view = ConnewView(self, app)

    def show_connew(self, items):
        self.connew_view.pack_forget()
        self.connew_view.setConclusion(items)
        self.connew_view.pack(padx=10, pady=10)
        self.app.update_idletasks()
        widget_width = self.connew_view.winfo_reqwidth() + 20  # เพิ่ม padding
        widget_height = self.connew_view.winfo_reqheight() + 20  # เพิ่ม padding
        x, y = getCenterPosition(self.app, width=widget_width, height=widget_height)
        self.app.geometry(f"{widget_width}x{widget_height}+{x}+{y}")


    # def show_connew(self, items):
    #     self.connew_view.pack_forget()
    #     x, y = getCenterPosition(self.app,width=self.width, height=self.height)
    #     self.app.geometry(f"{self.width}x{self.height}+{x}+{y}")
    #     self.connew_view.pack(padx=10, pady=10)
    #     self.connew_view.setConclusion(items)
    
    def back_main(self):
        self.connew_view.pack_forget()
        self.app.show_main()