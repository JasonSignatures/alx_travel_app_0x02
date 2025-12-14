from django.db import models
from django.conf import settings
from django.utils import timezone
from django.contrib.auth.models import User

class Listing(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    location = models.CharField(max_length=255)
    price_per_night = models.DecimalField(max_digits=8, decimal_places=2)
    host = models.ForeignKey(User, on_delete=models.CASCADE, related_name='listings')
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.title


class Booking(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name='bookings')
    guest = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookings')
    start_date = models.DateField()
    end_date = models.DateField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.guest.username} - {self.listing.title}"


class Review(models.Model):
    booking = models.OneToOneField(Booking, on_delete=models.CASCADE, related_name='review')
    rating = models.IntegerField()
    comment = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Review for {self.booking.listing.title} by {self.booking.guest.username}"

#Payment model referencing a book model while adapting a foreignkey if the bookimn models differs
class Payment(models.Model):
    STATUS_PENDING = "pending"
    STATUS_COMPLETED = "completed"
    STATUS_FAILED = "failed"
    STATUS_CHOICES = [
        (STATUS_PENDING, "Pending"),
        (STATUS_COMPLETED, "Completed"),
        (STATUS_FAILED, "Failed"),
    ]

    booking = models.ForeignKey(
        "Booking",  # change to your Booking model name or 'auth.User' if needed
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="payments"
    ) 
    
    booking_reference = models.CharField(max_length=128, blank=True, null=True)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    currency = models.CharField(max_length=8, default="ETB")
    tx_ref = models.CharField(max_length=128, unique=True)  # our unique tx_ref
    chapa_ref = models.CharField(max_length=128, blank=True, null=True)  # chapa internal ref_id
    chapa_checkout_url = models.URLField(max_length=512, blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_PENDING)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    customer_email = models.EmailField(max_length=254, blank=True, null=True)
    customer_first_name = models.CharField(max_length=128, blank=True, null=True)
    customer_last_name = models.CharField(max_length=128, blank=True, null=True)
 
    def __str__(self):
        return f"{self.tx_ref} - {self.status}"
