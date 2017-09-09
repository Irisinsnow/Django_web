from django.db import transaction
from django.http import JsonResponse
from django.shortcuts import render
from django.utils import timezone
from django.views.decorators.http import require_POST

from df_carts.models import Cart
from df_orders.models import OrderBasic, OrderDetail
from df_user.models import Address
from utils.decorators import login_required

timezone.now()


@login_required
def cart_place(request):
    """
    提交订单页面
    """
    passport_id = request.session.get('passport_id')
    # 查询默认的收货地址
    addr = Address.objects.get_default_addr(passport_id=passport_id)
    # 获取cart_id_list gET Post QueryDict
    cart_id_list = request.POST.getlist('cart_id_list')
    # ['1','2','3']
    cart_list = Cart.objects_logic.get_cart_list_by_id_list(cart_id_list=cart_id_list)
    cart_id_list = ','.join(cart_id_list)  # 1,2,3
    return render(request, 'place_order.html', {
        'addr': addr, 'cart_list': cart_list, 'cart_id_list': cart_id_list
    })


# 事务
@require_POST
@login_required
@transaction.atomic
def order_commit(request):
    """
    创建订单信息
    """
    addr_id = request.POST.get('addr_id')
    pay_method = request.POST.get('pay_method')
    cart_id_list = request.POST.get('cart_id_list')
    passport_id = request.session.get('passport_id')

    order_id = timezone.now().strftime('%Y%m%d%H%M%S') + str(passport_id)
    transit_price = 10.0

    cart_id_list = cart_id_list.split(',')  # 切分一个列表
    total_count, total_price = Cart.objects.get_goods_count_and_amout_by_id_list(cart_id_list=cart_id_list)
    # 创建一个保存点
    save_id = transaction.savepoint()
    try:
        # 创建订单的基本信息
        OrderBasic.objects.add_one_order_basic_info(order_id=order_id,
                                                    passport_id=passport_id,
                                                    addr_id=addr_id, total_count=total_count, total_price=total_price,
                                                    transit_price=transit_price, pay_method=pay_method)

        # 遍历创建订单详情
        cart_list = Cart.objects.get_cart_list_by_id_list(cart_id_list=cart_id_list)
        for cart_info in cart_list:
            # 组织订单详情数据
            goods_id = cart_info.goods.id
            goods_count = cart_info.goods_count
            goods_price = cart_info.goods.goods_price

            # 判断商品库存是不是足够
            if goods_count < cart_info.goods.goods_stock:
                # 库存充足
                OrderDetail.objects.add_one_order_detail_info(order_id=order_id, goods_id=goods_id,
                                                              goods_count=goods_count, goods_price=goods_price)
                # 清空购物车
                cart_info.delete()

                # 修改商品的库存和销量
                cart_info.goods.goods_stock = cart_info.goods.goods_stock - goods_count
                cart_info.goods.goods_sales = cart_info.goods.goods_sales + goods_count
                cart_info.goods.save()
            else:
                transaction.savepoint_rollback(save_id)
                return JsonResponse({'res': 0, 'content': '库存不足'})

    except Exception as e:
        # 出现异常
        transaction.savepoint_rollback(save_id)
        return JsonResponse({'res': 0, 'content': '服务器错误'})

    transaction.savepoint_commit(save_id)
    return JsonResponse({'res': 1})
