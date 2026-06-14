import pandas as pd
import matplotlib.pyplot as plt

# อ่านไฟล์ข้อมูลด้วยpandas
dataset = pd.read_csv('m5python/Aj phoom-my work/work/train.csv')
print(dataset.shape)
print(dataset.head())

# แยก label กับค่าพิกเซล
y_train = dataset['label']
x_train = dataset.drop('label', axis=1)

# ---------- CLEAN DATA ----------
print("\n Cleaning Data...")

# 1. เช็คว่ามีค่าว่างมั้ย
# ใช้ .isnull().sum() เพื่อหาจำนวนช่องที่เป็นค่าว่างในแต่ละคอลัมน์
missing_values = dataset.isnull().sum()
missing_total = missing_values.sum()

if missing_total > 0: # ถ้ามีค่าว่าง ให้รายงานจำนวนทั้งหมดและคอลัมน์ที่เจอ
    print(f"\n พบค่าที่หายไป {missing_total} ค่า")
    print(missing_values[missing_values > 0])
else:
    print("\n ไม่มีค่าที่หายไป")

dataset = dataset.dropna()  # ลบแถวที่มีค่าว่างออก

# 2. เช็ค label ให้อยู่ในช่วง 0–9
invalid_labels = dataset[~dataset['label'].isin(range(10))]
if len(invalid_labels) > 0:
    print(f"\n พบ label ที่ไม่อยู่ในช่วง 0–9 จำนวน {len(invalid_labels)} แถว")
    dataset = dataset[dataset['label'].isin(range(10))] # เก็บเฉพาะแถวที่ label ถูกต้อง (0–9)
else:
    print("\n label ถูกต้องทั้งหมด")

# 3. เช็คค่าความสว่างแต่ละพิกเซลให้อยู่ในช่วง 0–255
pixel_columns = dataset.columns.drop('label')

# หาค่าที่เกินหรือออกนอกช่วง
over_255 = (dataset[pixel_columns] > 255)
below_0 = (dataset[pixel_columns] < 0)
# นับจำนวนค่าที่ผิดปกติทั้งหมด
count_over_255 = over_255.sum().sum()
count_below_0 = below_0.sum().sum()

if count_over_255 > 0 or count_below_0 > 0:
    print(f"\n พบค่าพิกเซลผิดปกติ {count_over_255 + count_below_0} ค่า")  # สร้าง mask รวมแถวที่มีค่าผิด
    invalid_rows = over_255.any(axis=1) | below_0.any(axis=1)
    dataset = dataset[~invalid_rows]  # ลบแถวที่มีปัญหา
else:
    print("\n ทุกค่าพิกเซลอยู่ในช่วง 0–255")

# 4. ลบข้อมูลซ้ำ
before = dataset.shape[0]
dataset = dataset.drop_duplicates()
after = dataset.shape[0]
duplicates_removed = before - after
# แสดงจำนวนข้อมูลที่ถูกลบออก
if duplicates_removed > 0:
    print(f"\n ลบข้อมูลซ้ำออก {duplicates_removed} แถว")
else:
    print("\n ไม่มีข้อมูลซ้ำ")

# สรุปผล
print(f"\n ล้างข้อมูลเสร็จเรียบร้อย ขนาดข้อมูลใหม่: {dataset.shape}")

# แยก X, y หลังจาก clean
y_train = dataset['label']
x_train = dataset.drop('label', axis=1)

# แสดงตัวอย่างภาพตัวเลข 0-9 อย่างละภาพ
for i in range(10):
    # ดึงภาพที่มี label เท่ากับ i
    image = dataset.loc[dataset['label'] == i].iloc[0, 1:].values.reshape(28, 28)
    plt.subplot(5, 2, i + 1)
    plt.imshow(image, cmap = 'gray')
    plt.title(f"Label No.{i}")
    plt.axis('off')
 
plt.tight_layout()
plt.show()
