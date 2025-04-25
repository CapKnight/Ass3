from django.core.management.base import BaseCommand
from products.models import Product
import pandas as pd

class Command(BaseCommand):
    help = 'Import products from XLSX file with custom columns'

    def add_arguments(self, parser):
        parser.add_argument('file_path', type=str, help='Path to the XLSX file')

    def handle(self, *args, **kwargs):
        file_path = kwargs['file_path']
        try:
            df = pd.read_excel(file_path, engine='openpyxl')
            
            # 遍历每一行数据并映射字段
            for index, row in df.iterrows():
                Product.objects.create(
                    name=row['Name'],                   # Name
                    country=row['Country'],              # Country
                    region=row['Region'],                # Region
                    winery=row['Winery'],                # Winery
                    rating=row['Rating'],               # Rating
                    price=row['Price'],                  # Price
                    year=row['Year'],                    # Year
                    inventory=row['Inventory'],          # Inventory
                )
            
            self.stdout.write(self.style.SUCCESS(f'成功导入 {len(df)} 条商品数据'))
        
        except KeyError as e:
            self.stdout.write(self.style.ERROR(f'列名错误：{e}，请检查XLSX文件列名是否一致'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'错误：{str(e)}'))