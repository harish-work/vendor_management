from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class CustomUser(AbstractUser):
    fname = models.CharField(max_length=30,null=False)
    lname = models.CharField(max_length=30,null=False)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=10,null=False,blank=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['fname','lname','password']

    def get_username(self):
        return self.email


class Vendor(models.Model):
    name = models.CharField(max_length=30,null=False)
    contact_details = models.TextField(max_length=10)
    address = models.TextField(max_length=200)
    vendor_code = models.CharField(max_length=20,unique=True,null=False)
    on_time_delivery_rate = models.FloatField()
    quality_rating_avg = models.FloatField()
    average_reponse_time = models.FloatField()
    fullfillment_rate = models.FloatField()

    def __str__(self):
        return self.name


class PurchaseOrder(models.Model):
    po_number = models.CharField(max_length=20,unique=True)
    vendor = models.ForeignKey(Vendor,on_delete=models.CASCADE)
    order_date = models.DateTimeField(auto_now=True)
    delivery_date = models.DateTimeField()
    items = models.JSONField(default=dict,null=False)
    quantity = models.IntegerField()
    status = models.CharField(max_length=30)
    quality_rating = models.FloatField(null=True)
    issue_date = models.DateTimeField(auto_created=True)
    acknowledgment_date = models.DateTimeField(null=True)

    def __str__(self):
        return self.po_number


class HistoricalPerformance(models.Model):
    vendor = models.ForeignKey(Vendor,on_delete=models.CASCADE)
    date = models.DateTimeField()
    on_time_delivery_rate = models.FloatField()
    quality_rating_avg = models.FloatField()
    average_reponse_time =models.FloatField()
    fullfillment_rate = models.FloatField()

    def __str__(self):
        return self.vendor