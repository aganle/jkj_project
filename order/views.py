from django.shortcuts import render
from order.models import *
from goods.models import Store, Goods, Size
from utils.cartutils import SessionCartManager
from view.views import BaseRedirectView, View, BaseView
from django.http.response import HttpResponse, HttpResponseRedirect
import time
import uuid
from jkj_project.settings import BASE_DIR
from utils.alipay import AliPay
import os


alipay = AliPay(
    appid='2016091700531731',
    app_private_key_path=os.path.join(BASE_DIR, 'keys/app_private_2048.txt'),
    alipay_public_key_path=os.path.join(BASE_DIR, 'keys/alipay_public_2048'),
    return_url='http://127.0.0.1:8000/order/alipay/',
    app_notify_url='http://www.bjsxt.com'
)


class OrderView(View):
    def post(self, request):
        if request.session.get('user'):
            # 订单界面
            # 拿到购物项cartitems
            cartitems = request.POST.get('cartitems')
            request.session['cartitems'] = cartitems
            return HttpResponse('/order/orderlist/')
        else:
            # 登录界面
            return HttpResponse('/user/login/')

class OrderListView(BaseView):
    template_name = 'order.html'

    def get_extra_context(self, request):
        rawcartitems = request.session.get('cartitems', '')
        cartitems = rawcartitems.split(':')
        cart_manager = SessionCartManager(request.session)
        # 根据商品id，颜色，尺寸获得订单项
        # 读取用户的默认收货地址
        order_items = []
        for cartitem in cartitems:
            order_items.append(cart_manager.get_cart_item_by_id(*cartitem.split(',')))
        user = request.session.get('user')
        address = user.address_set.first()
        allprice = 0
        for order_item in order_items:
            allprice += order_item.all_price()
        return {'address': address, 'orderitems': order_items, 'allprice': allprice, 'raworderitems': rawcartitems}


class OrderCreatedView(BaseRedirectView):
    redirect_url = '' # 支付页面

    def handle(self, request):
        request.session.modified = True
        del request.session['cartitems']
        # 删除购物车记录
        orderitems = request.GET.get('orderitems')
        orderitems = orderitems.split(':')
        cart_manager = SessionCartManager(request.session)

        price = 0
        # 获取总价，留给后面支付使用
        for orderitem in orderitems:
            price += cart_manager.get_cart_item_by_id(*orderitem.split(',')).all_price()

        for orderitem in orderitems:
            # 从购物车中移除
            cart_manager.delete_cart_item(*orderitem.split(','))
        # order对象 （收货地址，订单项）（未付款，已付款，待评价，待收货，待发货，退货中，退货成功）
        # 反应用户买东西的事件
        # 订单的唯一标识 sign
        # 反应用户买东西的事件 order
        order = Order.objects.create(name=request.GET['name'], phone = request.GET['phone'],
                                     address = request.GET['address'], payway=request.GET['type'],
                                     orderitems=orderitems, sign = uuid.uuid4().hex,
                                     order=str(time.time() * 1000), user=request.session.get('user'))
        # 库存减少
        for orderitem in orderitems:
            goodsid, colorid, sizeid, count = orderitem.split(',')
            store = Goods.objects.get(id=goodsid).store_set.filter(color_id=colorid).filter(size=Size.objects.get(id=sizeid)).first()
            store.count -= int(count)
            store.save()  # 保存到数据库

        # 根据支付方式，生成支付页面
        params = alipay.direct_pay(out_trade_no=order.sign, subject='商城支付', total_amount=str(price))
        url = 'https://openapi.alipaydev.com/gateway.do?' + params
        order.save()  # 未支付状态
        self.redirect_url = url


class AliPayView(BaseView):
    def get(self, request, *args, **kwargs):
        data = request.GET.dict()
        # data中的业务参数：out_trade_no,trade_no,total_amount
        sign = data.pop('sign')
        if alipay.verify(data, sign):
            # 取出订单对象，修改订单状态，添加trade_no（退款凭证，服务器和支付宝的一个交易凭证）
            print(data['trade_no'], data['out_trade_no'], data['total_amount'])
            order = Order.objects.get(sign=data['out_trade_no'])
            order.status = '代发货'
            order.trade_no = data['trade_no']
            order.save()
            # 支付成功，重定向到订单页面，让用户选择是否支付成功
            # 如果用户选择已经支付成功，则查询数据库是否已经更新订单状态，如果没有则向服务器发起主动查询
            return HttpResponse('支付成功')
        else:
            return HttpResponse('支付失败')