from django.shortcuts import render
from view.views import BaseRedirectView,BaseView
from utils.cartutils import *


class CartView(BaseRedirectView):
    """添加购物项，重定向到购物车界面"""
    redirect_url = '/cart/cart.html'
    def handle(self, request, *args, **kwargs):
        # 处理业务逻辑（添加购物项）
        request.session.modified = True  # session存储机制问题
        cart_manager = SessionCartManager(request.session)
        cart_manager.add_cart_item(**request.POST.dict())

class CartListView(BaseView):
    template_name = 'cart.html'

    def get_extra_context(self, request):
        cart_manager = SessionCartManager(request.session)
        return {'cartItems': cart_manager.get_all_cart_items()}