# Generated by Django 3.2.7 on 2021-09-27 05:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sport', '0004_alter_player_email'),
    ]

    operations = [
        migrations.AddField(
            model_name='player',
            name='dob',
            field=models.DateField(null=True),
        ),
        migrations.AlterField(
            model_name='player',
            name='mobile',
            field=models.BigIntegerField(),
        ),
    ]
