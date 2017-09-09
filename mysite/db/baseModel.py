from django.db import models


class BaseModel(models.Model):
    """
    这是一个抽象的基类模型
    """
    is_delete = models.BooleanField(verbose_name="删除", default=False)
    update_time = models.DateTimeField(verbose_name="修改时间", auto_now=True)
    create_time = models.DateTimeField(verbose_name="创建时间", auto_now_add=True)

    class Meta:
        abstract = True  # 说明是一个抽象类
