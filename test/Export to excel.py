import pandas as pd
import tkinter as tk
from tkinter import filedialog

# ตัวอย่างข้อมูลใน DataFrame
data = {
    'ชื่อ': ['สมชาย', 'สมหญิง', 'สมศรี'],
    'อายุ': [25, 30, 22],
    'อาชีพ': ['นักเรียน', 'ครู', 'แพทย์']
}
df = pd.DataFrame(data)
print(df)

# ฟังก์ชันสำหรับเปิดหน้าต่างเลือกไฟล์
def save_file_dialog():
    root = tk.Tk()
    root.withdraw()  # ซ่อนหน้าต่างหลักของ tkinter

    # เปิดหน้าต่างเลือกไฟล์ และกำหนดประเภทไฟล์เป็น Excel
    file_path = filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[("Excel files", "*.xlsx")])

    return file_path

# รับตำแหน่งที่ต้องการบันทึกไฟล์จากผู้ใช้
file_path = save_file_dialog()

# บันทึก DataFrame ไปยังไฟล์ Excel
if file_path:
    df.to_excel(file_path, index=False)
    print(f"บันทึกไฟล์ที่: {file_path}")
else:
    print("การบันทึกไฟล์ถูกยกเลิก")
