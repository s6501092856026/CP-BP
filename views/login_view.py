import tkinter as tk
from tkinter import ttk # , PhotoImage, Canvas
from PIL import Image, ImageTk

class LoginView(ttk.Frame):

    def __init__(self, controller, app):
        super().__init__(app)
        self.controller = controller

        self.image = Image.open(r"C:\Users\User\Desktop\Project\CF&BP\image.png")  # Replace with your image path
        self.photo_image = ImageTk.PhotoImage(self.image)  # Convert image to PhotoImage

        self.image_label = ttk.Label(self, image=self.photo_image)
        self.image_label.grid(row=0, column=0, columnspan=2)  # Use grid layout within image_frame

        self.label_email = ttk.Label(self, text = "ชื่อผู้ใช้งาน")
        self.label_email.grid(row=1, column=0, columnspan=2, pady=(20, 0))

        self.label_password = ttk.Label(self, text = "รหัสผ่าน")
        self.label_password.grid(row=3, column=0, columnspan=2, padx=10, pady=10)

        self.warning_msg = ttk.Label(self, text = "", foreground="red")
        self.warning_msg.grid(row=5, padx=10, pady=10)

        self.entry_email = ttk.Entry(self, width=30, justify= "center")
        self.entry_email.grid(row=2, column=0, columnspan=2 , padx=10, pady=10)
        self.entry_email.insert(0, "admin")

        self.entry_password = ttk.Entry(self, width=30, show="*", justify= "center")
        self.entry_password.grid(row=4, column=0,columnspan=2,  padx=10, pady=10)
        self.entry_password.insert(0, "Daoruang07")

        self.button_login = ttk.Button(self, text="เข้าสู่ระบบ", command=self.login)
        self.button_login.grid(row=6, column=0, columnspan=2, padx=10, pady=10, ipadx=10, ipady=10, sticky='')

        self.button_signup = ttk.Button(self, text="ลงทะเบียน", command=self.controller.show_signup)
        self.button_signup.grid(row=7, column=0, columnspan=2, padx=10, pady=10, sticky='')

    
    def login(self):
        self.controller.authen(self.entry_email.get(), self.entry_password.get())

    def show_error(self):
        self.warning_msg.configure(text="ชื่อผู้ใช้งาน/รหัสผ่าน ผิดพลาด")

    def hide_error(self):
        self.warning_msg.configure(text="")
    
    