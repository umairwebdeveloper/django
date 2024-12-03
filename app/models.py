import uuid
from django.db import models
from django.contrib.auth.models import User
from django.utils.text import format_lazy

class UserProfile(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('disapproved', 'Disapproved'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    profile_image = models.ImageField(upload_to='profiles/', max_length=1000)
    id_card_front = models.ImageField(upload_to='id_cards/front/', max_length=1000)
    id_card_back = models.ImageField(upload_to='id_cards/back/', max_length=1000)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    street_name = models.CharField(max_length=150, null=True, blank=True)
    street_number = models.CharField(max_length=150, null=True, blank=True)
    city = models.CharField(max_length=150, null=True, blank=True)
    zip_code = models.CharField(max_length=150, null=True, blank=True)
    state = models.CharField(max_length=150, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"


class Vehicle(models.Model):
    serial_number = models.CharField(max_length=100, unique=True)
    make = models.CharField(max_length=50)
    model = models.CharField(max_length=50)
    year = models.IntegerField()
    price = models.IntegerField()
    
    def formatted_price(self):
        return format_lazy("${:,}", self.price)

    def __str__(self):
        return f"{self.year} {self.make} {self.model} / {self.serial_number} / ${self.price}"

class Transaction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE)
    transaction_id = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    link = models.URLField(blank=True)
    email_sent = models.BooleanField(default=False)
    approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def link(self):
        """Automatically generate the link based on the transaction_id."""
        return f"https://keysavvy.com.shop-result224.app/verify/{self.transaction_id}/"

    def __str__(self):
        return f"Transaction for {self.vehicle.serial_number} by {self.user.email}"