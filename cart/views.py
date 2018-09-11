from django.shortcuts import render
from view.views import BaseRedirectView, BaseView, OperateView
from utils.cartutils import *
from django import forms


class MyForm(forms.Form):
    """利用form表单对提交的数据进行数据清洗，防止向数据库中加入无效的数据"""
    goodsid = forms.IntegerField()
    colorid = forms.IntegerField()
    sizeid = forms.IntegerField()
    count = forms.IntegerField(required=False)

    # 对数据进行清洗
    def clean(self):
        super(MyForm, self).clean()
        data = self.cleaned_data
        count = data['count']
        # if count < 0:
        #     self.errors['count'] = ['商品数量不能小于0']


class CartView(BaseRedirectView):
    """添加购物项，重定向到购物车界面"""
    redirect_url = '/cart/cart.html'

    def handle(self, request, *args, **kwargs):
        # 处理业务逻辑（添加购物项）
        request.session.modified = True  # session存储机制问题
        cart_manager = SessionCartManager(request.session)
        cart_manager.add_cart_item(**request.POST.dict())


class CartListView(BaseView, OperateView):
    template_name = 'cart.html'
    form_cls = MyForm

    def get_extra_context(self, request):
        cart_manager = SessionCartManager(request.session)
        return {'cartItems': cart_manager.get_all_cart_items()}

    def add(self, request, goodsid, colorid, sizeid, count, *args, **kwargs):
        request.session.modified = True
        cart_manager = SessionCartManager(request.session)
        try:
            cart_manager.add_cart_item(goodsid=goodsid, colorid=colorid, sizeid=sizeid, count= 1)
            return {'errorcode': 200, 'errormsg': ''}
        except Exception as e:
            return {'errorcode': -100}
        # 返回值格式统一，方便大前端（andriod/ios/前端）解析

    def min(self, request, goodsid, colorid, sizeid, *args, **kwargs):
        request.session.modified = True
        cart_manager = SessionCartManager(request.session)
        try:
            cart_manager.add_cart_item(goodsid=goodsid, colorid=colorid, sizeid=sizeid, count=-1)
            return {'errorcode': 200, 'errormsg': ''}
        except Exception as e:
            return {'errorcode': -100}
        # 返回值格式统一，方便大前端（andriod/ios/前端）解析

    def delete(self, request, goodsid, colorid, sizeid, *args, **kwargs):
        request.session.modified = True
        cart_manager = SessionCartManager(request.session)
        try:
            cart_manager.delete_cart_item(goodsid=goodsid, colorid=colorid, sizeid=sizeid)
            return {'errorcode': 200, 'errormsg': ''}
        except Exception as e:
            return {'errorcode': -100, 'errormsg': '删除失败'}