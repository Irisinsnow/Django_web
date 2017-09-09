from django.conf.urls import url

from df_user import views

urlpatterns = [
    url(r"^register/$", views.register),  # 用户的注册页面和views
    url(r"^check_user_name_exist/$", views.check_user_name_exist),  # 检查用户名是否存在
    url(r'^login/$', views.login),  # 用户登陆
    url(r'^login_check/$', views.login_check),  # 用户登陆检验
    url(r'^logout/$', views.logout),  # 用户登出

    url(r'^$', views.user),  # 显示用户中心个人信息页
    url(r'^address/$', views.address),  # 显示用户中心地址页
    url(r'^order/(\d+)/$', views.order),  # 显示用户中心个人订单页

]
