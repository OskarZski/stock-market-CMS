# Generated by Django 3.1.3 on 2020-11-26 12:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quotes', '0004_auto_20201126_1239'),
    ]

    operations = [
        migrations.AlterField(
            model_name='stock',
            name='shares_owned',
            field=models.PositiveIntegerField(default=0),
        ),
    ]