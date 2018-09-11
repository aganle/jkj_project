from django.views import View
from django.shortcuts import render
from django.http.response import HttpResponseRedirect, JsonResponse, HttpResponseBadRequest


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

# 需要处理一些业务逻辑
class BaseRedirectView(View):
    redirect_url = None  # 留给子类实现
    def dispatch(self, request, *args, **kwargs):
        if hasattr(self, 'handle'):
            getattr(self, 'handle')(request, *args, **kwargs)
        return HttpResponseRedirect(self.redirect_url)

# 处理的都是post请求，这个里面不用渲染数据
# 一般来说不用渲染模板，只需要返回json即可
# request中有一个方法：is_ajax判断是否是ajax方法
class OperateView(View):
    form_cls = None
    def post(self, request, *args, **kwargs):
        form = self.form_cls(request.POST.dict())
        if form.is_valid():
            handle = self.request.POST.get('type', '')
            if hasattr(self, handle):
                return JsonResponse(getattr(self, handle)(request, **form.cleaned_data), safe=False)
            else:
                return HttpResponseBadRequest('type没有传递')
        else:
            return JsonResponse({'errorcode': -300, 'errormsg': form.errors})