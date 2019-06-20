# -*- coding:utf-8 -*-
from django.db import models

from blog.models import Post


# 评论app 按照耦合的方式 耦合到文章上
class Comment(models.Model):
    STATUS_NORMAL = 1
    STATUS_DELETE = 0
    STATUS_ITEMS = (
        (STATUS_NORMAL, '正常'),
        (STATUS_DELETE, '删除'),
    )

    # target = models.ForeignKey(Post, on_delete=models.CASCADE,
    #                            verbose_name="评论目标")  # 一个文章可以有多个评论 但是一个评论只能针对一篇文章 级联删除 删除主表 这个表也没有了
    target = models.CharField(max_length=100, verbose_name="评论目标")  # 里面存放被评论内容的网址 只需要有一个能够唯一标识当前页面地址的标记即可 admin后台无法处理权限
    content = models.CharField(max_length=2000, verbose_name="内容")
    nickname = models.CharField(max_length=50, verbose_name="昵称")
    website = models.URLField(verbose_name="网站")
    email = models.EmailField(verbose_name="邮箱")
    status = models.PositiveIntegerField(default=STATUS_NORMAL, choices=STATUS_ITEMS, verbose_name="状态")
    created_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")

    class Meta:
        verbose_name = verbose_name_plural = "评论"
        ordering = ['-id']

    @classmethod
    def get_by_target(cls, target):
        return cls.objects.filter(target=target, status=cls.STATUS_NORMAL)  # target表示某篇文章
