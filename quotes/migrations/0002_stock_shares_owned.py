# Generated by Django 3.1.3 on 2020-11-24 18:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quotes', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='stock',
            name='shares_owned',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
