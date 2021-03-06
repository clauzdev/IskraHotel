from django.db import models

room_type_choices = (
    ('эконом', 'Эконом номер'),
    ('комфортный', 'Комфортный номер'),
    ('полулюкс', 'Полулюкс номер'),
    ('люкс', 'Люксовый номер')
)


class RoomType(models.Model):
    room_type = models.CharField(max_length=32, choices=room_type_choices)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    maximum_capacity = models.IntegerField()
    size = models.IntegerField()
    view = models.CharField(max_length=32)
    bed_number = models.IntegerField()
    ratings = models.DecimalField(max_digits=2, decimal_places=1)
    photo = models.ImageField(upload_to='static/base/images/', default='static/base/images/room-1.jpg')

    def __str__(self):
        return self.room_type.capitalize()


class Room(models.Model):
    room_no = models.CharField(max_length=10)
    room_type = models.ForeignKey(RoomType, related_name='rooms', on_delete=models.CASCADE)
    available = models.BooleanField()

    def __str__(self):
        return f'{self.room_type} {self.room_no}'
