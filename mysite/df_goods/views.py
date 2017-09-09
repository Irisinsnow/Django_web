from django.core.paginator import Paginator
from django.http import JsonResponse
from django.shortcuts import render
from df_goods.models import Goods, BrowseHistory, Image
from df_goods.enums import *


def home_list_page(request):
    """
    显示首页的内容
    """
    # 查询每个种类的4个商品和4个新品信息
    fruits_new = Goods.objects.get_goods_list_by_type(goods_type_id=FRUIT, limit=3,
                                                      sort='new')
    fruits = Goods.objects_logic.get_goods_list_by_type(goods_type_id=FRUIT, limit=4)
    seafood_new = Goods.objects.get_goods_list_by_type(goods_type_id=SEAFOOD, limit=3,
                                                       sort='new')
    seafood = Goods.objects_logic.get_goods_list_by_type(goods_type_id=SEAFOOD, limit=4)
    meat_new = Goods.objects.get_goods_list_by_type(goods_type_id=MEAT, limit=3, sort='new')
    meat = Goods.objects_logic.get_goods_list_by_type(goods_type_id=MEAT, limit=4)
    eggs_new = Goods.objects.get_goods_list_by_type(goods_type_id=EGGS, limit=3,
                                                    sort='new')
    eggs = Goods.objects_logic.get_goods_list_by_type(goods_type_id=EGGS, limit=4)
    vegetables_new = Goods.objects.get_goods_list_by_type(goods_type_id=VEGETABLES,
                                                          limit=3, sort='new')
    vegetables = Goods.objects_logic.get_goods_list_by_type(goods_type_id=VEGETABLES,
                                                            limit=4)
    frozen_new = Goods.objects.get_goods_list_by_type(goods_type_id=FROZEN,
                                                      limit=3, sort='new')
    frozen = Goods.objects_logic.get_goods_list_by_type(goods_type_id=FROZEN, limit=4)

    context = {
        'fruits_new': fruits_new, 'fruits': fruits,
        'seafood_new': seafood_new, 'seafood': seafood,
        'meat_new': meat_new, 'meat': meat,
        'eggs_new': eggs_new, 'eggs': eggs,
        'vegetables_new': vegetables_new, 'vegetables': vegetables,
        'frozen_new': frozen_new, 'frozen': frozen
    }
    return render(request, 'index.html', context)


# /goods/商品ID/
def goods_details(request, goods_id):
    """
    显示商品详情页面
    """
    goods = Goods.objects_logic.get_goods_by_id(goods_id=goods_id)
    # 获取新品信息
    goods_new_li = Goods.objects_logic.get_goods_list_by_type(goods_type_id=goods.goods_type_id, limit=2, sort='new')
    # 获取种类
    type_title = GOODS_TYPE[goods.goods_type_id]
    if request.session.has_key('is_login'):
        # 用户已经登陆 可以记录历史浏览信息
        passport_id = request.session.get('passport_id')
        # 浏览的历史记录加入数据库里面
        BrowseHistory.objects.add_one_history(passport_id=passport_id, goods_id=goods_id)

        context = {
            'goods': goods,
            'goods_new_li': goods_new_li,
            'type_title': type_title
        }

        return render(request, 'detail.html', context)


# /list/type_id/page/?sort=
def goods_list(request, goods_type_id, page_index):
    """
    商品列表页面
    """
    sort = request.GET.get('sort', 'default')
    # 根据种类获取goods_list
    goods_li = Goods.objects_logic.get_goods_list_by_type(goods_type_id=goods_type_id, sort=sort)
    # 分页
    paginator = Paginator(goods_li, 1)
    # 获取总页数
    num_pages = paginator.num_pages
    # 当前也转化成数字
    page_index = int(page_index)
    if num_pages <= 5:
        pages = range(1, num_pages + 1)
    # 前三页
    elif page_index <= 3:
        pages = range(1, 6)
    # 最后3页
    elif num_pages - page_index <= 2:
        pages = range(num_pages - 4, num_pages + 1)
    else:
        pages = range(page_index - 2, page_index + 3)
    # 获取第几也的东西
    goods_li = paginator.page(int(page_index))
    good_new_li = Goods.objects_logic.get_goods_list_by_type(goods_type_id=goods_type_id,
                                                             limit=2, sort='new')
    return render(request, 'list.html', {'goods_id': goods_li, 'goods_new_li': good_new_li,
                                         'type_id': goods_type_id, 'type_title': GOODS_TYPE[int(goods_type_id)],
                                         'pages': pages, 'sort': sort})


def get_image_list(request):
    """
    根据商品的Id获取商品图片
    """
    goods_id_list = request.GET.get('goods_id_list')
    goods_id_list = goods_id_list.split(',')
    image_list = Image.objects.get_image_by_goods_id_list(goods_id_list=goods_id_list)
    img_dict = {}
    for image in image_list:
        # json格式需要字符串类型 不然h是IMAGEFILE
        img_dict[image.goods_id] = image.img_url.name
    return JsonResponse({'img_dict': img_dict})
