from django.db import models
from utils.commonutils import md

# Create your models here.
class User(models.Model):
    account = models.CharField(unique=True, max_length=20)
    password = models.CharField(max_length=64)

    class RegisterException(Exception):
        pass
    class LoginException(Exception):
        pass

    @staticmethod
    def register(account, password, *args, **kwargs):
        try:
            return User.objects.create(account=account, password=password)
        except Exception as e:
            raise User.RegisterException()

    @staticmethod
    def login(account, password, time, *args, **kwargs):
        import time as t
        current_server = t.time()*1000  # 当前服务器时间
        if not(int(time)>= current_server - 1000*60*10 and int(time)<=current_server):
            return
        try:
            user = User.objects.get(account=account)
            user_password = md(user.password + time)
            if user_password == password:
                return user
            else:
                return None
        except Exception as e:
            raise User.LoginException()


class Address(models.Model):
    province = models.CharField(max_length=10)
    city = models.CharField(max_length=10)
    area = models.CharField(max_length=10)
    details = models.CharField(max_length=520)
    name = models.CharField(max_length=20)
    phone = models.CharField(max_length=11)
    user = models.ForeignKey(User)
    isdelete = models.BooleanField(default=False)
    # 默认收货地址
    isprimary = models.BooleanField(default=False)