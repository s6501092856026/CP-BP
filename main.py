import tkinter as tk
from controllers.authen_controller import AuthenController
from controllers.main_controller import MainController
from controllers.breakeven_controller import BreakController

class App(tk.Tk):

    def __init__(self):
        super().__init__()
        self.controller = None
        self.title("CF&BP")
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

if __name__ == "__main__":
    app=App()
    app.mainloop()