# Generated by Django 4.0 on 2021-12-19 20:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0002_alter_user_first_name'),
        ('staff', '0010_alter_schedules_staff'),
    ]

    operations = [
        migrations.AlterField(
            model_name='schedules',
            name='staff',
            field=models.ForeignKey(limit_choices_to={'groups': 3}, on_delete=django.db.models.deletion.CASCADE, related_name='staff', to='authentication.user'),
        ),
    ]
