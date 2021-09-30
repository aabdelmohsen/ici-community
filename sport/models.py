from django.db import models
from django.utils import timezone

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
    qr_code = models.CharField(max_length=1000, null=True)
    disclaimer = models.BooleanField(default=False)
    def __str__(self):
        return self.first_name + ' ' + self.last_name
