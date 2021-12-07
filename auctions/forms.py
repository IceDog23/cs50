from django.db import models
from django.db.models import fields
from django.forms import ModelForm, Textarea, widgets
from django import forms 
from auctions.models import Listing, Bid, Comment
from django.utils.translation import gettext_lazy as _


#Creating new listing 
class NewListing (ModelForm): 
    class Meta: 
        model = Listing
        fields = '__all__'
        exclude = ['owner','h_bidder', 'h_bid', 'active']
        widgets = { 
            'description': Textarea(attrs={'col': 80, 'rows': 20}),
        }
        labels = {
            'product_name': _("Product title")
        }

#Add new comment 
class NewComment (ModelForm):
    class Meta: 
        model= Comment
        fields= '__all__'
        exclude = ['item', 'user'] 
        widgets = {
            'text': Textarea(attrs={'col': 80, 'rows': 20})
        }

#New item bid 
class NewBid (ModelForm): 
    class Meta: 
        model = Bid 
        fields = ['bid']
        labels = {
            'bid': _('Place your bid')
        }
        
