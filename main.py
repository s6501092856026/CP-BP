import tkinter as tk
from tkinter import ttk
from controllers.authen_controller import AuthenController
from controllers.main_controller import MainController
from controllers.breakeven_controller import BreakController
from controllers.connew_controller import ConnewController
from controllers.conprepare_controller import ConprepareController

class App(tk.Tk):

    def __init__(self):
        super().__init__()
        self.controller = None
        self.title("CF&BP")
        self.iconbitmap('icon.ico')

        self.resizable(width=False ,height=False)

        self.style = ttk.Style(self)

        # Customize styles for a white background and light yellow widgets
        white = '#ffffff'
        light_green = '#ccffcc'
        dark_green = '#006400'
        entry_bg = '#ffffe6'
        
        self.configure(bg=white)

        self.style.configure('TButton', font=('Tohama', 10), borderwidth=2, padding=5, background=dark_green)
        self.style.map('TButton', background=[('active', light_green)])
        self.style.configure('TLabel', font=('Tohama', 10, 'bold'), background=white)
        self.style.configure('TEntry', font=('Tohama', 10), fieldbackground=entry_bg, borderwidth=2)
        self.style.configure('TFrame', background=white)
        self.style.configure("Treeview.Heading", font=('Tohama', 8, 'bold'))
        self.style.configure("Treeview.Heading", font=("Tohama", 9, "bold"), background="lightblue")
        self.style.configure("Treeview", font=("Tohama", 9), rowheight=25)
        self.style.map("Treeview", background=[("selected", "green")], foreground=[("selected", "white")])

        self.show_login()

    def show_login(self):
        self.controller = AuthenController(self)
        self.controller.show_login()

    def show_main(self):
        self.controller = MainController(self)
        self.controller.show_main()
    
    def show_break(self, profile_name):
        self.controller = BreakController(self)
        self.controller.show_break(profile_name)

    def show_connew(self, profile_name, items, breakpoint_data):
        self.controller = ConnewController(self)
        self.controller.show_connew(profile_name, items, breakpoint_data)
    
    def show_conprepare(self, profile1, profile2, raw_data_1, trans_data_1,
                         perf_data_1, raw_data_2, trans_data_2, perf_data_2, breakpoint_data1, breakpoint_data2):
        self.controller = ConprepareController(self)
        self.controller.show_conprepare(profile1, profile2, raw_data_1, trans_data_1,
                                         perf_data_1, raw_data_2, trans_data_2, perf_data_2, breakpoint_data1, breakpoint_data2)

if __name__ == "__main__":
    app=App()
    app.mainloop()