import pandas as pd
import os
import django
import random
from pathlib import Path

# 设置 Django 环境
BASE_DIR = Path(__file__).resolve().parent
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecommerce.settings')
django.setup()

from products.models import Product

# 读取 Red.xlsx 文件
excel_file_path = BASE_DIR / 'data' / 'Red.xlsx'
df = pd.read_excel(excel_file_path)

# 遍历每一行并导入数据
for index, row in df.iterrows():
    # 处理 Year 字段（可能包含 "N.V."）
    year = row['Year']
    if str(year).strip().upper() == 'N.V.':
        year = None
    else:
        year = int(year)

    # 创建 Product 记录
    Product.objects.create(
        name=row['Name'],
        country=row['Country'],
        region=row['Region'],
        winery=row['Winery'],
        rating=float(row['Rating']),
        number_of_ratings=int(row['NumberOfRatings']),  # 确保导入此字段
        price=float(row['Price']),
        year=year,
        inventory=random.randint(0, 100)  # 随机生成 0-100 的库存
    )

print("Data import completed successfully!")