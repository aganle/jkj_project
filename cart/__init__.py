# CRUD操作
# 存放在session中,（商品id，商品颜色id，商品尺寸id）==》唯一标示一件商品
# {'cart',[{'102020':{'goodsid':10,'colorid':20,'sizeid':20,'count':10}},
#          {'112020':{'goodsid':11,'colorid':20,'sizeid':20,'count':20}}]}
# 用户是否登录
# 未登录则存放在session中
# 已登录则存放在数据库中
# goodsid
# colordid
# sieziid
# count
# user

# 用户表
# email
# name
# 密码

# 购物车设计
# 商品详情界面：
#  添加商品（CartView）,添加后重定向，（开发中很多界面都会重定向）
#  重定向到购物车界面（form表单）
# type = add&count=1
# View父类
# getattr(request.POST.get('type'))(**request.POST)  添加

# class BaseRedirectView(View):
# 	redirect_url = None
# 	def dispath_request(self):
# 		# 重定向一般是处理业务
# 		getattr(self, 'handle')(request)
# 		# 显示交给重定向后的页面
# 		return HttpRedirectResponse(self.redirect_url)

# class CartView(BaseRedirectView):
#     redirect_url = '/cartlistview'
#     def handle(self, request):
#     	utils = getCartUtils(request)
#     	utils.save(**request.POST)



# 购物车界面：
#  ajax
#  修改数量
#  查看商品
# 当用户出现：
#  session中的数据同步到数据库
# 工厂模式动态的获得操作对象（CRUD）

# 工厂模式/策略模式
# class CartUtils():
# 	def add(goodsid,colorid,sizeid,count):
# 		pass
# 	def delete(goodsid,colorid,sizeid):
# 		pass
# class SessionCartUutils(CartUtils):
#     def __init__(self,session):
#     	self.session = session

# class DBCartUtils(CartUtils):
# 	def add(goodsid,colorid,sizeid,count):
# 		pass
# 	def delete(goodsid,colorid,sizeid):
# 		pass
#     def getCartUtils(request):
#     	# 用户已登录
#     	if request.session.get('user', None):
#     		return DBCartUtils()
#     	else:
#     		# 用户未登录
#     		return SessionCartUutils()
#   utils = getCartUtils(request)

# 用户
# 实现简单登录（md5.js前端加密）
# md5（前端[md5.js]+后台[hashlib]）
# md5+如何在不同的时间登录，发送给服务器的密码不同（加密之后的密码是随机的）
# 中间件：对未登录用户和已登录的用户访问不同的界面