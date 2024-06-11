from tkinter import messagebox
from views.conprepare_view import ConprepareView
from utils.database import DatabaseUtil
from utils.window import getCenterPosition

class ConprepareController:
    
    def __init__(self, app):
        self.app = app

        self.conprepare_view = ConprepareView(self, app)
    
    def show_conprepare(self, profile1, profile2, raw_data_1, trans_data_1,
                         perf_data_1, raw_data_2, trans_data_2, perf_data_2, breakpoint_data1, breakpoint_data2):
        self.conprepare_view.pack_forget()
        self.conprepare_view.show_profile(profile1, profile2, raw_data_1, trans_data_1,
                                           perf_data_1, raw_data_2, trans_data_2, perf_data_2, breakpoint_data1, breakpoint_data2)
        self.conprepare_view.pack(padx=10, pady=10, fill="both", expand=True)
        self.app.update_idletasks()
        widget_width = self.conprepare_view.winfo_reqwidth() + 20  # เพิ่ม padding
        widget_height = self.conprepare_view.winfo_reqheight() + 20  # เพิ่ม padding
        x, y = getCenterPosition(self.app, width=widget_width, height=widget_height)
        self.app.geometry(f"{widget_width}x{widget_height}+{x}+{y}")

    def back_main(self):
        self.conprepare_view.pack_forget()
        self.app.show_main()
