import tkinter as tk
from tkinter import ttk, messagebox
from controllers.tooltip_controller import ToolTipController

class LoginView(ttk.Frame):

    def __init__(self, controller, app):
        super().__init__(app)
        self.controller = controller

        # กำหนดสไตล์สำหรับปุ่ม TButton
        self.style = ttk.Style()
        self.style.configure('My.TButton', relief='ridge', padding=5, background='green')

        # กรอบล็อกอิน
        login_frame = ttk.Frame(self, borderwidth=1, relief="ridge", padding="10 10 10 10")
        login_frame.grid(row=0, column=0, sticky='nsew')

        # โหลดรูปภาพโดยตรงโดยใช้ PhotoImage จาก tkinter
        self.photo_image = tk.PhotoImage(file=r"C:\Users\User\Desktop\Project\CF&BP\image.png")

        self.image_label = ttk.Label(login_frame, justify='center', anchor='center', image=self.photo_image, background='white')
        self.image_label.grid(row=0, column=0, columnspan=2, sticky='nsew')

        self.label_email = ttk.Label(login_frame, text="ชื่อผู้ใช้งาน", background='white')
        self.label_email.grid(row=1, column=0, columnspan=2, pady=(20, 0))

        self.entry_email = ttk.Entry(login_frame, width=30, justify="center")
        self.entry_email.grid(row=2, column=0, columnspan=2, padx=10, pady=10)
        self.entry_email.insert(0, "admin")

        self.label_password = ttk.Label(login_frame, text="รหัสผ่าน", background='white')
        self.label_password.grid(row=3, column=0, columnspan=2, padx=10, pady=10)

        self.entry_password = ttk.Entry(login_frame, width=30, show="*", justify="center")
        self.entry_password.grid(row=4, column=0, columnspan=2, padx=10, pady=10)
        self.entry_password.insert(0, "Daoruang07")

        self.warning_msg = ttk.Label(login_frame, text="", foreground="red", background='white')
        self.warning_msg.grid(row=5, column=0, columnspan=2, padx=5, pady=5)

        self.button_login = ttk.Button(login_frame, text="เข้าสู่ระบบ", command=self.login, style='My.TButton')
        self.button_login.grid(row=6, column=0, columnspan=2, padx=10, pady=10, ipadx=7.5, ipady=7.5)

        self.button_signup = ttk.Button(login_frame, text="ลงทะเบียน", command=self.controller.show_signup)
        self.button_signup.grid(row=7, column=0, columnspan=2, padx=10, pady=10)

        # กรอบหัวข้อ
        title_frame = ttk.Frame(self, borderwidth=1, relief="ridge", padding="10 10 10 10")
        title_frame.grid(row=0, column=1, sticky='nsew')

        self.label_title = ttk.Label(title_frame, justify='center', anchor='center',
                                     text="CF&BP", font=('Arial', 20, 'bold'), background='white')
        self.label_title.grid(row=0, column=0, columnspan=2, padx=10, pady=10, sticky='')

        self.label_subtitle = ttk.Label(title_frame, justify='center', anchor='n',
                                     text="โปรแกรมเพื่อวิเคราะห์คาร์บอนฟุตพริ้นท์\nและความคุ้มค่าการลงทุนของผลิตภัณฑ์\n\n(Program for analyze Carbon Footprint\nand Cost-Benefit Assessment of products) ",
                                     font=('Arial',11), background='white')
        self.label_subtitle.grid(row=1, column=0, columnspan=2, padx=10, pady=10, sticky='nsew')

        self.label_from = ttk.Label(title_frame, justify='right', anchor='se',
                                    text="อาจารย์ที่ปรึกษา\nศ.ดร.อรรถกร เก่งพล\n\nจัดทำโดย\nนายกษิดิศ ดาวเรือง\nX-MIE 6501092856026",
                                    font=('Arial',10), background='white')
        self.label_from.grid(row=2, column=1, sticky='SE')

        # กำหนดการขยายตัวของกรอบหลักเมื่อขนาดหน้าต่างเปลี่ยน
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # กำหนดการขยายตัวของกรอบหัวข้อ
        title_frame.grid_rowconfigure(0, weight=1)
        title_frame.grid_rowconfigure(1, weight=1)
        title_frame.grid_rowconfigure(2, weight=1)
        title_frame.grid_columnconfigure(0, weight=1)
        title_frame.grid_columnconfigure(1, weight=1)

        # กำหนดการขยายตัวของกรอบล็อกอิน
        login_frame.grid_rowconfigure(0, weight=1)
        login_frame.grid_rowconfigure(1, weight=1)
        login_frame.grid_rowconfigure(2, weight=1)
        login_frame.grid_rowconfigure(3, weight=1)
        login_frame.grid_rowconfigure(4, weight=1)
        login_frame.grid_rowconfigure(5, weight=1)
        login_frame.grid_rowconfigure(6, weight=1)
        login_frame.grid_rowconfigure(7, weight=1)
        login_frame.grid_columnconfigure(0, weight=1)
        login_frame.grid_columnconfigure(1, weight=1)

        self.add_tooltips()
    
    def login(self):
        self.controller.authen(self.entry_email.get(), self.entry_password.get())

    def show_error(self):
        self.warning_msg.configure(text="ชื่อผู้ใช้งาน/รหัสผ่าน ผิดพลาด")

    def hide_error(self):
        self.warning_msg.configure(text="")
    
    def add_tooltips(self):
        # เพิ่ม ToolTips สำหรับปุ่มและช่องกรอกข้อมูล
        ToolTipController(self.button_login, "เข้าสู่ระบบ")
        ToolTipController(self.button_signup, "ลงทะเบียนบัญชีใหม่")
        ToolTipController(self.entry_email, "กรุณากรอกชื่อผู้ใช้งาน")
        ToolTipController(self.entry_password, "กรุณากรอกรหัสผ่าน")

# class LoginView(ttk.Frame):

#     def __init__(self, controller, app):
#         super().__init__(app)
#         self.controller = controller

#         # Configure style for TButton
#         self.style = ttk.Style()
#         self.style.configure('My.TButton', relief='ridge', padding=5, background='green')

#         # Load the image directly using PhotoImage from tkinter
#         self.photo_image = tk.PhotoImage(file=r"C:\Users\User\Desktop\Project\CF&BP\image.png")

#         self.image_label = ttk.Label(self, image=self.photo_image, background='white')
#         self.image_label.grid(row=0, column=0, columnspan=2)

#         self.label_email = ttk.Label(self, text = "ชื่อผู้ใช้งาน", background='white')
#         self.label_email.grid(row=1, column=0, columnspan=2, pady=(20, 0))

#         self.label_password = ttk.Label(self, text = "รหัสผ่าน", background='white')
#         self.label_password.grid(row=3, column=0, columnspan=2, padx=10, pady=10)

#         self.warning_msg = ttk.Label(self, text = "", foreground="red", background='white')
#         self.warning_msg.grid(row=5, padx=10, pady=10)

#         self.entry_email = ttk.Entry(self, width=30, justify= "center")
#         self.entry_email.grid(row=2, column=0, columnspan=2 , padx=10, pady=10)
#         self.entry_email.insert(0, "admin")

#         self.entry_password = ttk.Entry(self, width=30, show="*", justify= "center")
#         self.entry_password.grid(row=4, column=0,columnspan=2,  padx=10, pady=10)
#         self.entry_password.insert(0, "Daoruang07")

#         self.button_login = ttk.Button(self, text="เข้าสู่ระบบ", command=self.login, style='My.TButton')
#         self.button_login.grid(row=6, column=0, columnspan=2, padx=10, pady=10, ipadx=10, ipady=10, sticky='')

#         self.button_signup = ttk.Button(self, text="ลงทะเบียน", command=self.controller.show_signup)
#         self.button_signup.grid(row=7, column=0, columnspan=2, padx=10, pady=10, sticky='')

#         self.add_tooltips()
    
#     def login(self):
#         self.controller.authen(self.entry_email.get(), self.entry_password.get())

#     def show_error(self):
#         self.warning_msg.configure(text="ชื่อผู้ใช้งาน/รหัสผ่าน ผิดพลาด")

#     def hide_error(self):
#          self.warning_msg.configure(text="")
    
#     def add_tooltips(self):
#         # เพิ่ม ToolTips สำหรับปุ่ม
#         ToolTipController(self.button_login, "เข้าสู่ระบบ")
#         ToolTipController(self.button_signup, "ลงทะเบียนบัญชีใหม่")
#         ToolTipController(self.entry_email, "กรุณากรอกชื่อผู้ใช้งาน")
#         ToolTipController(self.entry_password, "กรุณากรอกรหัสผ่าน")