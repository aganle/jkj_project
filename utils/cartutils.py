from cart.models import *

class CartManager:
    """完成购物车中的增删改查"""
    def add_cart_item(self, goodsid, colorid, sizeid, count, *args, **kwargs):
        pass

    def delete_cart_item(self, goodsid, colorid, sizeid, *args, **kwargs):
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
        count = int(count)
        cart = self.session.get('cart', [])
        key = self.__gen_key(goodsid, colorid, sizeid)
        if self.is_exist(cart, key):
            cartitem = self.get_cart_item(cart, key)
            if (cartitem.count + count) < 1:
                raise Exception()
            cartitem.count += count
        else:
            cart.append({key: CartItem(goodsid=goodsid, colorid=colorid, sizeid=sizeid, count=count)})
        self.session['cart'] = cart

    def delete_cart_item(self, goodsid, colorid, sizeid, *args, **kwargs):
        key = self.__gen_key(goodsid, colorid, sizeid)
        cart = self.session.get('cart')
        if self.is_exist(cart, key):
            index = -1
            for i in range(len(cart)):
                cart_list = list(cart[i].keys())
                if cart_list[0] == str(key):
                    index = i
                    break
            if index != -1:
                del cart[index]



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
        return str(goodsid) + '-' + str(colorid) + '-' + str(sizeid)

    def is_exist(self, cart, key):
        # 根据key判断cart是否已经存在key所对应的CartItem
        isExist = False
        for cartitem in cart:
            cartitem_keys_list = list(cartitem.keys())
            if cartitem_keys_list[0] == key:
                isExist = True
                break
        return isExist

    def get_cart_item(self, cart, key):
        for cartitem in cart:
            cartitem_keys_list = list(cartitem.keys())
            if cartitem_keys_list[0] == key:
                return cartitem[key]
        return None

    def get_cart_item_by_id(self, goodsid, colorid, sizeid, *args, **kwargs):
        cart = self.session.get('cart')
        key = self.__gen_key(goodsid, colorid, sizeid)
        if cart == None:
            return None
        else:
            for i in range(len(cart)):
                if list(cart[i].keys())[0] == key:
                    return list(cart[i].values())[0]

class UserCartManager(CartManager):
    pass

def get_cart_manager(request):
    if not request.session.get('user',"") :
        return SessionCartManager(request.session)
    else:
        # 值得考虑，需不需要将ssesion中的购物车数据拷贝到数据库
        # 删除session的购物车
        return UserCartManager(request.session)