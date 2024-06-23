import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import openpyxl.drawing
import openpyxl.drawing.image
import openpyxl.styles
import openpyxl
from io import BytesIO
from controllers.tooltip_controller import ToolTipController
import locale

# ตั้งค่าภาษาและภูมิภาค
locale.setlocale(locale.LC_ALL, 'th_TH.UTF-8')

class ConprepareView(ttk.Frame):

    def __init__(self, controller, app):
        super().__init__(app)
        self.controller = controller
        self.items = []

        self.style = ttk.Style()
        self.style.configure("My.TFrame", background='#C0E4F6')

        # Window
        self.main_frame =  ttk.Frame(self)

        self.label_profile1 = ttk.Label(self, borderwidth=1, relief="ridge", text = "", justify='center') 
        self.label_profile1.grid(row=1, column=0, sticky='NSWE')
        self.label_profile1.configure(anchor='center')

        self.label_profile2 = ttk.Label(self, borderwidth=1, relief="ridge", text = "", justify='center')
        self.label_profile2.grid(row=1, column=1, sticky='NSWE')
        self.label_profile2.configure(anchor='center')

        # Frame CF
        frame_cf = ttk.Frame(self, borderwidth=1, relief="ridge")
        frame_cf.grid(row=5, column=2, sticky='NSWE')

        self.label_percentcf = ttk.Label(frame_cf, borderwidth=1, relief="ridge", justify='center', text = "   ส่วนต่างคาร์บอนฟุตพริ้นท์")
        self.label_percentcf.grid(row=0, column=0, sticky='NSWE')
        self.label_percentcf.configure(anchor='w', background='#C0E4F6')

        self.label_cf = ttk.Label(frame_cf, borderwidth=1, relief="ridge", justify='center', text = "")
        self.label_cf.grid(row=0, column=1, sticky = 'NSWE')
        self.label_cf.configure(anchor='center', background='white')

        self.dif_revenue = ttk.Label(frame_cf, borderwidth=1, relief="ridge", justify='center', text = "   ส่วนต่างต้นทุนรวม")
        self.dif_revenue.grid(row=1, column=0, sticky='NSWE')
        self.dif_revenue.configure(anchor='w', background='#C0E4F6')

        self.add_dif_revenue = ttk.Label(frame_cf, borderwidth=1, relief="ridge", justify='center', text = "")
        self.add_dif_revenue.grid(row=1, column=1, sticky='NSWE')
        self.add_dif_revenue.configure(anchor='center', background='white')

        self.dif_percent = ttk.Label(frame_cf, borderwidth=1, relief="ridge", justify='center', text = "   ส่วนต่างกำไร")
        self.dif_percent.grid(row=2, column=0, sticky='NSWE')
        self.dif_percent.configure(anchor='w', background='#C0E4F6')

        self.add_dif_percent = ttk.Label(frame_cf, borderwidth=1, relief="ridge", justify='center', text = "")
        self.add_dif_percent.grid(row=2, column=1, sticky = 'NSWE')
        self.add_dif_percent.configure(anchor='center', background='white')

        # Button
        self.return_button = ttk.Button(self, text="Return to Profile", command=self.back)
        self.return_button.grid(row=5, column=0, padx=10, pady=10, ipadx=10, ipady=10, sticky = 'W')

        self.export_button = ttk.Button(self, text="Export to Excel") # , command=self.export
        self.export_button.grid(row=5, column=0, padx=10, pady=10, ipadx=10, ipady=10, sticky = 'E')

        # Frame Profile1
        frame_profile1 = ttk.Frame(self, borderwidth=1, relief="ridge", style="My.TFrame")
        frame_profile1.grid(row=2, rowspan=3, column=0, sticky='NSWE')

        self.profile1_treeview = ttk.Treeview(frame_profile1, columns=("Name", "Carbon"), show="headings")
        self.profile1_treeview.heading("Name", text="ชื่อ (X)")
        self.profile1_treeview.column("Name", width=370, stretch=True)
        text_width = len("คาร์บอนเทียบเท่า (Y)")  # คำนวณความยาวของข้อความ
        self.profile1_treeview.heading("Carbon", text="ค่าคาร์บอน (Y)")
        self.profile1_treeview.column("Carbon", width=text_width * 5)
        # self.profile1_treeview.heading("Unit", text="หน่วย")
        # self.profile1_treeview.column("Unit", width=60, stretch=True)
        self.profile1_treeview.grid(row=0, column=0)

        # สร้าง Scrollbar แนวแกน Y
        scroll_y = ttk.Scrollbar(frame_profile1, orient='vertical', command=self.profile1_treeview.yview)
        self.profile1_treeview.configure(yscrollcommand=scroll_y.set)
        scroll_y.grid(row=0, column=1, sticky='NS')

        self.grid_rowconfigure(0, weight=1)

        # Frame Profile2
        frame_profile2 = ttk.Frame(self, borderwidth=1, relief="ridge", style="My.TFrame")
        frame_profile2.grid(row=2, rowspan=3, column=1, sticky='NSWE')

        self.profile2_treeview = ttk.Treeview(frame_profile2, columns=("Name", "Carbon"), show="headings") # , "Unit"
        self.profile2_treeview.heading("Name", text="ชื่อ (X)")
        self.profile2_treeview.column("Name", width=370, stretch=True)
        text_width = len("คาร์บอนเทียบเท่า (Y)")  # คำนวณความยาวของข้อความ
        self.profile2_treeview.heading("Carbon", text="ค่าคาร์บอน (Y)")
        self.profile2_treeview.column("Carbon", width=text_width * 5)
        # self.profile2_treeview.heading("Unit", text="หน่วย")
        # self.profile2_treeview.column("Unit", width=60, stretch=True)
        self.profile2_treeview.grid(row=0, column=0)

        # สร้าง Scrollbar แนวแกน Y
        scroll_y = ttk.Scrollbar(frame_profile2, orient='vertical', command=self.profile2_treeview.yview)
        self.profile2_treeview.configure(yscrollcommand=scroll_y.set)
        scroll_y.grid(row=0, column=1, sticky='NS')

        self.grid_rowconfigure(0, weight=1)

        # Frame Breakeven_point
        frame_break = ttk.Frame(self, borderwidth=1, relief="ridge")
        frame_break.grid(row=0, column=2, sticky='NSWE')

        self.break_profile1 = ttk.Label(frame_break, text = "", borderwidth=1, relief="ridge")
        self.break_profile1.grid(row=0, column=0, columnspan=3, sticky='NSWE')
        self.break_profile1.configure(anchor='center')

        self.totalcost = ttk.Label(frame_break, text = "ต้นทุนรวม")
        self.totalcost.grid(row=1, column=0, padx=10, pady=10, sticky='W')
        self.totalcost.configure(anchor='w', background='white')

        # self.revenue = ttk.Label(frame_break, text = "รายได้")
        # self.revenue.grid(row=2, column=0, padx=10, pady=11, sticky='W')
        # self.revenue.configure(anchor='w', background='white')
        
        self.profit = ttk.Label(frame_break, text = "กำไร")
        self.profit.grid(row=2, column=0, padx=10, pady=10, sticky='W')
        self.profit.configure(anchor='w', background='white')
        
        self.breakeven = ttk.Label(frame_break, text = "ปริมาณผลิตที่จุดคุ้มทุน")
        self.breakeven.grid(row=3, column=0, padx=10, pady=10, sticky='W')
        self.breakeven.configure(anchor='w', background='white')

        # self.efficiency = ttk.Label(frame_break, text = "ประสิทธิภาพการผลิต")
        # self.efficiency.grid(row=4, column=0, padx=10, pady=11, sticky='W')
        # self.efficiency.configure(anchor='w', background='white')

        self.add_totalcost = ttk.Label(frame_break, text = "")
        self.add_totalcost.grid(row=1, column=1, padx=10, pady=10, sticky='E')
        self.add_totalcost.configure(anchor='w', background='white')

        # self.add_revenue = ttk.Label(frame_break, text = "")
        # self.add_revenue.grid(row=2, column=1, padx=10, pady=11, sticky='E')
        # self.add_revenue.configure(anchor='w', background='#FFD10A')

        self.add_profit = ttk.Label(frame_break, text = "")
        self.add_profit.grid(row=2, column=1, padx=10, pady=10, sticky='E')
        self.add_profit.configure(anchor='w', background='white')

        self.add_breakeven = ttk.Label(frame_break, text = "")
        self.add_breakeven.grid(row=3, column=1, padx=10, pady=10, sticky='E')
        self.add_breakeven.configure(anchor='w', background='white')

        # self.add_efficiency = ttk.Label(frame_break, text = "")
        # self.add_efficiency.grid(row=4, column=1, padx=10, pady=11, sticky='E')
        # self.add_efficiency.configure(anchor='w', background='#FFD10A')

        self.unit_totalcost = ttk.Label(frame_break, text = "บาท")
        self.unit_totalcost.grid(row=1, column=2, padx=10, pady=10)
        self.unit_totalcost.configure(anchor='e', background='white')

        # self.unit_revenue = ttk.Label(frame_break, text = "บาท")
        # self.unit_revenue.grid(row=2, column=2, padx=10, pady=11)
        # self.unit_revenue.configure(anchor='e', background='white')

        self.unit_profit = ttk.Label(frame_break, text = "บาท")
        self.unit_profit.grid(row=2, column=2, padx=10, pady=10)
        self.unit_profit.configure(anchor='e', background='white')

        self.unit_breakeven = ttk.Label(frame_break, text = "หน่วย")
        self.unit_breakeven.grid(row=3, column=2, padx=10, pady=10)
        self.unit_breakeven.configure(anchor='e', background='white')

        # self.unit_efficiency = ttk.Label(frame_break, text = "%")
        # self.unit_efficiency.grid(row=4, column=2, padx=10, pady=11)
        # self.unit_efficiency.configure(anchor='e', background='white')

        self.break_profile2 = ttk.Label(frame_break, text = "", borderwidth=1, relief="ridge")
        self.break_profile2.grid(row=4, column=0, columnspan=3, sticky='NSWE')
        self.break_profile2.configure(anchor='center')
        
        self.totalcost2 = ttk.Label(frame_break, text = "ต้นทุนรวม")
        self.totalcost2.grid(row=5, column=0, padx=10, pady=10, sticky='W')
        self.totalcost2.configure(anchor='w', background='white')

        # self.revenue2 = ttk.Label(frame_break, text = "รายได้")
        # self.revenue2.grid(row=2, column=0, padx=10, pady=11, sticky='W')
        # self.revenue2.configure(anchor='w', background='white')
        
        self.profit2 = ttk.Label(frame_break, text = "กำไร")
        self.profit2.grid(row=6, column=0, padx=10, pady=10, sticky='W')
        self.profit2.configure(anchor='w', background='white')
        
        self.breakeven2 = ttk.Label(frame_break, text = "ปริมาณผลิตที่จุดคุ้มทุน")
        self.breakeven2.grid(row=7, column=0, padx=10, pady=10, sticky='W')
        self.breakeven2.configure(anchor='w', background='white')

        # self.efficiency2 = ttk.Label(frame_break, text = "ประสิทธิภาพการผลิต")
        # self.efficiency2.grid(row=4, column=0, padx=10, pady=11, sticky='W')
        # self.efficiency2.configure(anchor='w', background='white')

        self.add_totalcost2 = ttk.Label(frame_break, text = "")
        self.add_totalcost2.grid(row=5, column=1, padx=10, pady=10, sticky='E')
        self.add_totalcost2.configure(anchor='w', background='white')

        # self.add_revenue2 = ttk.Label(frame_break, text = "")
        # self.add_revenue2.grid(row=2, column=1, padx=10, pady=11, sticky='E')
        # self.add_revenue2.configure(anchor='w', background='#FFD10A')

        self.add_profit2 = ttk.Label(frame_break, text = "")
        self.add_profit2.grid(row=6, column=1, padx=10, pady=10, sticky='E')
        self.add_profit2.configure(anchor='w', background='white')

        self.add_breakeven2 = ttk.Label(frame_break, text = "")
        self.add_breakeven2.grid(row=7, column=1, padx=10, pady=10, sticky='E')
        self.add_breakeven2.configure(anchor='w', background='white')

        # self.add_efficiency2 = ttk.Label(frame_break, text = "")
        # self.add_efficiency2.grid(row=4, column=1, padx=10, pady=11, sticky='E')
        # self.add_efficiency2.configure(anchor='w', background='#FFD10A')

        self.unit_totalcost2 = ttk.Label(frame_break, text = "บาท")
        self.unit_totalcost2.grid(row=5, column=2, padx=10, pady=10)
        self.unit_totalcost2.configure(anchor='e', background='white')

        # self.unit_revenue2 = ttk.Label(frame_break, text = "บาท")
        # self.unit_revenue2.grid(row=2, column=2, padx=10, pady=11)
        # self.unit_revenue2.configure(anchor='e', background='white')

        self.unit_profit2 = ttk.Label(frame_break, text = "บาท")
        self.unit_profit2.grid(row=6, column=2, padx=10, pady=10)
        self.unit_profit2.configure(anchor='e', background='white')

        self.unit_breakeven2 = ttk.Label(frame_break, text = "หน่วย")
        self.unit_breakeven2.grid(row=7, column=2, padx=10, pady=10)
        self.unit_breakeven2.configure(anchor='e', background='white')

        # self.unit_efficiency2 = ttk.Label(frame_break, text = "%")
        # self.unit_efficiency2.grid(row=4, column=2, padx=10, pady=11)
        # self.unit_efficiency2.configure(anchor='e', background='white')

        # Frame Recommend (รวมทั้งสาม frame เป็นกรอบเดียว)
        frame_recommend = ttk.Frame(self, borderwidth=1, relief="ridge")
        frame_recommend.grid(row=1, rowspan=4, column=2, sticky='NSWE')

        self.label_carbon_footprint = ttk.Label(frame_recommend, borderwidth=1, relief="ridge", text="พิจารณาที่คาร์บอนฟุตพริ้นท์", anchor='center', background='#C0E4F6')
        self.label_carbon_footprint.grid(row=0, column=0, sticky='NSWE')

        self.label_compare_summary = ttk.Label(frame_recommend, justify='center', text="", anchor='center', background='white')
        self.label_compare_summary.grid(row=1, column=0, padx=10, pady=10, sticky='NSWE')

        self.label_total_cost = ttk.Label(frame_recommend, borderwidth=1, relief="ridge", text="พิจารณาต้นทุน", anchor='center', background='#C0E4F6')
        self.label_total_cost.grid(row=2, column=0, sticky='NSWE')

        self.label_total_cost_summary = ttk.Label(frame_recommend, justify='center', text="", anchor='center', background='white')
        self.label_total_cost_summary.grid(row=3, column=0, padx=10, pady=10, sticky='NSWE')

        self.label_profit = ttk.Label(frame_recommend, borderwidth=1, relief="ridge", text="พิจารณากำไร", anchor='center', background='#C0E4F6')
        self.label_profit.grid(row=4, column=0, sticky='NSWE')

        self.label_profit_summary = ttk.Label(frame_recommend, justify='center', text="", anchor='center', background='white')
        self.label_profit_summary.grid(row=5, column=0, padx=10, pady=10, sticky='NSWE')

        # Configure the grid to make it flexible
        self.grid_rowconfigure(2, weight=1)
        self.grid_rowconfigure(3, weight=1)
        self.grid_rowconfigure(4, weight=1)
        self.grid_columnconfigure(2, weight=1)

        frame_cf.grid_rowconfigure(0, weight=1)
        frame_cf.grid_rowconfigure(1, weight=1)
        frame_cf.grid_rowconfigure(2, weight=1)
        frame_cf.grid_columnconfigure(0, weight=1)
        frame_cf.grid_columnconfigure(1, weight=1)

        frame_profile1.grid_rowconfigure(0, weight=1)
        frame_profile1.grid_columnconfigure(0, weight=1)
        frame_profile1.grid_columnconfigure(1, weight=0)

        frame_profile2.grid_rowconfigure(0, weight=1)
        frame_profile2.grid_columnconfigure(0, weight=1)
        frame_profile2.grid_columnconfigure(1, weight=0)

        frame_recommend.grid_rowconfigure(0, weight=1)
        frame_recommend.grid_rowconfigure(1, weight=1)
        frame_recommend.grid_rowconfigure(2, weight=1)
        frame_recommend.grid_rowconfigure(3, weight=1)
        frame_recommend.grid_rowconfigure(4, weight=1)
        frame_recommend.grid_rowconfigure(5, weight=1)
        frame_recommend.grid_columnconfigure(0, weight=1)

        self.add_button_tooltips()

    def add_button_tooltips(self):
        ToolTipController(self.export_button, "ส่งออกไปยัง Excel")
        ToolTipController(self.return_button, "กลับไปยังหน้าหลัก")
        
    def back(self):
        self.controller.back_main()

    def format_currency(self, value):
        return locale.currency(value, grouping=True)
    
    def set_breakpoint_data(self, profile1, profile2, breakpoint_data1, breakpoint_data2):
        revenue1 = None
        revenue2 = None
        profit1 = 0.0
        profit2 = 0.0

        if breakpoint_data1:
            fixed_cost, variable_cost, number_of_units, unit_price, product_efficiency = breakpoint_data1[0]
            total_cost1 = fixed_cost + (variable_cost * number_of_units)
            revenue1 = unit_price * number_of_units
            profit1 = revenue1 - total_cost1
            breakeven1 = fixed_cost / (unit_price - variable_cost)
            
            self.add_totalcost.config(text=self.format_currency(total_cost1))
            # self.add_revenue.config(text=self.format_currency(revenue1))
            self.add_profit.config(text=self.format_currency(profit1), foreground="red" if profit1 < 0 else "green")
            self.add_breakeven.config(text=f"{breakeven1:.2f}",foreground="red" if breakeven1 < 0 else "black")
            # self.add_efficiency.config(text=f"{product_efficiency:.2f}")
        else:
            self.add_totalcost.config(text="-", foreground="black")
            # self.add_revenue.config(text="-", foreground="black")
            self.add_profit.config(text="-", foreground="black")
            self.add_breakeven.config(text="-", foreground="black")
            # self.add_efficiency.config(text="-", foreground="black")

        if breakpoint_data2:
            fixed_cost, variable_cost, number_of_units, unit_price, product_efficiency = breakpoint_data2[0]
            total_cost2 = fixed_cost + (variable_cost * number_of_units)
            revenue2 = unit_price * number_of_units
            profit2 = revenue2 - total_cost2
            breakeven2 = fixed_cost / (unit_price - variable_cost)

            self.add_totalcost2.config(text=self.format_currency(total_cost2))
            # self.add_revenue2.config(text=self.format_currency(revenue2))
            self.add_profit2.config(text=self.format_currency(profit2), foreground="red" if profit2 < 0 else "green")
            self.add_breakeven2.config(text=f"{breakeven2:.2f}", foreground="red" if breakeven2 < 0 else "black")
            # self.add_efficiency2.config(text=f"{product_efficiency:.2f}")
        else:
            self.add_totalcost2.config(text="-", foreground="black")
            # self.add_revenue2.config(text="-", foreground="black")
            self.add_profit2.config(text="-", foreground="black")
            self.add_breakeven2.config(text="-", foreground="black")
            # self.add_efficiency2.config(text="-", foreground="black")

        # คำนวณและแสดงความแตกต่างเปอร์เซ็นต์ในกำไรหากมีทั้งสองกำไรที่พร้อมใช้งาน
        if profit1 is not None and profit2 is not None:
            percentage_difference = ((profit2 - profit1) / profit1) * 100
            if percentage_difference >= 0:
                self.add_dif_percent.config(
                    text=f"+{percentage_difference:.2f}%",
                    foreground="green")
            else:
                self.add_dif_percent.config(
                    text=f"{percentage_difference:.2f}%",
                    foreground="red")

            # แสดงผลต่าง % ของ revenue1 กับ revenue2 ใน add_dif_revenue
            revenue_difference = ((revenue2 - revenue1) / revenue1) * 100
            if revenue_difference >= 0:
                self.add_dif_revenue.config(
                    text=f"+{revenue_difference:.2f}%",
                    foreground="green")
            else:
                self.add_dif_revenue.config(
                    text=f"{revenue_difference:.2f}%",
                    foreground="red")
        else:
            self.add_dif_percent.config(text="-", foreground="black")
            self.add_dif_revenue.config(text="-", foreground="black")

        # เรียกฟังก์ชัน setBreakevenGraph เพื่อสร้างกราฟ โดยส่ง profile1, profile2, profit1 และ profit2 ไปให้
        self.setBreakevenGraph(profile1, profile2, total_cost1, total_cost2, profit1, profit2)

    def setCompareGraph(self, profile1, profile2):
        # สร้างภาพ Matplotlib
        figure = Figure(figsize=(6.5, 3.75), dpi=70)
        subplot = figure.add_subplot(111)

        # ดึงและรวมค่า "คาร์บอน" จากข้อมูลโปรไฟล์ 1 และ 2
        x_labels = [profile1, profile2]
        y_values = [0, 0]

        # รวมค่าคาร์บอนสำหรับโปรไฟล์ 1
        for item in self.profile1_treeview.get_children():
            y_values[0] += float(self.profile1_treeview.item(item, "values")[1])  # สมมติว่า "Carbon" เป็นคอลัมน์ที่สอง

        # รวมค่าคาร์บอนสำหรับโปรไฟล์ 2
        for item in self.profile2_treeview.get_children():
            y_values[1] += float(self.profile2_treeview.item(item, "values")[1])  # สมมติว่า "Carbon" เป็นคอลัมน์ที่สอง

        # สร้างกราฟแท่งโดยใช้สีต่าง ๆ สำหรับแต่ละแท่ง
        bars = subplot.bar(range(len(x_labels)), y_values, color=['#C0E4F6', '#E8ABB5'], width=0.1, align='center')

        # เพิ่มตัวเลขกำกับที่กราฟแท่ง
        for bar in bars:
            yval = bar.get_height()
            subplot.text(bar.get_x() + bar.get_width() / 2, yval + 0.05, f'{yval:.2f}', ha='center', va='bottom', fontsize=8, fontweight='bold', color='black')

        # เพิ่มหัวเรื่อง
        subplot.set_title('Comparison of Carbon footprint', fontsize=8, fontweight='bold', color='black')
        subplot.set_ylabel('KgCO2eq', fontsize=8, fontweight='bold', color='black')

        # ปรับแต่งเส้นขอบ
        subplot.spines['top'].set_visible(False)
        subplot.spines['right'].set_visible(False)
        subplot.spines['left'].set_color('black')
        subplot.spines['bottom'].set_color('black')

        # กำหนดแบบอักษรและสีของเส้น
        subplot.tick_params(axis='both', which='major', labelsize=8, colors='black')

         # กำหนดระยะห่างระหว่างแท่ง
        subplot.set_xticks(range(len(x_labels)))

        # กำหนดแท่งใหม่เป็นชื่อของแต่ละ profile
        subplot.set_xticklabels(x_labels)

        # สร้างเฟรมสำหรับกราฟ
        frame = tk.Frame(self, highlightbackground='black', highlightthickness=1, borderwidth=1, relief="ridge")
        frame.grid(row=0, column=0, sticky="NSWE")

        # สร้างวิดเจ็ต FigureCanvasTkAgg
        canvas = FigureCanvasTkAgg(figure, master=frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        # สร้างข้อความเปรียบเทียบ
        summary_text = ""

        # เปรียบเทียบคาร์บอนฟุตพริ้นท์และสร้างข้อความคำแนะนำ
        if y_values[0] < y_values[1]:
            summary_text = f"{profile1} < {profile2}\n"
            summary_text += f"ควรเลือก {profile1} เพื่อคาร์บอนฟุตพริ้นท์ต่ำสุด"
        elif y_values[0] > y_values[1]:
            summary_text = f"{profile2} < {profile1}\n"
            summary_text += f"ควรเลือก {profile2} เพื่อคาร์บอนฟุตพริ้นท์ต่ำสุด"
        else:
            # summary_text = f"คาร์บอนฟุตพริ้นท์ของ {profile1} และ {profile2} เท่ากัน\n\n"
            summary_text += f"ทั้งสองมีคาร์บอนฟุตพริ้นท์เท่ากัน"

        # อัพเดตป้ายข้อความสรุป
        self.label_compare_summary.config(text=summary_text) # , background='#FFD10A'

    def setBreakevenGraph(self, profile1, profile2, total_cost1, total_cost2, profit1, profit2):
        # สร้างภาพ Matplotlib
        figure = Figure(figsize=(6.5, 3.75), dpi=70)
        subplot = figure.add_subplot(111)

        # ป้ายกำกับข้อมูลสำหรับแกน x
        x_labels = [profile1, profile2]

        # ค่าของแกน y สำหรับต้นทุนรวมและกำไร
        y_values = [[total_cost1, profit1], [total_cost2, profit2]]

        # กำหนดตำแหน่ง x ของแต่ละแท่งกราฟ
        x = range(len(x_labels))

        # ความกว้างของแท่งกราฟ
        bar_width = 0.25

        # สร้างกราฟแท่ง
        bars1 = subplot.bar([pos - bar_width/2 for pos in x], [y[0] for y in y_values], bar_width, label='Total Cost', color='#C0E4F6')
        bars2 = subplot.bar([pos + bar_width/2 for pos in x], [y[1] for y in y_values], bar_width, label='Profit', color='#E8ABB5')

        # เพิ่มตัวเลขกำกับที่กราฟแท่งในหน่วยเงินบาท
        for bars in [bars1, bars2]:
            for bar in bars:
                yval = bar.get_height()
                formatted_value = self.format_currency(yval)
                subplot.text(bar.get_x() + bar.get_width() / 2, yval + 0.05, formatted_value, ha='center', va='bottom', fontsize=8, fontweight='bold', color='black')

        # เพิ่มหัวเรื่องให้กับกราฟ
        subplot.set_title('Comparison of Total Cost and Profit', fontsize=10, fontweight='bold', color='black')

        # กำหนดป้ายชื่อแกน y
        subplot.set_ylabel('Baht', fontsize=8, fontweight='bold', color='black')

        # ปรับแต่งเส้นขอบของกราฟ
        subplot.spines['top'].set_visible(False)
        subplot.spines['right'].set_visible(False)
        subplot.spines['left'].set_color('black')
        subplot.spines['bottom'].set_color('black')

        # กำหนดพารามิเตอร์ของเส้นแบ่ง
        subplot.tick_params(axis='both', which='major', labelsize=8, colors='black')

        # กำหนดตำแหน่งและป้ายกำกับของ x-tick
        subplot.set_xticks(x)
        subplot.set_xticklabels(x_labels)

        # เพิ่มตำนาน (legend)
        subplot.legend()

        # สร้างเฟรมเพื่อถือกราฟ
        frame = tk.Frame(self, highlightbackground='black', highlightthickness=1, borderwidth=1, relief="ridge")
        frame.grid(row=0, column=1, sticky="NSWE")

        # สร้างวิดเจ็ต FigureCanvasTkAgg และเพิ่มลงในเฟรม
        canvas = FigureCanvasTkAgg(figure, master=frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        # สร้างข้อความเปรียบเทียบสำหรับต้นทุนรวม
        total_cost_summary_text = ""
        if total_cost1 > total_cost2:
            total_cost_summary_text += f"{profile1} > {profile2}\n"
            total_cost_summary_text += f"ควรเลือก {profile2} เพื่อต้นทุนต่ำสุด"
        elif total_cost1 < total_cost2:
            total_cost_summary_text += f"{profile2} > {profile1}\n"
            total_cost_summary_text += f"ควรเลือก {profile1} เพื่อต้นทุนต่ำสุด"
        else:
            total_cost_summary_text += f"ต้นทุนรวมของ {profile1} และ {profile2} เท่ากัน"

        # สร้างข้อความเปรียบเทียบสำหรับกำไร
        profit_summary_text = ""
        if profit1 > profit2:
            profit_summary_text += f"{profile1} > {profile2}\n"
            profit_summary_text += f"ควรเลือก {profile1} เพื่อกำไรสูงสุด"
        elif profit1 < profit2:
            profit_summary_text += f"{profile2} > {profile1}\n"
            profit_summary_text += f"ควรเลือก {profile2} เพื่อกำไรสูงสุด"
        else:
            # profit_summary_text += f"กำไรของ {profile1} และ {profile2} เท่ากัน\n"
            profit_summary_text += f"ทั้งสองทำกำไรได้เท่ากัน"

        # อัพเดตป้ายข้อความสรุปด้วยพื้นหลังสี #FFD10A
        self.label_total_cost_summary.config(text=total_cost_summary_text) # , background='#FFD10A'
        self.label_profit_summary.config(text=profit_summary_text)

    def show_profile(self, profile1, profile2, rawmats_1, transpots_1,
                      performances_1, rawmats_2, transpots_2, performances_2, breakpoint_data1, breakpoint_data2):

        # Check if any of the data is None
        if rawmats_1 is None or transpots_1 is None or performances_1 is None or rawmats_2 is None or transpots_2 is None or performances_2 is None:
            messagebox.showerror("Error", "Data is missing")
            return

        # แสดงข้อมูลโปรไฟล์ที่เลือกใน Label
        self.label_profile1.config(text=profile1)
        self.label_profile2.config(text=profile2)
        self.break_profile1.config(text=profile1)
        self.break_profile2.config(text=profile2)

        # Clear existing data in the treeview
        self.profile1_treeview.delete(*self.profile1_treeview.get_children())
        self.profile2_treeview.delete(*self.profile2_treeview.get_children())

        # Insert raw materials data for profile 1
        for rawmat in rawmats_1:
            self.profile1_treeview.insert("", "end", values=(rawmat[0], round(float(rawmat[1]) * float(rawmat[2]), 3), "KgCO2eq"))

        # Insert transportation data for profile 1
        for transpot in transpots_1:
            self.profile1_treeview.insert("", "end", values=(transpot[0], round(float(transpot[1]) * float(transpot[2]), 3), "KgCO2eq"))

        # Insert performances data for profile 1
        for performance in performances_1:
            self.profile1_treeview.insert("", "end", values=(performance[0], round(float(performance[1]) * float(performance[2]), 3), "KgCO2eq"))

        # Insert raw materials data for profile 2
        for rawmat in rawmats_2:
            self.profile2_treeview.insert("", "end", values=(rawmat[0], round(float(rawmat[1]) * float(rawmat[2]), 3), "KgCO2eq"))

        # Insert transportation data for profile 2
        for transpot in transpots_2:
            self.profile2_treeview.insert("", "end", values=(transpot[0], round(float(transpot[1]) * float(transpot[2]), 3), "KgCO2eq"))

        # Insert performances data for profile 2
        for performance in performances_2:
            self.profile2_treeview.insert("", "end", values=(performance[0], round(float(performance[1]) * float(performance[2]), 3), "KgCO2eq"))

        self.setCompareGraph(profile1, profile2)
        self.set_breakpoint_data(profile1, profile2, breakpoint_data1, breakpoint_data2)
        self.updateLabel()
    
    def updateLabel(self):
        # คำนวณค่าคาร์บอนทั้งหมดสำหรับโปรไฟล์ 1
        total_carbon_profile1 = sum(float(self.profile1_treeview.item(item, "values")[1]) for item in self.profile1_treeview.get_children())

        # คำนวณค่าคาร์บอนทั้งหมดสำหรับโปรไฟล์ 2
        total_carbon_profile2 = sum(float(self.profile2_treeview.item(item, "values")[1]) for item in self.profile2_treeview.get_children())

        # คำนวณเปอร์เซ็นต์ความแตกต่าง
        if total_carbon_profile1 != 0:
            percentage_difference = ((total_carbon_profile1 - total_carbon_profile2) / total_carbon_profile1) * 100
        else:
            percentage_difference = 0  # เพื่อจัดการการหารด้วยศูนย์

        # จัดรูปแบบเปอร์เซ็นต์ความแตกต่างโดยมี "+" นำหน้าหากเป็นบวก
        percentage_text = f"{percentage_difference:+.2f}%" if percentage_difference >= 0 else f"{percentage_difference:.2f}%"

        # อัปเดตป้ายข้อความด้วยเปอร์เซ็นต์ความแตกต่างและเปลี่ยนสีถ้าเป็นลบ
        if percentage_difference < 0:
            self.label_cf.config(text=percentage_text, foreground = "red")
        else:
            self.label_cf.config(text=percentage_text, foreground = "green")

    # def export(self):
    #     wb = openpyxl.Workbook()  # สร้างอ็อบเจ็กต์สมุดงานใหม่
    #     sheet = wb.active  # รับแผ่นงานที่กำลังใช้งาน

    #     profile1 = []
    #     profile2 = [] 
        
    
    #     for category, _, name, amount, unit in self.items:
    #         if category == 'Material':
    #             profile1.append((name, amount, unit))              
    #         elif category == 'Transpotation':
    #             profile2.append((name, amount, unit))

    #     # วาดกราฟ
    #     figure = Figure(figsize=(5, 3), dpi=70)
    #     subplot = figure.add_subplot(111)

    #     x = [item[0] for item in profile1]
    #     y = [float(item[1]) for item in profile2]

    #     subplot.tick_params(axis='x', labelrotation=90, labelfontfamily="tahoma")
    #     subplot.plot(x, y)

    #     buffer = BytesIO()
    #     figure.savefig(buffer, format="png")
    #     img = openpyxl.drawing.image.Image(buffer)
    #     sheet.add_image(img, f"A{len(profile1) + 5}")

    #     align = openpyxl.styles.Alignment(horizontal="center")

    #     sheet.merge_cells("A1:C1")
    #     sheet["A1"].value = "โปรไฟล์ที่หนึ่ง"
    #     sheet["A1"].alignment = align
    #     sheet.merge_cells("D1:F1")
    #     sheet["D1"].value = "โปรไฟล์ที่สอง"
    #     sheet["D1"].alignment = align
    #     sheet.merge_cells("G1:I1")

    #     data = profile1 + profile2

    #     for row_index, row in enumerate(data):
    #         for col_index, value in enumerate(row):
    #             sheet.cell(row=row_index + 2, column=col_index + 1, value=value)

    #     file_path = filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[("ไฟล์ Excel", "*.xlsx")])

    #     if file_path:
    #         wb.save(file_path) 
    #         print(f"บันทึกไฟล์ที่: {file_path}")
    #     else:
    #         print("การบันทึกไฟล์ถูกยกเลิก")
        

    
    
