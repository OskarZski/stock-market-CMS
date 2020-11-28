# Generated by Django 3.1.3 on 2020-11-26 12:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quotes', '0003_stock_currency_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='stock',
            name='shares_owned',
            field=models.DecimalField(decimal_places=5, default=0, max_digits=10),
        ),
    ]
