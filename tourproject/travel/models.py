from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User
from datetime import timedelta, date

class Package(models.Model):
    vendor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='vendor_packages')
    title = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    duration_days = models.IntegerField()
    destination = models.CharField(max_length=100)
    image = models.ImageField(upload_to='package_images/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    auto_expiry_days = models.IntegerField(default=30)
    approved = models.BooleanField(default=False)

    def is_expired(self):
        return date.today() > self.created_at.date() + timedelta(days=self.auto_expiry_days)

    def __str__(self):
        return self.title

class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookings')
    package = models.ForeignKey(Package, on_delete=models.CASCADE)
    booked_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=[('Pending', 'Pending'), ('Confirmed', 'Confirmed')], default='Pending')

    def __str__(self):
        return f"{self.user.username} - {self.package.title}"
