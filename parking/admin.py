from django.contrib import admin
from .models import Place, Event, Sector, ParkingPlace, Booking
# Register your models here.

admin.site.register(Place)
admin.site.register(Event)
admin.site.register(Sector)
admin.site.register(ParkingPlace)
admin.site.register(Booking)