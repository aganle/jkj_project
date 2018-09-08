from django.shortcuts import render
from django.views import View
from goods.models import *
from django.core.paginator import Paginator
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

