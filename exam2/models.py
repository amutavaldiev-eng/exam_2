from django.db import models
from django.contrib.auth.models import AbstractUser
from datetime import datetime

class CustomUser(AbstractUser):
    photo = models.ImageField(upload_to="profiles/")
    phone = models.CharField(max_length=20)
    about = models.TextField()
    


class Category(models.Model):
    name = models.CharField(max_length=100)
    players_count = models.PositiveIntegerField()
    def __str__(self):
        return self.name

class Field(models.Model):
    name = models.CharField(max_length=150)
    address = models.CharField(max_length=255)
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    photo = models.ImageField(upload_to="fields/")
    is_free = models.BooleanField(default=True)
    def __str__(self):
        return self.name




class Booking(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    field = models.ForeignKey(Field, on_delete=models.CASCADE)
    has_team = models.BooleanField(default=False)
    players_needed = models.PositiveIntegerField()
    status = models.CharField(max_length=20, default="active")
    created_at = models.DateTimeField(default=datetime.now)
    def __str__(self):
        return self.name


class Participant(models.Model):
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    joined_at = models.DateTimeField(default=datetime.now)