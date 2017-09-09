import copy

from django.db import models


class BaseManager(models.Manager):
    """
    一个基础的模型管理类
    """

    def get_all_valid_fields(self):
        """
        获取self所在模型类的有效属性的字符串列表
        """
        model_class = self.model
        attr_tuple = model_class._meta.get_fields()
        str_attr_list = []
        for attr in attr_tuple:
            # 把ForeignKey的attr.name 加上_id
            if isinstance(attr, models.ForeignKey):
                str_attr = '%s_id' % attr.name
            else:
                str_attr = attr.name
            # 把str_attr加入列表中
            str_attr_list.append(str_attr)

        return str_attr_list

    def create_one_object(self, **kwargs):
        """
        创建一个对象进入数据库
        """
        valid_list = self.get_all_valid_fields()
        # 遍历删除之前拷贝一份字典 然后用新的字典来遍历
        kws = copy.copy(kwargs)

        for key in kws:
            if key not in valid_list:
                kwargs.pop(key)

        model_class = self.model
        obj = model_class(**kwargs)
        obj.save()
        return obj

    def get_one_object(self, **filters):
        """
        根据filter条件查询
        """
        try:
            obj = self.get(**filters)
        except self.model.DoesNotExist:
            obj = None
        return obj

    def get_object_list(self, filters={}, exclude_filters={}, order_by=('-pk',)):
        """
        查询self.model模型对应查询集合
        """
        object_list = self.filter(**filters).exclude(**exclude_filters).order_by(*order_by)
        return object_list
