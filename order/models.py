from django.db import models
from userview.models import UserDetails
from home.models import Booking
from home.models import Package


# Create your models here.
class Payment(models.Model):
    razorpay_payment_id = models.CharField(max_length=100,blank=True,null=True)
    user = models.ForeignKey(UserDetails,on_delete=models.CASCADE)
    package = models.ForeignKey(Package,on_delete=models.CASCADE)
    booking = models.ForeignKey(Booking,on_delete=models.CASCADE)
    amount_paid = models.CharField(max_length=100,null=True)

    