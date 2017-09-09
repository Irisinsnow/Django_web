from django.conf.urls import url

from df_goods import views

urlpatterns = [
    url(r'^$', views.home_list_page),  # 显示首页内容
    url(r'^goods/(?P<goods_id>\d+)/$', views.goods_details),  # 显示商品的详情页面
    url(r'^list/(\d+)/(\d+)/$', views.goods_list),  # 显示商品的第几面
    url(r'^get_image_list/$', views.get_image_list),  # 获取搜索结果页的商品图片数据

]
