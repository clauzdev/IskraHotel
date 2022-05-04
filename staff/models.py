from django.db import models
from rooms import models as rooms
from authentication.models import User
# Create your models here.
# post_choices = (
#     ('горничная', 'Горничная'),
#     ('администратор', 'Администратор'),
#     ('менеджер', 'Менеджер'),
#     ('директор', 'Директор')
# )

# class staff(models.Model):
#     fio = models.CharField(max_length=50, verbose_name='FIO')
#     phone_no = models.CharField(max_length=12, verbose_name='Phone No')
#     post = models.CharField(max_length=20, verbose_name='Post', choices=post_choices)
#     passport_no = models.CharField(max_length=10, blank=True)

#     # oshibka = Schedules.objects.filter(staff = f'{self.post} {self.fio}').count()
#     # oshibok = models.CharField(default=f'{oshibka}')
#     def __str__(self):
#         return f'{self.post} {self.fio}'

class Schedules(models.Model):
    room_no = models.ForeignKey(rooms.Room, related_name='rooms', on_delete=models.CASCADE)
    date = models.DateField()
    time = models.TimeField()
    staff = models.ForeignKey(User, limit_choices_to={'groups': 3}, related_name='staff', on_delete=models.CASCADE)
    is_done = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.room_no} {self.date}'

class Products(models.Model):
    product = models.CharField(max_length=50, verbose_name='products')

    def __str__(self):
        return f'{self.product}'

class Transporters(models.Model):
    transporter = models.CharField(max_length=50, verbose_name='transportername')

    def __str__(self):
        return f'{self.transporter}'

class Deliveries(models.Model):
    product = models.ForeignKey(Products, related_name='products', on_delete=models.CASCADE)
    count = models.IntegerField()
    date = models.DateField()
    transporter = models.ForeignKey(Transporters, related_name='transporters', on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.product} {self.date}'