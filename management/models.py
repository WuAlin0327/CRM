from django.db import models
from rbac.models import UserInfo as User
# Create your models here.

class School(models.Model):
    """
    校区表
    """
    title = models.CharField(verbose_name='校区名称',max_length=32)

    def __str__(self):
        return self.title


class Depart(models.Model):
    """
    部门表
    """
    title = models.CharField(verbose_name='部门名称',max_length=32)

    def __str__(self):
        return self.title

class UserInfo(User):
    name = models.CharField(verbose_name='真名',max_length=16,default='miao')
    phone = models.IntegerField(verbose_name='电话号码')
    gen = (
        (1, '男'),
        (2, '女')
    )
    gender = models.IntegerField(verbose_name='性别',choices=gen,default=1)
    depart = models.ForeignKey(verbose_name='部门',to='Depart',on_delete=models.CASCADE)
