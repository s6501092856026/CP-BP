import tkinter as tk
from tkinter import ttk, messagebox
from controllers.tooltip_controller import ToolTipController

class MainView(ttk.Frame):

    def __init__(self, controller, app):
        super().__init__(app)
        self.controller = controller

        self.style = ttk.Style()
        self.style.configure("My.TFrame", background='#C0E4F6')

        # Window
        frame_button = ttk.Frame(self, borderwidth=1, relief="ridge", style='My.TFrame')
        frame_button.grid(row=0, column=1, sticky='NS')

        self.breakeven_button = ttk.Button(frame_button, text="คำนวณการเงิน", command=self.breakeven)
        self.breakeven_button.grid(row=0, column=0, padx=5, pady=11, ipadx=10, ipady=10)

        self.edit_button = ttk.Button(frame_button, text="แก้ไขโปรไฟล์", command=self.edit) 
        self.edit_button.grid(row=1, column=0, padx=5, pady=11, ipadx=10, ipady=10)

        self.newprofile_button = ttk.Button(frame_button, text="สร้างโปรไฟล์ใหม่", command=self.newprofile)
        self.newprofile_button.grid(row=2, column=0, padx=5, pady=11, ipadx=10, ipady=10)

        self.delete_button = ttk.Button(frame_button, text="ลบโปรไฟล์", command=self.delete_selected_item)
        self.delete_button.grid(row=3, column=0, padx=5, pady=11, ipady=10)

        self.compare_button = ttk.Button(frame_button, text="เปรียบเทียบโปรไฟล์", command=self.compare)
        self.compare_button.grid(row=4, column=0, padx=5, pady=11, ipadx=10, ipady=10)   

        # เรียกใช้งานเมท็อด add_button_tooltips() เพื่อเพิ่ม Tooltip สำหรับปุ่ม
        self.add_button_tooltips()

        frame_treeview = ttk.Frame(self, borderwidth=1, relief="ridge", style='My.TFrame')
        frame_treeview.grid(row=0, column=0, sticky='NSWE')

        # Budgets
        self.list_treeview = ttk.Treeview(frame_treeview, columns=("ID", "Name"), show="headings")
        self.list_treeview.heading("ID", text="ไอดี")
        self.list_treeview.column("ID", width=30, stretch=True)
        self.list_treeview.heading("Name", text="ชื่อโปรไฟล์")
        self.list_treeview.column("Name", width=200, stretch=True)
        self.list_treeview.grid(row=0, column=0, ipady=55)

        # สร้าง Scrollbar แนวแกน Y
        scroll_y = ttk.Scrollbar(frame_treeview, orient='vertical', command=self.list_treeview.yview)
        self.list_treeview.configure(yscrollcommand=scroll_y.set)
        scroll_y.grid(row=0, column=1, sticky='NS')

        self.grid_rowconfigure(0, weight=1)
        
        self.list_treeview.bind("<<TreeviewSelect>>", lambda event: self.get_selected_item())

        self.detail_treeview = ttk.Treeview(frame_treeview, columns=("Detail", "Emission Factor", "Amount", "Unit"), show="headings")
        self.detail_treeview.heading("Detail", text="ชื่อ")
        self.detail_treeview.column("Detail", width=370, stretch=True)
        self.detail_treeview.heading("Emission Factor", text="ปัจจัยการปล่อย")
        self.detail_treeview.column("Emission Factor", width=85, stretch=True)
        self.detail_treeview.heading("Amount", text="ปริมาณ")
        self.detail_treeview.column("Amount", width=50, stretch=True)
        self.detail_treeview.heading("Unit", text="หน่วย")
        self.detail_treeview.column("Unit", width=40, stretch=True)
        self.detail_treeview.grid(row=0, column=2, ipady=55)

        # สร้าง Scrollbar แนวแกน Y
        scroll_y = ttk.Scrollbar(frame_treeview, orient='vertical', command=self.detail_treeview.yview)
        self.detail_treeview.configure(yscrollcommand=scroll_y.set)
        scroll_y.grid(row=0, column=3, sticky='NS')

        self.grid_rowconfigure(0, weight=1)

    # เมท็อดสำหรับเพิ่ม Tooltip สำหรับปุ่ม
    def add_button_tooltips(self):
        ToolTipController(self.delete_button, "ลบรายการที่เลือก")
        ToolTipController(self.breakeven_button, "คำนวณจุดคุ้มทุน")
        ToolTipController(self.newprofile_button, "สร้างโปรไฟล์ใหม่")
        ToolTipController(self.compare_button, "เปรียบเทียบโปรไฟล์")
        ToolTipController(self.edit_button, "แก้ไขโปรไฟล์")
    
    def newprofile(self):
        self.detail_treeview.delete(*self.detail_treeview.get_children())
        self.controller.show_newprofile()
    
    def compare(self):
        self.detail_treeview.delete(*self.detail_treeview.get_children())
        self.controller.show_compare()

    def breakeven(self):
        selected_item = self.list_treeview.selection()
        if selected_item:
            profile_name = self.list_treeview.item(selected_item, 'values')[1]
            self.controller.show_break(profile_name)  # ส่ง profile_name ไปยัง show_break
        else:
            messagebox.showinfo("แจ้งเตือน", "กรุณาเลือกรายการก่อน")

    def edit(self):
        selected_item = self.list_treeview.focus()  # Get the item that is currently selected
        if  selected_item:  # If an item is selected
            item_text = self.list_treeview.item(selected_item, 'values')  # Get the text of the selected item
            self.controller.show_editprofile(item_text[0] )
        
    def set_profile(self, products):
        self.list_treeview.delete(*self.list_treeview.get_children())

        for product in products:
            (product_id, product_name) = product
            self.list_treeview.insert("", "end", values=(product_id, product_name))
            
    def set_detail(self, rawmats, transpots, performances):
        self.detail_treeview.delete(*self.detail_treeview.get_children())

        for rawmat in rawmats:
            (name_raw) = rawmat
            self.detail_treeview.insert("", "end", values=(name_raw)) 

        for transpot in transpots:
            (transpot_name) = transpot
            self.detail_treeview.insert("", "end", values=(transpot_name))

        for performance in performances:
            (performance_name) = performance
            self.detail_treeview.insert("", "end", values=(performance_name)) 

    def get_selected_item(self):
        selected_item = self.list_treeview.focus()  # Get the item that is currently selected
        if  selected_item:  # If an item is selected
            item_text = self.list_treeview.item(selected_item, 'values')  # Get the text of the selected item
            self.controller.show_detail(item_text[0])

    def delete_selected_item(self):
        selected_item = self.list_treeview.focus()  # Get the item that is currently selected
        if selected_item:  # If an item is selected
            item_text = self.list_treeview.item(selected_item, 'values')  # Get the text of the selected item
            confirm = messagebox.askyesno("Confirm Delete", "คุณต้องการลบโปรไฟล์นี้ใช่หรือไม่?")
            if confirm:
                self.controller.delete_profile(item_text[0])
                self.controller.show_profile()
