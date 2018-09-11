from django.conf.urls import url
from user import views
urlpatterns = [
    url(r'^register/$', views.RegisterView.as_view()),
    url(r'^registercontrol/$', views.RegisterControlView.as_view()),
    url(r'^login/$', views.LoginView.as_view()),
    url(r'^logincontrol/$', views.LoginControl.as_view()),
    url(r'^usercenter/$', views.UserCenterView.as_view()),
    url(r'^address/$', views.AddressView.as_view()),
]