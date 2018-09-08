from django.views import View
from django.shortcuts import render
from django.http.response import HttpResponse


class BaseView(View):
    """完成渲染功能，准备阶段"""
    template_name = None

    def get(self, request, *args, **kwargs):
        # prepare预处理，获取objects
        if hasattr(self, 'prepare'):
            getattr(self, 'prepare')(request, *args, **kwargs)
        # 用于获取cookie
        if hasattr(self, 'handle_request_cookie'):
            getattr(self, 'handle_request_cookie')(request, *args, **kwargs)
        response = render(request, self.template_name, self.get_context(request))
        # 用于添加cookie
        if hasattr(self, 'handle_response_cookie'):
            getattr(self, 'handle_response_cookie')(response, *args, **kwargs)
        return response

    def get_context(self, request):
        context = {}
        context.update(self.get_extra_context(request))
        return context

    def get_extra_context(self, request):
        # 让子类实现
        return {}