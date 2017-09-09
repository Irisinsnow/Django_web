from django.conf.urls import url

from df_carts import views

urlpatterns = [
    url(r"^add/$", views.cart_add),  # 添加商品到购物车
    url(r'^count/$', views.cart_count),  # 统计购物车里的数量
    url(r'^update/$', views.cart_update),  # 更新购物车信息
    url(r'^del/$', views.cart_del),  # 删除购物车信息
    url(r'^$', views.cart_show),  # 显示购物车页面
]
