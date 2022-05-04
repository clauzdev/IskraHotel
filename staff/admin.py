from django.contrib import admin
from django.contrib.admin import ModelAdmin
from staff.models import Schedules, Products, Transporters, Deliveries
# Register your models here.
# class staffAdmin(ModelAdmin):
#     list_display = (
#         '__str__',)


class SchedulesAdmin(ModelAdmin):
    list_display = (
        '__str__','time',)

class ProductsAdmin(ModelAdmin):
    list_display = (
        '__str__',)

class TransportersAdmin(ModelAdmin):
    list_display = (
        '__str__',)

class DeliveriesAdmin(ModelAdmin):
    list_display = (
        'product','count','date','transporter',)



# admin.site.register(staff, staffAdmin)
admin.site.register(Schedules, SchedulesAdmin)
admin.site.register(Products, ProductsAdmin)
admin.site.register(Transporters, TransportersAdmin)
admin.site.register(Deliveries, DeliveriesAdmin)