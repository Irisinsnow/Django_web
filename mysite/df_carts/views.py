from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.http import require_GET

from df_carts.models import Cart
from df_goods.models import Goods
from utils.decorators import login_required


@require_GET
@login_required
def cart_add(request):
    """
    添加商品信息到购物车
    """
    goods_id = request.GET.get('goods_id')
    goods_count = request.GET.get('goods_count')
    passport_id = request.session.get("passport_id")
    goods = Goods.objects.get_goods_by_id(goods_id=goods_id)
    # 判断库存够不够数量
    if goods.goods_stock < int(goods_count):
        return JsonResponse({'res': 0})
    else:
        Cart.objects.add_one_cart_info(passport_id=passport_id, goods_id=goods_id, goods_count=int(goods_count))
        return JsonResponse({'res': 1})


@require_GET
@login_required
def cart_count(request):
    """
    获取用户购物车中商品总数
    """
    passport_id = request.session.get('passport_id')
    res = Cart.objects.get_cart_count_by_passport(passport_id=passport_id)
    return JsonResponse({'res': res})


# /cart
@login_required
def cart_show(request):
    """
    显示用户购车页面
    """
    passport_id = request.session.get('passport_id')
    cart_list = Cart.objects_logic.get_cart_list_by_passport(passport_id=passport_id)
    return render(request, 'cart.html', {'cart_list': cart_list})


@require_GET
@login_required
def cart_update(request):
    """
    更新用户购物车的商品数目
    """
    goods_id = request.GET.get('goods_id')
    goods_count = request.GET.get('goods_count')
    passport_id = request.session.get('passport_id')
    res = Cart.objects.update_cart_info_by_passport(passport_id=passport_id,
                                                    goods_id=goods_id, goods_count=int(goods_count))
    if res:
        # 更新成功
        return JsonResponse({'res': 1})
    else:
        return JsonResponse({'res': 0})


@require_GET
@login_required
def cart_del(request):
    """
    删除购物车记录
    """
    cart_id = request.GET.get('cart_id')

    res = Cart.objects.del_cart_info_by_id(cart_id=cart_id)
    if res:
        return JsonResponse({'res': 1})
    else:
        return JsonResponse({"res": 0})
