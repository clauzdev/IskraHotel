# Generated by Django 4.0 on 2022-04-02 12:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0003_alter_customer_photo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='photo',
            field=models.ImageField(upload_to='customer_photo'),
        ),
    ]
