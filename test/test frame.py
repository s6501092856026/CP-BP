import seaborn as sns
import pandas as pd

# สร้าง DataFrame จากข้อมูลที่มีอยู่
data = {
    'Profile': [profile1]*len(x_values_1) + [profile2]*len(x_values_2), 
    'Name': x_values_1 + x_values_2,
    'Carbon Emission': y_values_1 + y_values_2
}

df = pd.DataFrame(data)

# สร้างกราฟโดยใช้ Seaborn
sns.barplot(x='Profile', y='Carbon Emission', hue='Name', data=df)

# แสดงกราฟ
plt.show()
