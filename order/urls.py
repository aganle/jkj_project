from django.conf.urls import url
from order import views
urlpatterns = [
    url(r'^$', views.OrderView.as_view()),
]