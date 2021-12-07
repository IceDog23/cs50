from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.base import Model
from django.db.models.deletion import CASCADE
from django.db.models.enums import Choices

class User(AbstractUser):
    pass

class Categories (models.Model): 
    category = models.CharField(max_length=64)

    def __str__ (self): 
        return f'{self.category}'

class Listing (models.Model): 
    product_name = models.CharField(max_length=64)
    description = models.CharField(max_length=300, default='Default description') 
    price = models.IntegerField()
    img = models.URLField(blank = True, null = True)
    owner = models.ForeignKey(User, on_delete= models.CASCADE, related_name = 'items')
    category = models.ForeignKey(Categories, on_delete=CASCADE, blank = True, null=True)
    t_create = models.DateTimeField(auto_now_add=True)

    h_bidder = models.ForeignKey(User, blank=True, on_delete=CASCADE, related_name="highest_bidder", null=True)
    h_bid = models.IntegerField(blank=True, null=True, default=0)
    active = models.BooleanField(default='True')

    def __str__ (self): 
        return f'{self.product_name}'

class Bid (models.Model): 
    bid = models.PositiveIntegerField() 
    bidder = models.ForeignKey(User, on_delete=models.CASCADE, related_name = "bids_on_products")
    item = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name='item_bids')

    def __str__ (self): 
        return f'{self.item}: {self.bid}'

class Comment (models.Model):
    title = models.CharField(max_length=64) 
    text = models.CharField(max_length=64)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_comments')
    item = models.ForeignKey(Listing,on_delete=models.CASCADE, related_name='item_comments')

    def __str__ (self): 
        return f'{self.title}: ({self.user})'

class Watchlist (models.Model): 
    item = models.ForeignKey(Listing, on_delete=CASCADE, related_name='on_watchlist')
    user = models.ForeignKey(User, on_delete=CASCADE, related_name='watchlist')
    watched = models.BooleanField(default=False)

    def __str__ (self): 
        return f'{self.user}: ({self.item})'
        