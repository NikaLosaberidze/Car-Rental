from django.contrib import admin
from .models import CustomUser, Car, Rental

admin.site.register(CustomUser)
admin.site.register(Car)
admin.site.register(Rental)