from django.db import models
from user.models import User

class Order(models.Model):
    # 订单号，给程序看
    sign = models.CharField(max_length=120)
    # 订单编号，给客户看
    order = models.CharField(max_length=120)
    user = models.ForeignKey(User)
    # 收货人相关信息
    name = models.CharField(max_length=20)
    phone = models.CharField(max_length=11)
    address = models.CharField(max_length=120)
    # 订单项
    orderitems = models.CharField(max_length=520)
    creeated = models.DateTimeField(auto_now_add=True)
    payway = models.CharField(max_length=10)
    status = models.CharField(max_length=20, default='待支付')
    trade_no = models.CharField(max_length=120, null=True, blank=True)

