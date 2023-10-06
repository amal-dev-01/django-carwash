from django.db import models
from userview.models import UserDetails

# Create your models here.


class Category(models.Model):
    name=models.CharField(max_length=50)
    
    def __str__(self):
        return self.name
    
class VechileType(models.Model):
    vechile_type = models.CharField(max_length=100)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    def __str__(self):
        return self.vechile_type
    
class Package(models.Model):
    name = models.CharField(max_length=100)
    # category = models.ForeignKey(Category, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.name
    
class Variation(models.Model):
    vechile_type = models.ForeignKey(VechileType, on_delete=models.CASCADE)
    package = models.ForeignKey(Package, on_delete=models.CASCADE)
    price = models.CharField(max_length=100)
    
    def __str__(self):
        return f"{self.vechile_type},{self.package}"


# class (models.Model):
#     date = models.DateField()
#     start_time = models.TimeField()
#     end_time = models.TimeField()
#     is_booked = models.BooleanField(default=False)


class Slot(models.Model):
    TIMESLOT_LIST = (
        (0, '09:00 – 09:30'),
        (1, '10:00 – 10:30'),
        (2, '11:00 – 11:30'),
        (3, '12:00 – 12:30'),
        (4, '13:00 – 13:30'),
        (5, '14:00 – 14:30'),
        (6, '15:00 – 15:30'),
        (7, '16:00 – 16:30'),
    )
    date = models.DateField(null=True, blank=True)
    timeslot = models.IntegerField(choices=TIMESLOT_LIST, null=True, blank=True)
    variation = models.ForeignKey(Variation, on_delete=models.CASCADE)
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.date}{self.timeslot}"
    
    
 
class Booking(models.Model):
    user = models.ForeignKey(UserDetails, on_delete=models.CASCADE)
    slot = models.ForeignKey(Slot, on_delete=models.CASCADE,unique=False)
    variation = models.ForeignKey(Variation, on_delete=models.CASCADE)
    price = models.PositiveIntegerField()
    is_paid= models.BooleanField(default=False)
    is_ordered = models.BooleanField(default=False)
    is_canceled = models.BooleanField(default=False)
    
    def __str__(self):
            return f"{self.user}{self.slot}"


class Coupon(models.Model):
    code = models.CharField(max_length=20, unique=True)
    discount_percentage = models.PositiveIntegerField()
    valid_for_first_login = models.BooleanField(default=True)
    used = models.BooleanField(default=False)  


    def __str__(self):
        return self.code



        
        
        
        
        