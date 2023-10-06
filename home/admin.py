from django.contrib import admin
from .models import Category, Package,Variation,VechileType,Slot,Booking,Coupon


# Register your models here.
admin.site.register(Category)
admin.site.register(Package)
class okay(admin.ModelAdmin):
    list_display = ('id',)
admin.site.register(Variation,okay)
admin.site.register(VechileType)
admin.site.register(Slot)
admin.site.register(Booking)
admin.site.register(Coupon)



