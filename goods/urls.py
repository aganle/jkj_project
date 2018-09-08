from django.conf.urls import url
from goods import views

urlpatterns = [
    url(r'^$', views.GoodsListView.as_view()),
    url(r'^goodsdetails/$', views.GoodsDetailView.as_view())
]
