# Generated by Django 5.2 on 2025-04-26 17:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0003_alter_product_options_alter_product_country_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='number_of_ratings',
            field=models.IntegerField(default=0),
        ),
    ]
