from cart.models import *

class CartManager:
    """完成购物车中的增删改查"""
    def add_cart_item(self, goodsid, colorid, sizeid, count, *args, **kwargs):
        pass

    def delete_cart_item(self, goodsid, colorid, sizeid, count, *args, **kwargs):
        pass

    def get_all_cart_items(self, *args, **kwargs):
        pass


class SessionCartManager(CartManager):
    # 注意session可能为空
    # 浏览器发送过来的数据都是字符串
    def __init__(self, session):
        self.session = session

    def add_cart_item(self, goodsid, colorid, sizeid, count, *args, **kwargs):
        # [{"key":CatItem}]  /[{'key':key,'value':CartItem}]
        cart = self.session.get('cart', [])
        key = self.__gen_key(goodsid, colorid, sizeid)
        if self.is_exist(cart, key):
            cartitem = self.get_cart_item(cart, key)
            cartitem.count += count
        else:
            cart.append({key:CartItem(goodsid=goodsid, colorid=colorid, sizesid=sizeid, count=count)})
        self.session['cart'] = cart

    def delete_cart_item(self, goodsid, colorid, sizeid, count, *args, **kwargs):
        pass

    def get_all_cart_items(self, *args, **kwargs):
        # [{'10101':CartItem}]
        cart = self.session.get('cart', [])
        if cart == None:
            return []
        else:
            cartitems = []
            for cartitem in cart:
                cartitems.extend(cartitem.values())
            return cartitems

        return self.session.get('cart', [])

    def __gen_key(self, goodsid, colorid, sizeid):
        # 根据(goodsid, colorid, sizeid)生成key，唯一标识一件商品
        return goodsid + '-' + colorid + '-' + sizeid

    def is_exist(self, cart, key):
        # 根据key判断cart是否已经存在key所对应的CartItem
        isExist = False
        for cartitem in cart:
            if cartitem.keys()[0] == key:
                isExist = True
                break
        return isExist

    def get_cart_item(self, cart, key):
        for cartitem in cart:
            if cartitem.keys()[0] == key:
                return cartitem[key]
        return None