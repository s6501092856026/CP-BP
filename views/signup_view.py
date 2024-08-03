from tkinter import ttk,END
from tkinter import messagebox
from controllers.tooltip_controller import ToolTipController

class SignupView(ttk.Frame):

    def __init__(self, controller, app):
        super().__init__(app)
        self.controller = controller

        self.label_firstname = ttk.Label(self, text = "Name", background='white', font=('Tohama', 11))
        self.label_firstname.grid(row=0, column=0, padx=10, pady=10)

        self.label_lastname = ttk.Label(self, text = "Lastname", background='white', font=('Tohama', 11))
        self.label_lastname.grid(row=1, column=0, padx=10, pady=10)

        self.label_tel = ttk.Label(self, text = "Tel.", background='white', font=('Tohama', 11))
        self.label_tel.grid(row=2, column=0, padx=10, pady=10)

        self.label_username = ttk.Label(self, text = "Username", background='white', font=('Tohama', 11))
        self.label_username.grid(row=3, column=0, padx=10, pady=10)

        self.label_password = ttk.Label(self, text = "Password", background='white', font=('Tohama', 11))
        self.label_password.grid(row=4, column=0, padx=10, pady=10)

        self.label_email = ttk.Label(self, text = "E-mail", background='white', font=('Tohama', 11))
        self.label_email.grid(row=5, column=0, padx=10, pady=10)

        self.warning_msg = ttk.Label(self, text= "", foreground="red", background='white')
        self.warning_msg.grid(row=6, column=1, padx=10, pady=10)

        self.firstname = ttk.Entry(self, width=30, font=('Tohama', 10))
        self.firstname.grid(row=0, column=1, padx=10, pady=10)

        self.lastname = ttk.Entry(self, width=30, font=('Tohama', 10))
        self.lastname.grid(row=1, column=1, padx=10, pady=10)

        self.tel = ttk.Entry(self, width=30, font=('Tohama', 10))
        self.tel.grid(row=2, column=1, padx=10, pady=10)

        self.username = ttk.Entry(self, width=30, font=('Tohama', 10))
        self.username.grid(row=3, column=1, padx=10, pady=10)

        self.password = ttk.Entry(self, width=30, font=('Tohama', 10))
        self.password.grid(row=4, column=1, padx=10, pady=10)
        
        self.email = ttk.Entry(self, width=30, font=('Tohama', 10))
        self.email.grid(row=5, column=1, padx=10, pady=10)

        self.signup_button = ttk.Button(self, text="Register",command=self.signup)
        self.signup_button.grid(row=7, column=0, padx=10, pady=10)
        
        self.back_button = ttk.Button(self, text="Back", command=self.controller.show_login)
        self.back_button.grid(row=7, column=1, padx=10, pady=10, sticky='E')

        # สร้าง tooltips
        self.add_tooltips()

    def add_tooltips(self):
        # เพิ่ม tooltips
        ToolTipController(self.firstname, "กรุณากรอกชื่อ")
        ToolTipController(self.lastname, "กรุณากรอกนามสกุล")
        ToolTipController(self.tel, "กรุณากรอกเบอร์โทร")
        ToolTipController(self.username, "กรุณากรอกชื่อผู้ใช้งาน")
        ToolTipController(self.password, "กรุณากรอกรหัสผ่าน")
        ToolTipController(self.email, "กรุณากรอกอีเมลล์")
        ToolTipController(self.signup_button, "คลิกเพื่อสมัครสมาชิก")
        ToolTipController(self.back_button, "คลิกเพื่อกลับสู่หน้าเข้าสู่ระบบ")

    def clear_entries(self):
        self.agree_msg.configure(text="ลงทะเบียนสำเร็จ")
        self.firstname.delete(0,END)
        self.lastname.delete(0,END)
        self.tel.delete(0,END)
        self.username.delete(0,END)
        self.password.delete(0,END)
        self.email.delete(0,END)

    def show_error(self, msg):
        self.warning_msg.configure(text=msg)

    def hide_error(self):
        self.warning_msg.configure(text="")
    
    def signup(self):
        self.controller.signup(self.firstname.get(), self.lastname.get(), self.username.get(), self.email.get(), self.password.get(), self.tel.get())
    
    def show_massagebox(self, msg):
        messagebox.showinfo("Information", msg)