# Generated by Django 3.2.7 on 2021-12-18 02:59

from django.db import migrations, models
import sport.models


class Migration(migrations.Migration):

    dependencies = [
        ('sport', '0019_auto_20211218_0258'),
    ]

    operations = [
        migrations.AlterField(
            model_name='daily_scan',
            name='scan_date',
            field=models.DateField(default=sport.models.get_cst_date),
        ),
    ]
