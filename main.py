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
        # self.style.theme_use('clam')  # Use a modern theme

        # Customize styles for a white background and light yellow widgets
        white = '#ffffff'
        light_green = '#ccffcc'
        dark_green = '#99ff99'
        # light_yellow = '#ffffcc'
        # dark_yellow = '#ffff99'
        entry_bg = '#ffffe6'
        
        self.configure(bg=white)

        self.style.configure('TButton', font=('Arial', 9), padding=10, background=light_green)
        self.style.map('TButton', background=[('active', dark_green)])
        self.style.configure('TLabel', font=('Arial', 9), background=white)
        self.style.configure('TEntry', font=('Arial', 9), fieldbackground=entry_bg)
        self.style.configure('TFrame', background=white)

        self.show_login()

    def show_login(self):
        self.controller = AuthenController(self)
        self.controller.show_login()

    def show_main(self):
        self.controller = MainController(self)
        self.controller.show_main()
    
    def show_break(self):
        self.controller = BreakController(self)
        self.controller.show_break()

    def show_connew(self, items):
        self.controller = ConnewController(self)
        self.controller.show_connew(items)
    
    def show_conprepare(self):
        self.controller = ConprepareController(self)
        self.controller.show_conprepare()

if __name__ == "__main__":
    app=App()
    app.mainloop()