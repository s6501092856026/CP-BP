from tkinter import ttk

class LoginView(ttk.Frame):

    def __init__(self, controller, app):
        super().__init__(app)
        self.controller = controller

        self.label_email = ttk.Label(self, text = "Username", foreground="black", font=("Times New Roman", 10, "bold"))
        self.label_email.grid(row=0, column=0, pady=(20, 0))

        self.label_password = ttk.Label(self, text = "Password", foreground="black", font=("Times New Roman", 10, "bold"))
        self.label_password.grid(row=2, column=0, padx=10, pady=10)

        self.warning_msg = ttk.Label(self, text = "",foreground="red")
        self.warning_msg.grid(row=4, padx=10, pady=10)

        self.entry_email = ttk.Entry(self, width=30, justify= "center")
        self.entry_email.grid(row=1, column=0, padx=10, pady=10)
        self.entry_email.insert(0, "admin")

        self.entry_password = ttk.Entry(self, width=30, show="*", justify= "center")
        self.entry_password.grid(row=3, column=0, padx=10, pady=10)
        self.entry_password.insert(0, "Daoruang07")

        self.button_login = ttk.Button(self, text="Login", command=self.login)
        self.button_login.grid(row=5, column=0, padx=10, pady=10)

        self.button_signup = ttk.Button(self, text="Signup", command=self.controller.show_signup)
        self.button_signup.grid(row=6, column=0, padx=10, pady=10)
    
    def login(self):
        self.controller.authen(self.entry_email.get(), self.entry_password.get())

    def show_error(self):
        self.warning_msg.configure(text="Invalid Username/Password")

    def hide_error(self):
        self.warning_msg.configure(text="")
    
    