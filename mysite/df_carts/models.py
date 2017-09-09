from django.db import models
from django.db.models import Sum  # 导入聚合类

from db.BaseManager import BaseManager
from db.baseModel import BaseModel
from df_goods.models import Image


# Create your models here.

class CartLogicManager(BaseManager):
    """
    购物车逻辑模型管理器类
    """

    def get_cart_list_by_passport(self, passport_id):
        """
        根据passport_id查询用户的购物车信
        """
        cart_list = Cart.objects.get_cart_list_by_passport(passport_id=passport_id)
        for cart_info in cart_list:
            # 根据商品id获取商品图片
            img = Image.objects.get_image_by_goods_id(goods_id=cart_info.goods.id)
            cart_info.goods.img_url = img.img_url
        return cart_list

    def get_cart_list_by_id_list(self, cart_id_list):
        """
        根据cart_id_list查询购物车信息
        """
        cart_list = Cart.objects.get_cart_list_by_id_list(cart_id_list=cart_id_list)
        for cart_info in cart_list:
            # 根据商品id获取商品图片
            img = Image.objects.get_image_by_goods_id(goods_id=cart_info.goods.id)
            cart_info.goods.img_url = img.img_url
        return cart_list


class CartManager(BaseManager):
    """
    购物车模型管理器类
    """

    def get_one_cart_info(self, passport_id, goods_id):
        """
        获取用户购物车中的某条信息
        """
        cart_info = self.get_one_object(passport_id=passport_id, goods_id=goods_id)
        return cart_info

    def add_one_cart_info(self, passport_id, goods_id, goods_count):
        """
        添加购物车记录
        """
        # 1.判断用户的购物车中是否已经添加过该商品
        cart_info = self.get_one_cart_info(passport_id=passport_id, goods_id=goods_id)
        if cart_info is None:
            cart_info = self.create_one_object(passport_id=passport_id, goods_id=goods_id, goods_count=goods_count)
        else:
            cart_info.goods_count = cart_info.goods_count + goods_count
            cart_info.save()
        return cart_info

    def get_cart_count_by_passport(self, passport_id):
        """
        根据passport_id查询购物中商品的总数
        """
        res_dict = self.get_object_list(filters={'passport_id': passport_id}).aggregate(Sum('goods_count'))
        # 返回值为一个特点，格式：{'goods_count__sum':结果} 若聚合没有结果，值部分为None
        res = res_dict['goods_count__sum']
        if res is None:
            res = 0
        return res

    def get_cart_list_by_passport(self, passport_id):
        """
        根据passport_id查询用户的购物车信
        """
        cart_list = self.get_object_list(filters={'passport_id': passport_id})
        return cart_list

    def update_cart_info_by_passport(self, passport_id, goods_id, goods_count):
        """
        根据passport_id更新用户购物车中商品的数目
        """
        cart_info = self.get_one_cart_info(passport_id=passport_id, goods_id=goods_id)
        # 1.判断商品的库存是否充足
        if cart_info.goods.goods_stock < goods_count:
            # 库存不足
            return False
        else:
            # 库存足够
            cart_info.goods_count = goods_count
            cart_info.save()
            return True

    def del_cart_info_by_id(self, cart_id):
        """
        根据cart_id删除购物车信息
        """
        try:
            cart_info = self.get_one_object(id=cart_id)
            cart_info.delete()
            return True
        except Exception as e:
            return False

    def get_cart_list_by_id_list(self, cart_id_list):
        """
        根据cart_id_list查询购物车信息
        """
        cart_list = self.get_object_list(filters={'id__in': cart_id_list})
        return cart_list

    def get_goods_count_and_amout_by_id_list(self, cart_id_list):
        """
        获取购物车中商品的总数目和总价格
        """
        cart_list = self.get_object_list(filters={'id__in': cart_id_list})
        # 累加计算商品总数和总价
        total_count, total_price = 0, 0
        for cart_info in cart_list:
            total_count = total_count + cart_info.goods_count
            total_price = total_price + cart_info.goods_count * cart_info.goods.goods_price
        return total_count, total_price


class Cart(BaseModel):
    """
    购物车模型类
    """
    passport = models.ForeignKey('df_user.Passport', verbose_name='账户')
    goods = models.ForeignKey('df_goods.Goods', verbose_name='商品')
    goods_count = models.IntegerField(default=1, verbose_name='商品数目')

    objects = CartManager()
    objects_logic = CartLogicManager()

    class Meta:
        db_table = 's_cart'
