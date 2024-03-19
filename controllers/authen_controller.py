import tkinter as tk
from views.signup_view import SignupView
from views.login_view import LoginView
from utils.window import getCenterPosition
from utils.validator import isRequired, isValidEmail
from utils.database import DatabaseUtil
class AuthenController:
    width = 350
    height = 400

    def __init__(self, app):
        self.app = app

        self.login_view = LoginView(self, app)
        self.signup_view = SignupView(self, app)
    
    def authen(self, username, password):
        if(isRequired(username) and isRequired(password)):
            db = DatabaseUtil.getInstance()
            result = db.fetch_data(
                "SELECT * FROM users WHERE username = %s AND password = %s",
                (username, password)
            )
            for row in result:
                if(row[5] == username and row[6] == password):
                    self.app.user = row
                    self.login_view.hide_error()
                    self.login_view.pack_forget()
                    self.app.show_main()
                
            self.login_view.show_error()
        else:
            self.login_view.show_error()

    def signup(self, firstname, lastname, username, email, password, tel):
        # Validate
        if(isRequired(firstname) and isRequired(lastname) and isRequired(username) and isRequired(tel) and isValidEmail(email) and isRequired(password)):
            db = DatabaseUtil.getInstance()
            params = (firstname, lastname, username, tel, email, password)
            result = db.execute_query("INSERT INTO users (firstname, lastname, username, tel, email, password) VALUES (%s, %s, %s, %s, %s, %s)", params)

            if(result > 0):
                self.signup_view.show_massagebox( "Insert user data successfully.")
                self.signup_view.clear_entries()
            else: 
                self.signup_view.show_massagebox( "Insert user data error.")
        else:
            self.signup_view.show_error("Invalid data.")

    def show_login(self):
        self.signup_view.pack_forget()
        x, y = getCenterPosition(self.app,width=self.width + 50, height=self.height + 100)
        self.app.geometry(f"{self.width + 50}x{self.height + 100}+{x}+{y}")

        self.login_view.pack(padx=10, pady=10, expand=True)
    
    def show_signup(self):
        self.login_view.pack_forget()
        x, y = getCenterPosition(self.app,width=self.width, height=self.height)
        self.app.geometry(f"{self.width}x{self.height}+{x}+{y}")
        
        self.signup_view.pack(padx=10, pady=10, expand=True)
    
    