from django.db import models

# Create your models here.
from django.utils.translation import ugettext_lazy as _

class User(models.Model):
    """
    @todo:账号表
    """
    uid = models.CharField(_(u'用户id'), max_length=32, blank=True, null=True, help_text=u'用户唯一标识', db_index=True,
                           unique=True)
    password = models.CharField(verbose_name='密码', max_length=16)
    create_time = models.DateField(verbose_name='创建时间', auto_now_add=True)
    def __str__(self):
        return self.uid

    class Meta:
        verbose_name='用户表'
        verbose_name_plural='用户表'
    pass

class UserInfo(models.Model):
    """
    @todo:用户表
    """
    WX_USER = 1
    GUEST_USER = 11
    NORMAL_USER = 22
    COMPANY_USER = 33

    USER_SRC = (
        (WX_USER, u'微信授权用户'),
        (GUEST_USER, u'游客用户'),
        (NORMAL_USER, u'普通用户'),
        (COMPANY_USER, u'机构用户'),
    )

    MALE = 1
    FEMALE = 0

    GENDER = (
        (MALE, u'男'),
        (FEMALE, u'女'),
    )

    UNVERIFIED = 0
    ACTIVATED = 1
    DISABLED = 2
    DELETED = 3
    ASSIGN = 10

    USER_STATUS = (
        (UNVERIFIED, u'未验证'),
        (ACTIVATED, u'已激活'),
        (DISABLED, u'已禁用'),
        (DELETED, u'已删除'),
        (ASSIGN, u'已分配'),
    )

    user_id = models.CharField(_(u'用户id'), max_length=32, blank=True, null=True, help_text=u'用户唯一标识', db_index=True,
                         unique=True)
    name = models.CharField(_(u'姓名'), max_length=32, blank=True, null=True, help_text=u'用户姓名', db_index=True)
    email = models.CharField(_(u'邮箱'), max_length=40, blank=True, null=True, help_text=u'用户邮箱', db_index=True)
    sex = models.IntegerField(_(u'性别'), choices=GENDER, default=MALE, help_text=u'用户性别')
    age = models.IntegerField(_(u'年龄'), default=0, help_text=u'用户年龄')
    nickname = models.CharField(_(u'昵称'), max_length=32, blank=True, null=True, help_text=u'用户昵称')
    avatar = models.CharField(_(u'头像地址'), max_length=60, blank=True, null=True, help_text=u'用户头像')
    phone = models.CharField(_(u'手机号'), max_length=11, blank=True, null=True, help_text=u'用户电话', db_index=True)
    country = models.CharField(_(u'国家'), max_length=32, blank=True, null=True, help_text=u'用户国家')
    province = models.CharField(_(u'省份'), max_length=32, blank=True, null=True, help_text=u'用户省份')
    city = models.CharField(_(u'城市'), max_length=32, blank=True, null=True, help_text=u'用户城市')
    location = models.CharField(_(u'地址'), max_length=60, blank=True, null=True, help_text=u'用户地址')
    create_time = models.DateField(verbose_name='创建时间', auto_now_add=True)

    def __str__(self):
        return self.user_id

    class Meta:
        verbose_name='用户信息表'
        verbose_name_plural='用户信息表'
    pass


class Topic(models.Model):
    """
    @todo:帖子表
    """
    t_uid = models.CharField(verbose_name='帖子所属用户id', max_length=18)
    t_kind = models.CharField(verbose_name='类别', max_length=32)
    create_time = models.DateField(verbose_name='创建时间', auto_now_add=True)
    t_photo = models.CharField(verbose_name='帖子图片', max_length=128, null=True)
    t_content = models.CharField(verbose_name='帖子正文', max_length=3000)
    t_title = models.CharField(verbose_name='帖子标题', max_length=64)
    t_introduce = models.CharField(verbose_name='帖子简介', max_length=256)
    recommend = models.BooleanField(verbose_name='是否推荐', default=False)

    def __str__(self):
        return self.t_title

    class Meta:
        verbose_name = '帖子表'
        verbose_name_plural = '帖子表'
    pass

class Reply(models.Model):
    """
    @todo:回复表
    """
    r_tid = models.CharField(verbose_name='帖子id', max_length=16)
    r_uid = models.CharField(verbose_name='发表者id', max_length=16)
    r_photo = models.CharField(verbose_name='回复的图片', max_length=128, null=True)
    r_time = models.DateField(verbose_name='留言时间', auto_now_add=True)
    r_content = models.CharField(verbose_name='回复内容', max_length=256)

    def __str__(self):
        return self.r_tid

    class Meta:
        verbose_name = '回复表'
        verbose_name_plural = '回复表'
    pass


class Kind(models.Model):
    """
    @todo:分类表
    """
    k_name = models.CharField(verbose_name='分类名称', max_length=16)

    def __str__(self):
        return self.k_name

    class Meta:
        verbose_name = '分类表'
        verbose_name_plural = '分类表'
    pass


class Announcement(models.Model):
    """
    @todo:公告表
    """
    a_title = models.CharField(verbose_name='公告标题', max_length=64)
    a_content = models.CharField(verbose_name='公告内容', max_length=3000, null=True)

    def __str__(self):
        return self.a_title

    class Meta:
        verbose_name = '公告表'
        verbose_name_plural = '公告表'
    pass

