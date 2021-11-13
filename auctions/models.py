from typing import List
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.base import Model


class User(AbstractUser):
    pass
    
class Listing (models.Model): 
    product_name = models.CharField(max_length=64)
    price = models.IntegerField()
    owner = models.ForeignKey(User, on_delete= models.CASCADE, related_name = 'items')

    def __str__ (self): 
        return f'{self.product_name}'


class Bid (models.Model): 
    bid = models.IntegerField() 
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


class Wishlist (models.Model): 
    item = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name='on_wishlist')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="wished_items")

    def __str__ (self): 
        return f'{self.item} - ({self.user})'