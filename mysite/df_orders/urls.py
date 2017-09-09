from django.conf.urls import url

from df_orders import views

urlpatterns = [
    url(r"^$", views.cart_place),  # 提交订单页面
    url(r'^commit/$', views.order_commit),  # 创建订单

]
