from goods.models import *
from view.views import BaseView
from utils.pageutils import MultiObjectReturned


class GoodsListView(BaseView, MultiObjectReturned):
    # 所有不变的东西，都放到类属性中
    template_name = 'index.html'
    objects_name = 'goods'
    category_objects = Category.objects.all()

    def prepare(self, request):
        category_id = int(request.GET.get('category', Category.objects.first().id))
        self.objects = Category.objects.get(id=category_id).goods_set.all()
        self.category_id = category_id

    def get_extra_context(self, request):
        page_num = request.GET.get('page', 1)
        context = {'category_id': self.category_id, 'categorys': self.category_objects}
        # 根据当前页码调用pageutils模块中的get_objects方法获取实体
        context.update(self.get_objects(page_num))
        return context


class GoodsDetailView(BaseView):
    template_name = 'details.html'

    def handle_request_cookie(self, request):
        # 获取cookie
        self.historys = eval(request.COOKIES.get('history', '[]'))
        pass

    def handle_response_cookie(self, response):
        # 设置cookie，填写用户浏览商品的id
        if self.goodsId not in self.historys:
            self.historys.append(self.goodsId)
            # session不能存不能被序列化的字符串
        response.set_cookie('history', str(self.historys))

    def get_extra_context(self, request):
        goodsId = int(request.GET.get('goodsid'))
        self.goodsId = goodsId
        good = Goods.objects.get(id=goodsId)
        # 推荐商品
        recommand_goods = []
        for id in self.historys:
            recommand_goods.append(Goods.objects.get(id=id))
        return {'good': good, 'goods_details':good.goodsdetails_set.all(), 'recommand_goods':recommand_goods[-4 :]}
