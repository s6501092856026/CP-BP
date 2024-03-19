import tkinter as tk
from tkinter import ttk # , PhotoImage, Canvas
from PIL import Image, ImageTk

class LoginView(ttk.Frame):

    def __init__(self, controller, app):
        super().__init__(app)
        self.controller = controller

        # โหลดรูปภาพ
        # image = PhotoImage(file="background.png")  # เปลี่ยน "image.png" เป็นชื่อไฟล์รูปภาพของคุณ

        # สร้าง Canvas
        # canvas = Canvas(self, width=120, height=120)  # ปรับขนาด Canvas ตามต้องการ
        # canvas.create_image(0, 0, anchor=tk.CENTER, image=image)  # ปรับตำแหน่งรูปภาพตามต้องการ
        # canvas.grid(row=0, column=0)


        self.image_frame = ttk.Frame(self)
        self.image_frame.grid(row=0, column=0, columnspan=2, sticky="")

        self.image = Image.open(r"C:\Users\User\Desktop\Project\CF&BP\image.png")  # Replace with your image path
        self.photo_image = ImageTk.PhotoImage(self.image)  # Convert image to PhotoImage

        self.image_label = ttk.Label(self.image_frame, image=self.photo_image)
        self.image_label.grid(row=0, column=0, columnspan=2)  # Use grid layout within image_frame

        self.label_email = ttk.Label(self, text = "Username", foreground="black", font=("Times New Roman", 10, "bold"))
        self.label_email.grid(row=1, column=0, columnspan=2, pady=(20, 0))

        self.label_password = ttk.Label(self, text = "Password", foreground="black", font=("Times New Roman", 10, "bold"))
        self.label_password.grid(row=3, column=0, columnspan=2, padx=10, pady=10)

        self.warning_msg = ttk.Label(self, text = "", foreground="red", font=("Times New Roman", 10, "bold"))
        self.warning_msg.grid(row=5, padx=10, pady=10)

        self.entry_email = ttk.Entry(self, width=30, justify= "center")
        self.entry_email.grid(row=2, column=0, columnspan=2 , padx=10, pady=10)
        self.entry_email.insert(0, "admin")

        self.entry_password = ttk.Entry(self, width=30, show="*", justify= "center")
        self.entry_password.grid(row=4, column=0,columnspan=2,  padx=10, pady=10)
        self.entry_password.insert(0, "Daoruang07")

        self.button_login = ttk.Button(self, text="Login", command=self.login)
        self.button_login.grid(row=6, column=0, columnspan=2, padx=10, pady=10, ipadx=10, ipady=10, sticky='')

        self.button_signup = ttk.Button(self, text="Signup", command=self.controller.show_signup)
        self.button_signup.grid(row=7, column=0, columnspan=2, padx=10, pady=10, sticky='')
    
    def login(self):
        self.controller.authen(self.entry_email.get(), self.entry_password.get())

    def show_error(self):
        self.warning_msg.configure(text="Invalid Username/Password")

    def hide_error(self):
        self.warning_msg.configure(text="")
    
    