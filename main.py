import tkinter as tk
from controllers.authen_controller import AuthenController
from controllers.main_controller import MainController
from controllers.breakeven_controller import BreakController
from controllers.connew_controller import ConnewController
from controllers.conprepare_controller import ConprepareController
from ttkthemes import ThemedStyle

class App(tk.Tk):

    def __init__(self):
        super().__init__()
        self.controller = None
        self.title("CF&BP")
        self.iconbitmap('icon.ico')
        
        # self.resizable(width=False ,height=False)

        self.style = ThemedStyle(self)
        self.style.set_theme("plastik") # ("adapta") ("radiance") ("scidblue") ("plastik") ("breeze")

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