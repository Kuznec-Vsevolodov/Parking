from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import PermissionsMixin
from django.utils import timezone

class Place(models.Model):
    title = models.CharField(max_length=200)
    address = models.CharField(max_length=300)
    general_scheme = models.ImageField()
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

class Event(models.Model):
    place = models.ForeignKey(Place, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField()
    event_day = models.DateField()
    event_cover = models.ImageField()

    def __str__(self):
        return self.title

class Sector(models.Model):
    title = models.CharField(max_length=200)
    size = models.SmallIntegerField()
    place = models.ForeignKey(Place, on_delete=models.CASCADE)
    rows = models.SmallIntegerField()
    columns = models.SmallIntegerField()
    description = models.TextField()
    price = models.SmallIntegerField()

    def __str__(self):
        return self.title

class ParkingPlace(models.Model):
    row = models.SmallIntegerField()
    column = models.SmallIntegerField()
    sector_id = models.ForeignKey(Sector, on_delete=models.CASCADE)

class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    parking_place = models.ForeignKey(ParkingPlace, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)

class Wallet(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    wallet = models.SmallIntegerField()

class UserType(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_owner = models.BooleanField()