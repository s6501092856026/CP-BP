import tkinter as tk

def calculate_footprint():
    # ฟังก์ชันนี้จะทำการคำนวณ carbon footprint ตามที่ต้องการ

    # ในที่นี้คุณสามารถเขียนโค้ดเพิ่มเติมเพื่อทำการคำนวณ carbon footprint ได้

    # ตัวอย่างการคำนวณ
    # ค่าการใช้พลังงาน
    electricity = float(entry_electricity.get())
    transportation = float(entry_transportation.get())
    waste = float(entry_waste.get())

    # ปริมาณ carbon footprint
    carbon_footprint = electricity + transportation + waste

    # แสดงผลใน Label
    lbl_result.config(text=f"Carbon Footprint: {carbon_footprint} tons CO2e")

# สร้างหน้าต่างหลัก
root = tk.Tk()
root.title("Carbon Footprint Calculator")

# สร้าง Label และ Entry สำหรับใส่ข้อมูล
lbl_electricity = tk.Label(root, text="Electricity usage (tons CO2e):")
lbl_electricity.pack()
entry_electricity = tk.Entry(root)
entry_electricity.pack()

lbl_transportation = tk.Label(root, text="Transportation (tons CO2e):")
lbl_transportation.pack()
entry_transportation = tk.Entry(root)
entry_transportation.pack()

lbl_waste = tk.Label(root, text="Waste (tons CO2e):")
lbl_waste.pack()
entry_waste = tk.Entry(root)
entry_waste.pack()

# สร้างปุ่มคำนวณ
btn_calculate = tk.Button(root, text="Calculate", command=calculate_footprint)
btn_calculate.pack()

# Label สำหรับแสดงผลลัพธ์
lbl_result = tk.Label(root, text="")
lbl_result.pack()

# เริ่มต้นโปรแกรม
root.mainloop()
