from django.shortcuts import render
from view.views import BaseRedirectView


class OrderView(BaseRedirectView):
    def handle(self, request, *args, **kwargs):
        if request.session.get('user'):
            # 订单界面
            pass
        else:
            # 登录界面
            self.redirect_url = '/user/login/'
