from django.http import HttpRequest, HttpResponseRedirect
from jkj_project import settings


class UserAuth(object):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request, *args, **kwargs):
        # 如果用户请求的地址是user相关的的，先判断是否已经登录
        print('我执行了')
        if request.path in settings.AUTH:
            user = request.session.get('user', '')
            # 不满足条件，重定向
            if not user:
                return HttpResponseRedirect('/user/login')
        # 满足条件，正常访问
        return self.get_response(request)
