import pandas as pd
import os
import django
import random
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecommerce.settings')
django.setup()

from products.models import Product

excel_file_path = BASE_DIR / 'data' / 'Red.xlsx'
df = pd.read_excel(excel_file_path)

for index, row in df.iterrows():
    year = row['Year']
    if str(year).strip().upper() == 'N.V.':
        year = None
    else:
        year = int(year)

    Product.objects.create(
        name=row['Name'],
        country=row['Country'],
        region=row['Region'],
        winery=row['Winery'],
        rating=float(row['Rating']),
        number_of_ratings=int(row['NumberOfRatings']), 
        price=float(row['Price']),
        year=year,
    )

print("Data import completed successfully!")