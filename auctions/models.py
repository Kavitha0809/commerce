from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Category(models.Model):
    name = models.CharField(max_length=64)

    def __str__(self):
        return self.name


class AuctionListing(models.Model):  # ✅ Changed class name to follow naming conventions
    title = models.CharField(max_length=64)
    description = models.TextField()
    price = models.DecimalField(default=200, max_digits=10, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, blank=True, null=True)  # ✅ Removed max_length
    image_url = models.URLField(blank=True) 
    is_active = models.BooleanField(default=True)  # ✅ Changed "Is_active" to "is_active" (PEP8)
    created_at = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)  # ✅ Changed "Owner" to "owner" (PEP8)
    watchlisted_by = models.ManyToManyField(User, related_name="watchlist", blank=True)
   
    def __str__(self):
        return f"{self.title} : {self.description}"
    

class Bids(models.Model): 
    auction = models.ForeignKey(AuctionListing, related_name="bids", on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    bid_amount = models.DecimalField(max_digits=10, decimal_places=2)
    bid_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.first_name} bid on {self.auction.title} with {self.bid_amount}"


class Comments(models.Model):
    auction = models.ForeignKey(AuctionListing, related_name="comments", on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.first_name} commented on {self.auction.title}: {self.content}"
