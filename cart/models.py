from django.db import models
from goods.models import *
# Create your models here.


class CartItemManager(models.Model):
    """过滤掉已经删除的商品"""
    def all(self):
        return super(CartItem, self).all().filter(isdelete=False)


class CartItem(models.Model):
    """购物项"""
    goodsid = models.IntegerField()
    colorid = models.IntegerField()
    sizeid = models.IntegerField()
    count = models.IntegerField()
    isdelete = models.BooleanField(default=False)
    objects = CartItemManager()

    def goods(self):
        return Goods.objects.get(id=self.goodsid)

    def color(self):
        return Color.objects.get(id=self.colorid)

    def size(self):
        return Size.objects.get(id=self.sizeid)

    def all_price(self):
        return self.goods().gprice * (int(self.count))





