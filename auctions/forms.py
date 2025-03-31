from django import forms
from .models import AuctionListing

class AuctionForm(forms.ModelForm):
    class Meta:
        model = AuctionListing
        fields = ['title','description','price','category','image_url','is_active']
        widgets = {
            'description':forms.Textarea(attrs={'rows':4,'cols':40}),
            'price' : forms.NumberInput(attrs={'step':0.01}),

        }
