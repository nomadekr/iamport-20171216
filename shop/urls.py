from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'(?P<item_id>\d+)/order/new/$', views.order_new, name='order_new'),
]

