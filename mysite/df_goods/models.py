from django.db import models
from tinymce.models import HTMLField

from db.BaseManager import BaseManager
from db.baseModel import BaseModel
from df_goods.enums import *


class GoodLocalManager(BaseManager):
    """
    商品的逻辑模型管理类
    """

    def get_goods_by_id(self, goods_id):
        """
        根据商品的ID进行查找
        """
        goods = Goods.objects.get_goods_by_id(goods_id=goods_id)
        image = Image.objects.get_image_by_goods_id(goods_id)

        goods.img_url = image.img_url
        return goods

    def get_goods_list_by_type(self, goods_type_id, limit=None, sort='default'):
        """
        根据商品的种类ID获取商品信息
        """
        goods_list = Goods.objects.get_goods_list_by_type(goods_type_id=goods_type_id,
                                                          limit=limit, sort=sort)

        for goods in goods_list:
            img = Image.objects.get_image_by_goods_id(goods_id=goods.id)
            goods.img_url = img.img_url
        return goods_list


class GoodManager(BaseManager):
    """
    商品模型管理类
    """

    def get_goods_by_id(self, goods_id):
        """
        跟商品的id获取商品信息
        """
        goods = self.get_one_object(id=goods_id)
        return goods

    def get_goods_list_by_type(self, goods_type_id, limit=None, sort='default'):
        if sort == 'new':
            # 新品
            order_by = ('-create_time',)
        elif sort == 'price':
            # 价格
            order_by = ('goods_price',)
        elif sort == 'hot':
            # 人气排序
            order_by = ('-goods_sales',)
        else:
            order_by = ('-pk',)
        goods_list = self.get_object_list(filters={'goods_type_id': goods_type_id}, order_by=order_by)
        if limit:
            goods_list = goods_list[:limit]
        return goods_list


class Goods(BaseModel):
    """
    商品模型类
    """
    goods_type_choice = (
        (FRUIT, GOODS_TYPE[FRUIT]),
        (SEAFOOD, GOODS_TYPE[SEAFOOD]),
        (MEAT, GOODS_TYPE[MEAT]),
        (EGGS, GOODS_TYPE[EGGS]),
        (VEGETABLES, GOODS_TYPE[VEGETABLES]),
        (FROZEN, GOODS_TYPE[FROZEN])
    )
    # 1-6之间
    goods_type_id = models.SmallIntegerField('商品种类id', choices=goods_type_choice)
    goods_name = models.CharField('商品名称', max_length=20)
    goods_sub_title = models.CharField('副标题', max_length=256)
    goods_price = models.DecimalField('价格', max_digits=10, decimal_places=2)
    transit_price = models.DecimalField('运费', max_digits=10, decimal_places=2)
    goods_unite = models.CharField('单位', max_length=20)
    goods_info = HTMLField('商品详情')
    goods_stock = models.IntegerField(default=0, verbose_name='库存')
    goods_sales = models.IntegerField('商品销量', default=0)
    goods_status = models.SmallIntegerField('状态', default=0)

    objects = GoodManager()
    objects_logic = GoodLocalManager()

    class Meta:
        db_table = 's_goods'


class ImageManager(BaseManager):
    """
    图片模型管理类
    """

    def get_image_by_goods_id(self, goods_id):
        """
        根据商品的id获取商品的图片
        """
        images = self.get_object_list(filters={'goods_id': goods_id})
        if images.exists():
            # 商品有图片
            images = images[0]
        else:
            # 商品没有图片
            images.img_url = ''
        return images

    def get_image_by_goods_id_list(self, goods_id_list):
        """
        根据goods_id_list获取图片的查询集
        """
        image_list = self.get_object_list(filters={'goods_id__in': goods_id_list})
        return image_list


class Image(BaseModel):
    """
    图片模型类
    """
    goods = models.ForeignKey('Goods', verbose_name="所属商品")
    img_url = models.ImageField(upload_to='goods', verbose_name='商品图片')
    is_def = models.BooleanField('是否默认', default=False)

    objects = ImageManager()

    class Meta:
        db_table = 's_goods_image'


class BrowseHistoryLogicManager(BaseManager):
    """
    浏览历史的逻辑模型管理器
    """

    def get_browse_list_by_passport(self, passport_id, limit=None):
        """
        获取浏览记录的信息列表:
        """
        browsed_li = BrowseHistory.objects.get_browse_list_by_passport(passport_id=passport_id, limit=limit)
        for browsed in browsed_li:
            image = Image.objects.get_image_by_goods_id(goods_id=browsed.goods.id)
            browsed.img_url = image.img_url
        return browsed_li


class BrowseHistoryManager(BaseManager):
    """
    历史浏览模型的管理类
    """

    def get_one_history(self, passport_id, goods_id):
        """
        查询用户是否浏览过该商品
        """
        browsed = self.get_one_object(passport_id=passport_id, goods_id=goods_id)
        return browsed

    def add_one_history(self, passport_id, goods_id):
        """
        添加一条用户的浏览记录
        """
        browsed = self.get_one_history(passport_id=passport_id, goods_id=goods_id)
        if browsed:
            # 如果浏览过该商品,update save
            browsed.save()
        else:
            browsed = self.create_one_object(passport_id=passport_id, goods_id=goods_id)

        return browsed

    def get_browse_list_by_passport(self, passport_id, limit=None):
        """
        根据passport_id 获取浏览记录
        """
        browsed_li = self.get_object_list(filters={'passport_id': passport_id}, order_by=('-update_time',))
        if limit:
            browsed_li = browsed_li[:limit]
        return browsed_li


class BrowseHistory(BaseModel):
    """
    历史浏览模型类
    """
    passport = models.ForeignKey('df_user.Passport', verbose_name='所属账户')
    goods = models.ForeignKey('df_goods.Goods', verbose_name='商品')

    objects = BrowseHistoryManager()
    objects_logic = BrowseHistoryLogicManager()

    class Meta:
        db_table = 's_browse_history'
