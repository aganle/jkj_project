from django.views import View
from django.shortcuts import render


class BaseView(View):
    """完成渲染功能，准备阶段"""
    template_name = None

    def get(self, request, *args, **kwargs):
        # prepare预处理，获取objects
        if hasattr(self, 'prepare'):
            getattr(self, 'prepare')(request, *args, **kwargs)
        response = render(request, self.template_name, self.get_context(request))
        if hasattr(self, 'destory'):
            getattr(self, 'destory')(request)
        return response

    def get_context(self, request):
        context = {}
        context.update(self.get_extra_context(request))
        return context

    def get_extra_context(self, request):
        # 让子类实现
        return {}