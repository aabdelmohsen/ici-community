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
import uuid
import os

def rename_profile_image(instance, filename):
    print('Original file name :::::::::::::: {}'.format(filename))
    new_file_name = '{}-{}.png'.format(instance.first_name, uuid.uuid4())
    print('new file name :::::::::::::: {}'.format(new_file_name))
    return new_file_name


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
    profile_picture = models.ImageField(default='', upload_to=rename_profile_image)
    registeration_date = models.DateTimeField(default=timezone.now)
    qr_code = models.ImageField(default='')
    disclaimer = models.BooleanField(default=False)

    def __str__(self):
        return str(self.id) + ' ::: ' + self.first_name + ' ::: ' + self.last_name + ' ::: ' + str(self.mobile)





class Daily_Scan(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    scan_date = models.DateField(default=date.today)
    scan_timestamp = models.DateTimeField(default=timezone.now)
    