# -*- urf-8 -*-

from django.contrib import admin


class BaseOwnerAdmin(admin.ModelAdmin):
    """
    0.所有App都可以用到的
    1.用来自动补充文章、分类、标签、侧边栏、友链这些Model的owner字段
    2.用来针对 queryset 过滤当前用户的数据
    """
    exclude = ('owner',)  # 排除字段 与field二选一

    # 只能显示当前登录用户的请求 request默认所有数据都给予
    def get_queryset(self, request):
        qs = super(BaseOwnerAdmin, self).get_queryset(request)
        return qs.filter(owner=request.user)

    # 作用是保存数据到数据库
    # 每次保存数据库的时候需要将用户设置为当前登录的用户
    # form是页面提交过来的表单之后的对象
    # change用于标志本次保存的数据是新增的还是更新的
    # obj 当前要保存的对象 就是models那玩意儿
    def save_model(self, request, obj, form, change):
        obj.owner = request.user
        return super(BaseOwnerAdmin, self).save_model(request, obj, form, change)
