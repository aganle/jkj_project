from django.core.paginator import Paginator


class MultiObjectReturned:
    per_page = 12
    objects = None
    objects_name = 'objects'

    def get_objects(self, page_num='1'):
        # 根据当前页码获取实体
        paginator = Paginator(self.objects, self.per_page)
        page_num = int(page_num)
        if page_num < 1:
            page_num = 1
        if page_num > paginator.num_pages:
            page_num = paginator.num_pages
        page = paginator.page(page_num)

        # 返回值：
        # page:用于判断是否有上、下一页
        # page_range:页码范围
        # self.objects_name: 当前页的所有实体
        returned = {'page': page,
                    'page_range': paginator.page_range,
                    self.objects_name: page.object_list}
        return returned
