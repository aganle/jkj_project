from django.db import models

# Create your models here.

class CartItem(models.Model):
    """购物项"""
    goodsid = models.IntegerField()
    colorid = models.IntegerField()
    sizesid = models.IntegerField()
    count = models.IntegerField()