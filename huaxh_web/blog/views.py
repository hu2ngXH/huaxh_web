from django.views.generic import ListView, DetailView
from .models import Post, Tag, Category
from config.models import SideBar
from comment.models import Comment
from comment.forms import CommentForm


# 通用处理
class CommonViewMixin:
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)  # 获取上下文 这是一个多态的继承 super指的是下面IndexView这个类的继承
        context.update({
            'sidebars': SideBar.get_all(),  # 侧边栏
        })
        context.update(Category.get_navs())  # 分类
        return context


# 首页处理
class IndexView(CommonViewMixin, ListView):
    queryset = Post.latest_posts()
    paginate_by = 5  # 每页数量
    context_object_name = 'post_list'  # 指定上下文 context变量要使用的名字
    template_name = 'blog/list.html'


from django.shortcuts import get_object_or_404


# 分类列表页处理
class CategoryView(IndexView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category_id = self.kwargs.get('category_id')
        category = get_object_or_404(Category, pk=category_id)  # 为什么是pk 用来获取一个对象的实例 如果获取到 就返回实例对象 如果不存在直接抛出404错误
        context.update({
            'category': category,
        })
        return context

    def get_queryset(self):
        """重写queryset，根据分类过滤"""
        queryset = super().get_queryset()
        category_id = self.kwargs.get('category_id')
        return queryset.filter(category_id=category_id)


# 标签列表页处理
class TagView(IndexView):
    def get_context_date(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tag_id = self.kwargs.get('tag_id')  # 参数从url中拿到
        tag = get_object_or_404(Tag, pk=tag_id)
        context.update({
            'tag': tag,
        })
        return context

    def get_queryset(self):
        """重写queryset，根据分类过滤"""
        queryset = super().get_queryset()
        tag_id = self.kwargs.get('tag_id')
        return queryset.filter(tag__id=tag_id)


# 博文详情页
class PostListView(ListView):
    queryset = Post.latest_posts()
    paginate_by = 1  # 每页数量设置
    context_object_name = 'post_list'
    template_name = 'blog/list.html'


from datetime import date
from django.core.cache import cache  # 缓存 没有配置的情况下是内存缓存 内存缓存进程间独立


class PostDetailView(CommonViewMixin, DetailView):
    queryset = Post.latest_posts()  # 两次过滤 一次拿到所有的最新数据 一次找到对应的id
    template_name = 'blog/detail.html'  # TemplateView的参数 直接调用静态页面
    context_object_name = 'post'
    pk_url_kwarg = 'post_id'  # 这个是第二次过滤的参数

    def get(self, request, *args, **kwargs):
        response = super().get(request, *args, **kwargs)
        self.handle_visited()
        return response

    def handle_visited(self):
        increase_pv = False
        increase_uv = False
        uid = self.request.uid
        pv_key = 'pv:%s:%s' % (uid, self.request.path)
        uv_key = 'uv:%s:%s:%s' % (uid, str(date.today()), self.request.path)
        if not cache.get(pv_key):
            increase_pv = True
            cache.set(pv_key, 1, 1 * 60)  # 1分钟有效
        if not cache.get(uv_key):
            increase_uv = True
            cache.set(uv_key, 1, 24 * 60 * 60)  # 24小时有效

        from django.db.models import F

        if increase_uv and increase_pv:
            Post.objects.filter(pk=self.object.id).update(pv=F('pv') + 1, uv=F('uv') + 1)
        elif increase_pv:
            Post.objects.filter(pk=self.object.id).update(pv=F('pv') + 1)
        elif increase_uv:
            Post.objects.filter(pk=self.object.id).update(pv=F('uv') + 1)


from django.db.models import Q  # 条件表达式


# 搜索栏
class SearchView(IndexView):
    def get_context_data(self):
        context = super().get_context_data()
        context.update({
            'keyword': self.request.GET.get("search", '')  # 在上下文中增加key
        })
        return context

    def get_queryset(self):
        queryset = super().get_queryset()  # 这里调用了IndexView的get_queryset
        keyword = self.request.GET.get("search")
        # print("search is", keyword)
        if not keyword:
            return queryset
        # Q表达式实现了类似 SELECT * FROM post WHERE title ILIKE '%<keyword>%' or desc ILIKE '%<keyword>%'
        return queryset.filter(Q(title__icontains=keyword) | Q(desc__icontains=keyword))  # 过滤条件是相似查询只是忽略大小写


# 增加作者页面
class AuthorView(IndexView):
    def get_queryset(self):
        queryset = super().get_queryset()
        author_id = self.kwargs.get('owner_id')
        return queryset.filter(owner_id=author_id)

# from django.shortcuts import render
# # factions view
# def post_list(request, category_id=None, tag_id=None):
#     tag = None
#     category = None
#
#     if tag_id:
#         post_list, tag = Post.get_by_tag(tag_id)
#     elif category_id:
#         post_list, tag = Post.get_by_category(category_id)
#     else:
#         post_list = Post.latest_posts()
#     context = {
#         'category': category,
#         'tag': tag,
#         'post_list': post_list,
#         'Sidebars': SideBar.get_all(),
#     }
#     context.update(Category.get_navs())  # 更新操作 就相当于在末尾增加
#     return render(request, 'blog/list.html', context=context)
#
#
# def post_detail(request, post_id=None):
#     print("post_id=", post_id)
#     print("request: ", vars(request))  #
#     try:
#         post = Post.objects.get(id=post_id)
#     except Post.DoesNotExist:
#         post = None
#     context = {
#         'post': post,
#         'sidebars': SideBar.get_all(),
#     }
#     context.update(Category.get_navs())
#     print("context:", context)
#     return render(request, 'blog/detail.html', context=context)
