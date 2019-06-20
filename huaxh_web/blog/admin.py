# -*- coding:utf-8 -*-
from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from django.contrib.admin.models import LogEntry

from .models import Post, Category, Tag
from .adminforms import PostAdminForm
from huaxh_web.custom_site import custom_site
from huaxh_web.base_admin import BaseOwnerAdmin


# 同一个页面编辑关联数据
class PostInline(admin.TabularInline):  # 可选择继承自admin.StackedInline，以获取不同的展示样式
    fields = ('title', 'desc')
    extra = 1  # 控制额外多几个
    model = Post


@admin.register(Category, site=custom_site)  # 注册站点的时候就注册到新建的site上面去
class CategoryAdmin(BaseOwnerAdmin):
    inlines = [PostInline, ]  # 扩展Category字段 可以在分类页面编辑post页面
    list_display = ('name', 'status', 'is_nav', 'created_time', 'post_count')  # 用于显示
    fields = ('name', 'status', 'is_nav')  # 提交表单的内容 Form

    def post_count(self, obj):
        return obj.post_set.count()

    post_count.short_description = '文章数量'


@admin.register(Tag, site=custom_site)
class TagAdmin(BaseOwnerAdmin):
    list_display = ('name', 'status', 'created_time')
    fields = ('name', 'status')


class CategoryOwnerFilter(admin.SimpleListFilter):
    """ 自定义过滤器只展示当前用户分类 两个属性两个方法重写"""
    title = '分类'
    parameter_name = 'owner_category'  # URL参数 例如查询分类id为1的内容 URL后面的Query部分是?owner_category = 1

    # 返回要展示的内容和查询用的id
    def lookups(self, request, model_admin):
        return Category.objects.filter(owner=request.user).values_list('id', 'name')

    # 根据URL Query的内容返回列表页数据 self.value() 就是?owner_category = 1 中的1 QuerySet就是列表页所有展示数据的集合
    def queryset(self, request, queryset):
        category_id = self.value()
        if category_id:
            return queryset.filter(category_id=self.value())
        return queryset


@admin.register(Post, site=custom_site)
class PostAdmin(BaseOwnerAdmin):
    form = PostAdminForm
    list_display = [
        'title', 'category', 'status',
        'created_time', 'operator'
    ]
    list_display_links = ['title']  # 用来配置哪些字段可以作为链接 点击它们 可以进入编辑页面

    list_filter = (CategoryOwnerFilter,)  # 页面过滤器 自定义过滤器
    search_fields = ['title', 'category__name']  # 搜索字段 通过__双下划线的方式指定搜索关联model的数据

    # 第一个元素是string 第二个元素是dict dict的key可以是‘fields’、'description'和‘classes’
    fieldsets = (
        ('基础配置', {
            'fields': (
                ('title', 'category'),  # todo bug 第二个用户在分类筛选的时候 发现了第一个用户的分类
                'status',
                'tag',
            ),
        }),
        ('内容', {
            'fields': (
                'desc',
                'is_md',
                'content',
                'content_ck',
                # 'content_md',
            ),
        })
    )

    filter_vertical = ('tag',)

    # 自定义list_display的对象 参数固定 就是当前行的对象
    def operator(self, obj):
        return format_html(
            '<a href = "{}">编辑</a>',
            reverse('cus_admin:blog_post_change', args=(obj.id,))
        )

    operator.short_description = '操作'  # 指定表头的展示文案

    # class Media:
    #     # 完整的资源地址 页面加载的时候会把这些资源加载到页面上
    #     css = {
    #         'all': ("https://cdn.bootcss.com/bootstrap/4.0.0-beta.2/css/bootstrap.min.css",),
    #     }
    #     js = ("https://cdn.bootcss.com/bootstrap/4.0.0-beta.2/js/bootstrap.bundle.js",)
    #

@admin.register(LogEntry, site=custom_site)
class LogEntryAdmin(admin.ModelAdmin):
    list_display = ['object_repr', 'object_id', 'action_flag', 'user', 'change_message']
