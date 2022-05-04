# Generated by Django 3.0.6 on 2020-05-10 18:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('rooms', '0005_auto_20200510_1758'),
        ('customer', '0002_auto_20200510_1717'),
    ]

    operations = [
        migrations.CreateModel(
            name='Booking',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('booking_id', models.CharField(max_length=32)),
                ('booking_date', models.DateTimeField(auto_now_add=True)),
                ('check_in_date', models.DateField()),
                ('check_out_date', models.DateField()),
                ('paid', models.BooleanField(default=False)),
                ('booked', models.BooleanField(default=False)),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='booking', to='customer.Customer')),
                ('room', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='booking', to='rooms.Room')),
            ],
        ),
    ]
