from django.conf.urls import url
from .views import *

urlpatterns = [
    url(r'^login/$',login_views,name='login'),
    url(r'^register/$',register_views,name='register'),
    url(r'^checkphone/$',checkphone_views),
    url(r'^all_type_goods/$',all_type_goods_views),
    url(r'^logout/$',logout_views,name='logout'),
    url(r'^check_login/$', check_login_views),
    url(r'^add_cart/$',add_cart_views),
    url(r'^',index_views),
]