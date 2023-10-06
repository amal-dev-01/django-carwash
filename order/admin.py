from django.contrib import admin
from .models import Payment

# Register your models here.
class okay(admin.ModelAdmin):
    list_display = ('id',)

admin.site.register(Payment,okay)
