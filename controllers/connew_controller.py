from views.connew_view import ConnewView
from utils.window import getCenterPosition

class ConnewController:

    def __init__(self, app):
        self.app = app
        self.connew_view = ConnewView(self, app)

    def show_connew(self, profile_name, items, breakpoint_data):
        self.connew_view.pack_forget()
        self.connew_view.setConclusion(profile_name, items, breakpoint_data)
        self.connew_view.pack(padx=10, pady=10, fill="both", expand=True)
        self.app.update_idletasks()
        widget_width = self.connew_view.winfo_reqwidth() + 20  # เพิ่ม padding
        widget_height = self.connew_view.winfo_reqheight() + 20  # เพิ่ม padding
        x, y = getCenterPosition(self.app, width=widget_width, height=widget_height)
        self.app.geometry(f"{widget_width}x{widget_height}+{x}+{y}")
    
    def back_main(self):
        self.connew_view.pack_forget()
        self.app.show_main()