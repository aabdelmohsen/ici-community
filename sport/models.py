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
    Q_CHOICES = [('Yes', 'Yes'), ('No', 'No')]
    # plus21 = models.BooleanField(default=False)
    plus21 = models.CharField(max_length=10, choices=Q_CHOICES, default='No')
    date_of_birth = models.DateField(null=True, blank=True)
    vaccinated = models.CharField(max_length=10, choices=Q_CHOICES, default='No')
    # vaccinated = models.BooleanField(default=False)
    emergency_contact_name = models.CharField(max_length=250)
    emergency_contact_phone = models.CharField(max_length=100)
    profile_picture = models.ImageField(default='', upload_to=rename_profile_image)
    registeration_date = models.DateTimeField(default=timezone.now)
    qr_code = models.CharField(max_length=20)
    disclaimer = models.BooleanField(default=False)

    def __str__(self):
        return 'ID: ' + str(self.id) + '  :::::  First Name: ' + self.first_name + '  :::::  Last Name: ' + self.last_name + '  :::::  Mobile: ' + str(self.mobile)

    def clean_date_of_birth(self):
        bdate = self.cleaned_data['date_of_birth']
        if self.plus21 == 'on':
            return null
        else:
            return bdate




class Daily_Scan(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    scan_date = models.DateField(default=date.today)
    scan_timestamp = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return 'ID: ' + str(self.player.id) + '  :::::  First Name: ' + self.player.first_name + '  :::::  Last Name: ' + self.player.last_name + '  :::::  Scan Date: ' + str(self.scan_date)

    