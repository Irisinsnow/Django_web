from django.db import models
from db.baseModel import BaseModel
from db.BaseManager import BaseManager


class PassportManager(BaseManager):
    """
    通行证的管理器模型
    """

    def add_one_passport(self, username, password, email):
        """
        添加一个账户的信息
        """
        passport = self.create_one_object(username=username, password=password, email=email)
        return passport

    def get_one_passport(self, username, password=None):
        """z
        根据用户名和密码进行获取
        """
        if password is None:
            passport = self.get_one_object(username=username)
        else:
            passport = self.get_one_object(username=username, password=password)
        return passport


class Passport(BaseModel):
    """
    通行证模型类
    """

    username = models.CharField("用户名", max_length=20)
    password = models.CharField('密码', max_length=40)
    email = models.EmailField('用户邮箱')

    objects = PassportManager()

    class Meta:
        db_table = 's_user_account'  # 制定表明


class AddressManager(BaseManager):
    """
    地址类模型的管理器模型
    """

    def get_default_addr(self, passport_id):
        """
        根据passport_id 进行查询账户的默认收货地址
        """
        addr = self.get_one_object(passport_id=passport_id, is_def=True)
        return addr

    def add_one_address(self, passport_id, recipient_name, recipient_addr,
                        recipient_phone, zip_code):
        def_addr = self.get_default_addr(passport_id=passport_id)
        if def_addr:
            # 用户有默认的地址
            addr = self.create_one_object(passport_id=passport_id,
                                          recipient_name=recipient_name,
                                          recipient_addr=recipient_addr,
                                          recipient_phone=recipient_phone,
                                          zip_code=zip_code)
        else:
            # 用户没有默认地址 添加默认
            addr = self.create_one_object(passport_id=passport_id,
                                          recipient_name=recipient_name,
                                          recipient_addr=recipient_addr,
                                          recipient_phone=recipient_phone,
                                          zip_code=zip_code,
                                          is_def=True)
        return addr


class Address(BaseModel):
    """
    创建地址类的模型类
    """
    passport = models.ForeignKey('Passport', verbose_name="所属账户")
    recipient_name = models.CharField("收件人", max_length=20)
    recipient_addr = models.CharField("收件人地址", max_length=256)
    recipient_phone = models.CharField("收件人的电话", max_length=11)
    zip_code = models.CharField("邮政编码", max_length=6)
    is_def = models.BooleanField("是否默认", default=False)

    objects = AddressManager()

    class Meta:
        db_table = 's_user_address'
