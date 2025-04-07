from django.db import models
from django.contrib.auth.models import AbstractUser, PermissionsMixin, BaseUserManager
from django.conf import settings
from django.utils import timezone


    

class CustomUserManager(BaseUserManager):
    def _create_user(self, phone_number, password=None, **extra_fields):
        if not phone_number:
            raise ValueError('The Phone Number must be set')
        phone_number = phone_number.strip() # Cleaning
        user = self.model(phone_number=phone_number, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_user(self,phone_number=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(phone_number, password, **extra_fields)


    def create_superuser(self, phone_number, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(phone_number, password, **extra_fields)



class CustomUser(AbstractUser, PermissionsMixin):
    username = None
    phone_number = models.CharField(max_length=15, unique=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30, blank=True, null=True)
    email = models.EmailField(blank=True, default='',unique=True)
    liked_cars = models.ManyToManyField('Car', related_name='liked_by', blank=True)

    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    date_joined = models.DateTimeField(default=timezone.now)
    last_login = models.DateTimeField(blank=True, null=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def __str__(self):
        return self.phone_number
    


class Car(models.Model):
    
    TRANSMISSION_CHOICES = [
        ('manual', 'Manual'),
        ('automatic', 'Automatic'),
        ('tiptronic', 'Tiptronic')
    ]
    brand = models.CharField(max_length=25)
    model = models.CharField(max_length=25)
    year = models.PositiveSmallIntegerField()
    daily_rental_price = models.DecimalField(max_digits=7, decimal_places=2)
    capacity = models.SmallIntegerField()
    transmission = models.CharField(max_length=10, choices=TRANSMISSION_CHOICES)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    city = models.CharField(max_length=30)
    fuel_tank = models.PositiveIntegerField()
    image1 = models.ImageField(upload_to='car_images/')
    image2 = models.ImageField(upload_to='car_images/', blank=True, null=True)
    image3 = models.ImageField(upload_to='car_images/', blank=True, null=True)


    def __str__(self):
        return f"{self.brand} {self.model} ({self.year})"
    



class Rental(models.Model):
    renter = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    car = models.ForeignKey('Car', on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    total_price = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True)

    def days(self):
        return max(1, (self.end_date - self.start_date).days)  # Ensure at least 1 day is charged

    def save(self, *args, **kwargs):
        if self.start_date and self.end_date:
            self.total_price = self.days() * self.car.daily_rental_price  # Auto-calculate total price
        super().save(*args, **kwargs)

    class Meta:
        ordering = ['-start_date']

    def __str__(self):
        return f"{self.renter.first_name} rented {self.car.brand} {self.car.model}"