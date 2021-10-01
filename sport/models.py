from django.db import models
from django.utils import timezone
from datetime import date
import barcode
from barcode.writer import ImageWriter
from io import BytesIO
from django.core.files import File
import qrcode
import qrcode.image.svg
import base64

class Player(models.Model):
    first_name = models.CharField(max_length=250)
    last_name = models.CharField(max_length=250)
    mobile = models.BigIntegerField()
    address = models.CharField(max_length=300)
    email = models.EmailField(max_length=250)
    CHOICES = [('Male', 'Male'), ('Female', 'Female')]
    gender = models.CharField(max_length=10, choices=CHOICES, default='Male')
    date_of_birth = models.DateField(null=True)
    vaccinated = models.BooleanField(default=False)
    emergency_contact_name = models.CharField(max_length=250)
    emergency_contact_phone = models.CharField(max_length=100)
    profile_picture = models.ImageField(default='')
    registeration_date = models.DateTimeField(default=timezone.now)
    qr_code = models.ImageField(default='')
    disclaimer = models.BooleanField(default=False)

    def __str__(self):
        return self.first_name + ' :::: ' + self.last_name





class Daily_Scan(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    scan_date = models.DateField(default=date.today)
    scan_timestamp = models.DateTimeField(default=timezone.now)
    