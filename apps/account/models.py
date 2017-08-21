from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    avatar = models.URLField(blank=True, verbose_name="头像")
    creditrank = models.IntegerField(default=100, verbose_name="信用级别")
    usertype = models.IntegerField(choices=((0, "商家"), (1, "用户")), verbose_name="用户类型", default=1)
    phonenumber = models.CharField(max_length=11, blank=True, verbose_name="联系方式")
    truename = models.CharField(max_length=30, blank=True, verbose_name="真实姓名")

    can_order = models.BooleanField(verbose_name="是否能订餐", default=True)

    def get_now_order_list(self):
        try:
            return self.myorder.all().filter(is_accept=True, is_done=False, is_abnormal=False)
        except:
            return None

    def get_done_order_list(self):
        try:
            return self.myorder.all().filter(is_accept=True, is_done=True, is_abnormal=False)
        except:
            return None

    def get_collect_list(self):
        try:
            return self.mycollect.business.all()
        except:
            return None

    def get_businessuser_now_order(self):
        try:
            return self.business.order_list.orders.all().order_by('-date_create')
        except:
            return None


class Accesstoken(models.Model):
    access_token = models.CharField(max_length=200)
    date_create = models.DateTimeField(auto_now_add=True)


class OAuthQQProfile(models.Model):
    user = models.OneToOneField(User, verbose_name="用户")
    qq_openid = models.CharField(max_length=100, blank=True)
    access_token = models.CharField(max_length=100, blank=True)
    nickname = models.CharField(max_length=256, blank=True, verbose_name="昵称")
    sex = models.IntegerField(choices=((1, "男"), (2, "女"), (0, "未知")), verbose_name="性别", default=1)
    stuid = models.CharField(max_length=20, verbose_name="学号", blank=True)

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name = "QQ个人信息"
        verbose_name_plural = verbose_name
