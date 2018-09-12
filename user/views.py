from django.http import HttpResponse
from django.shortcuts import render
from view.views import BaseView, BaseRedirectView, OperateView
from user.models import *
from utils.commonutils import *
from django import forms


class UserCenterView(BaseView):
    template_name = 'user.html'


class RegisterView(BaseView):
    template_name = 'register.html'


class RegisterControlView(BaseRedirectView):
    redirect_url = '/user/usercenter/'

    # 完成表单的验证
    def handle(self, request, *args, **kwargs):
        user = User.register(**request.POST.dict())
        request.session['user'] = user


class LoginView(BaseView):
    template_name = 'login.html'


class LoginControl(BaseRedirectView):
    redirect_url = '/user/usercenter/'

    def handle(self, request, *args, **kwargs):
        user = User.login(**request.POST.dict())
        request.session['user'] = user


class AddressForm(forms.Form):
    name = forms.CharField(required=False)
    phone = forms.CharField(required=False)
    provinceid = forms.IntegerField(required=False)
    cityid = forms.IntegerField(required=False)
    areaid = forms.IntegerField(required=False)
    details = forms.CharField(required=False)


class AddressView(BaseView, OperateView):
    template_name = 'address.html'
    form_cls = AddressForm

    def get_extra_context(self, request):
        default_cities = get_cities_by_id(provinces[0]['id'])
        default_areas = get_areas_by_id(default_cities[0]['id'])
        user = request.session['user']
        address = user.address_set.all()
        return {
            'provinces': provinces,
            'cities': default_cities,
            'areas': default_areas,
            'address': address
        }

    def get_cities(self, request, provinceid, *args, **kwargs):
        data = []
        cities = get_cities_by_id(str(provinceid))
        data.append(cities)
        areas = get_areas_by_id(cities[0]['id'])
        data.append(areas)
        return data

    def get_areas(self, request, cityid, *args, **kwargs):
        areas = get_areas_by_id(str(cityid))
        return areas

    def save_address(self, request, name, phone, provinceid, cityid, areaid, details):
        user = request.session.get('user')
        province = get_province_by_id(provinceid)
        city = get_city_by_id(provinceid, cityid)
        area = get_area_by_id(cityid, areaid)
        try:
            address = Address.objects.create(name=name, phone=phone, province=province,city=city, area=area, details=details, user=user)
            return {'errorcode': 200, 'errormsg': ''}
        except:
            return {'errorcode': 200, 'errormsg': '地址保存失败'}

