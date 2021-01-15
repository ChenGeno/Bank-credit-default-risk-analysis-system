from django.db import models
from dataclasses import dataclass
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser

# Create your models here.


class Staff(models.Model):
    def __str__(self):
        return "Staff:[id={}, sno={}, sname={}]".format(
            self.id, self.sno, self.sname
        )

    class Sex(models.IntegerChoices):  # 采用 Django 提供了的 IntegerChoices 类，完成性别字段的枚举
        WOMAN = 0
        MAN = 1

    id = models.AutoField(primary_key=True)  # 用户id。 (AutoField：自增)
    sno = models.CharField(max_length=32, unique=True)  # 员工号(系统账号)  (unique=True : 字段唯一)
    password = models.CharField(max_length=32)  # 密码
    sname = models.CharField(max_length=32)  # 员工姓名
    email = models.EmailField(null=True, max_length=32)  # 邮箱 (blank=True 允许空值)
    sex = models.IntegerField(choices=Sex.choices, default=1)  # 性别  (default=1 : 默认为男性)
    """
      目前，将 auto_now 或 auto_now_add 设置为 True，将导致该字段设置为 editable=False 和 blank=True。
      auto_now: 每次保存对象时，自动将该字段设置为现在。  auto_now_add: 当第一次创建对象时，自动将该字段设置为现在。
    """
    create_time = models.DateField(auto_now=False, auto_now_add=True)  # 创建时间
    update_time = models.DateField(auto_now=True, auto_now_add=False)  # 最近一次修改时间
