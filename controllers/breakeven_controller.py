from views.breakpoint_view import BreakpointView
from utils.window import getCenterPosition
from utils.database import DatabaseUtil

class BreakController:

    def __init__(self, app):
        self.app = app
        self.breakpoint_view = BreakpointView(self, app)

    # def show_break(self):
    #     self.breakpoint_view.pack_forget()  # ลบการแพ็ควิดเจต์ breakpoint_view เพื่อลบออกจากหน้าต่าง (หากมีการแสดงผลอยู่ก่อนหน้านี้)
    #     self.breakpoint_view.pack(padx=10, pady=10, expand=True)  # แสดงวิดเจต์ breakpoint_view พร้อมกับการขยายตัวเต็มขอบเต็มหน้าจอ
    #     self.app.update_idletasks()  # อัพเดตวิดเจต์
    #     width = self.breakpoint_view.winfo_reqwidth() + 20  # เพิ่มขอบเขตบางส่วน
    #     height = self.breakpoint_view.winfo_reqheight() + 20  # เพิ่มขอบเขตบางส่วน
    #     x, y = getCenterPosition(self.app, width=width, height=height)
    #     self.app.geometry(f"{width}x{height}+{x}+{y}")

    def show_break(self):
        self.breakpoint_view.pack_forget()  # ลบการแพ็ควิดเจต์ breakpoint_view เพื่อลบออกจากหน้าต่าง (หากมีการแสดงผลอยู่ก่อนหน้านี้)
        
        db = DatabaseUtil.getInstance()
        product = db.fetch_data("select product_name from product where product_id")

        self.breakpoint_view.pack(padx=10, pady=10, expand=True)  # แสดงวิดเจต์ breakpoint_view พร้อมกับการขยายตัวเต็มขอบเต็มหน้าจอ
        self.app.update_idletasks()  # อัพเดตวิดเจต์
        width = self.breakpoint_view.winfo_reqwidth() + 20  # เพิ่มขอบเขตบางส่วน
        height = self.breakpoint_view.winfo_reqheight() + 20  # เพิ่มขอบเขตบางส่วน
        x, y = getCenterPosition(self.app, width=width, height=height)
        self.app.geometry(f"{width}x{height}+{x}+{y}")

        self.breakpoint_view.set_select(product)


    # def show_break(self):
    #     self.breakpoint_view.pack(padx=10, pady=10)
    #     x, y = getCenterPosition(self.app,width=self.width, height=self.height)
    #     self.app.geometry(f"{self.width}x{self.height}+{x}+{y}")
    #     self.breakpoint_view.pack(padx=10, pady=10, expand=True)
    
    def back_main(self):
        self.breakpoint_view.pack_forget()
        self.app.show_main()
    
    # def show_nameprofile(self):
        # db = DatabaseUtil.getInstance()
        # result = db.fetch_data("SELECT product_name FROM product")
        # self.breakpoint_view.set_nameprofile(result)