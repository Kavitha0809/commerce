from django.contrib import admin
from .models import User,AuctionListing,Bids,Comments,Category
# Register your models here.

admin.site.register(AuctionListing)
admin.site.register(Bids)
admin.site.register(Comments)
admin.site.register(User)
admin.site.register(Category)
