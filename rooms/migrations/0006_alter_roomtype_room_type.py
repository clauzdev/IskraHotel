# Generated by Django 4.0 on 2021-12-19 19:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rooms', '0005_auto_20200510_1758'),
    ]

    operations = [
        migrations.AlterField(
            model_name='roomtype',
            name='room_type',
            field=models.CharField(choices=[('эконом', 'Эконом номер'), ('комфортный', 'Комфортный номер'), ('полулюкс', 'Полулюкс номер'), ('люкс', 'Люксовый номер')], max_length=32),
        ),
    ]