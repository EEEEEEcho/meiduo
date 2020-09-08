from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

# 使用Django中自带的用户模型类和注册功能，对自带的用户模型类修改，然后使用。
class User(AbstractUser):
    """自定义用户模型类"""
    mobile = models.CharField(max_length=11,unique=True,verbose_name="手机号")

    class Meta:
        db_table = 'tb_user'    # 自定义表名
        # 在admin站点管理该表时，这个表叫做 用户
        verbose_name = '用户'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.username