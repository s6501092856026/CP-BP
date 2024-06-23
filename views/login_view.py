import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from controllers.tooltip_controller import ToolTipController
import fitz

class PDFViewer(tk.Toplevel):
    def __init__(self, parent, pdf_path):
        super().__init__(parent)
        self.title("Help")
        self.pdf_path = pdf_path
        self.doc = fitz.open(pdf_path)
        self.current_page = 0

        self.label = tk.Label(self)
        self.label.grid(row=0, column=1)

        self.button_prev = tk.Button(self, text="<", command=self.prev_page)
        self.button_prev.grid(row=0, column=0, padx=10, pady=10)

        self.button_next = tk.Button(self, text=">", command=self.next_page)
        self.button_next.grid(row=0, column=2, padx=10, pady=10)

        self.show_page(self.current_page)

        # Make the PDFViewer window not resizable
        self.resizable(width=False, height=False)

    def show_page(self, page_num):
        page = self.doc.load_page(page_num)
        pix = page.get_pixmap()
        img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
        self.photo = ImageTk.PhotoImage(img)

        self.label.config(image=self.photo)
        self.label.image = self.photo

    def next_page(self):
        if self.current_page < len(self.doc) - 1:
            self.current_page += 1
            self.show_page(self.current_page)

    def prev_page(self):
        if self.current_page > 0:
            self.current_page -= 1
            self.show_page(self.current_page)


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

        self.label_email = ttk.Label(login_frame, text="ชื่อผู้ใช้งาน", font=('Tohama', 10), background='white')
        self.label_email.grid(row=1, column=0, columnspan=2, pady=(20, 0))

        self.entry_email = ttk.Entry(login_frame, width=30, justify="center")
        self.entry_email.grid(row=2, column=0, columnspan=2, padx=10, pady=10)
        self.entry_email.insert(0, "admin")

        self.label_password = ttk.Label(login_frame, text="รหัสผ่าน", font=('Tohama', 10), background='white')
        self.label_password.grid(row=3, column=0, columnspan=2, padx=10, pady=10)

        self.entry_password = ttk.Entry(login_frame, width=30, show="*", justify="center")
        self.entry_password.grid(row=4, column=0, columnspan=2, padx=10, pady=10)
        self.entry_password.insert(0, "Daoruang07")

        self.warning_msg = ttk.Label(login_frame, text="", foreground="red", background='white')
        self.warning_msg.grid(row=5, column=0, columnspan=2, padx=5, pady=5)

        self.button_login = ttk.Button(login_frame, text="เข้าสู่ระบบ", command=self.login, style='My.TButton')
        self.button_login.grid(row=6, column=0, columnspan=2, padx=10, pady=10, ipadx=7.5, ipady=7.5, sticky='')

        self.button_signup = ttk.Button(login_frame, text="ลงทะเบียน", command=self.controller.show_signup)
        self.button_signup.grid(row=7, column=0, columnspan=2, padx=10, pady=10, sticky='')

        # กรอบหัวข้อ
        title_frame = ttk.Frame(self, borderwidth=1, relief="ridge", padding="10 10 10 10") # 
        title_frame.grid(row=0, column=1, sticky='nsew')

        # สร้าง Canvas สำหรับพื้นหลัง
        self.canvas = tk.Canvas(title_frame, width=750, height=450)
        self.canvas.grid(row=0, column=0, rowspan=3, columnspan=2, sticky='nsew')

        # โหลดและตั้งค่าพื้นหลัง
        bg_image_path = r"C:\Users\User\Desktop\Project\CF&BP\Background.jpg"
        bg_image = Image.open(bg_image_path)
        
        # ปรับขนาดภาพให้พอดีกับ title_frame
        bg_image = bg_image.resize((750, 450), Image.LANCZOS)
        self.bg_photo = ImageTk.PhotoImage(bg_image)
        self.canvas.create_image(0, 0, image=self.bg_photo, anchor='nw')

        self.label_title = ttk.Label(title_frame, justify='left', anchor='s',
                                     text="โปรแกรมเพื่อวิเคราะห์คาร์บอนฟุตพริ้นท์\nและความคุ้มค่าการลงทุนของผลิตภัณฑ์"
                                     , font=('Tohama', 12, 'bold'))
        self.label_title.grid(row=0, column=0, padx=10, sticky='W')
        
        self.label_subtitle = ttk.Label(title_frame, justify='left', anchor='s',
                                     text="(Program for analyze Carbon Footprint\nand Cost-Benefit Assessment of products) "
                                     , font=('Tohama', 12, 'bold'))
        self.label_subtitle.grid(row=2, column=0, padx=10, sticky='W')

        self.label_from = ttk.Label(title_frame, justify='right', anchor='se',
                                    text="อาจารย์ที่ปรึกษา\nศ.ดร.อรรถกร เก่งพล\n\nจัดทำโดย\nนายกษิดิศ ดาวเรือง\nX-MIE 6501092856026"
                                    , font=('Tohama', 10))
        self.label_from.grid(row=2, column=1, sticky='SE')

        # ปุ่มเครื่องหมายคำถาม
        self.button_help = ttk.Button(title_frame, text="?", command=self.show_help)
        self.button_help.grid(row=2, column=0, ipadx=2, ipady=2, padx=0, pady=0, sticky='sw')

        # # ปุ่มเครื่องหมายคำถาม
        # self.button_help = ttk.Button(title_frame, text="?", command=self.show_help)
        # self.button_help.place(relx=0.05, rely=0.95, anchor='sw')
        
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
        ToolTipController(self.button_help, "help")

    def show_help(self):
        # ฟังก์ชันที่แสดงหน้าช่วยเหลือ
        pdf_path = r"C:\Users\User\Desktop\Project\CF&BP\help.pdf"
        PDFViewer(self, pdf_path)
    

