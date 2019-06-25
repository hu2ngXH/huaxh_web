"""huaxh_web URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path, include

from .custom_site import custom_site

from blog.views import IndexView, CategoryView, TagView, PostDetailView, SearchView, AuthorView
from config.views import LinkListView
from comment.views import CommentView
from django.contrib.sitemaps import views as sitemap_views
from blog.rss import LatestPostFeed
from blog.sitemap import PostSitemap

# from blog.apis import PostList
# from blog.apis import post_list
# from blog.views import post_detail, post_list

# 一个路径对应一个函数
# / 首页
# /post/<post_id>/ 博文详情页
# /category/<category_id>/ 分类列表页
# /tag/<tag_id>/ 标签列表页
# /links/友链展示页
# 列表页View：根据不同的查询条件分别展示博客首页、分类列表页和标签列表页
# 文章页View：展示博文详情页
# 友链页View：展示所有友情链接


from rest_framework.routers import DefaultRouter
from blog.apis import PostViewSet, CategoryViewSet

router = DefaultRouter()
router.register(r'post', PostViewSet, base_name='api-post')
router.register(r'category', CategoryViewSet, base_name='api-category')

from rest_framework.documentation import include_docs_urls  # docs工具

from django.conf import settings
from django.conf.urls import url, include
from django.conf.urls.static import static
from .autocomplete import CategoryAutocomplete, TagAutocomplete

from django.views.decorators.cache import cache_page  # 缓存模块

urlpatterns = [
                  re_path(r'^$', IndexView.as_view(), name='index'),
                  re_path(r'^category/(?P<category_id>\d+)$', CategoryView.as_view(), name='category-list'),
                  re_path(r'^tag/(?P<tag_id>\d+)$', TagView.as_view(), name='tag-list'),
                  re_path(r'^post/(?P<post_id>\d+)$', PostDetailView.as_view(), name='post-detail'),
                  re_path(r'^links/$', LinkListView.as_view(), name='links'),
                  re_path(r'^search/$', SearchView.as_view(), name='search'),  # 搜索页面
                  re_path(r'^author/(?P<owner_id>\d+)$', AuthorView.as_view(), name='author'),  # 作者页面
                  re_path(r'^comment/$', CommentView.as_view(), name='comment'),

                  re_path(r'^rss|feed/', LatestPostFeed(), name='rss'),
                  re_path(r'^sitemap\.xml$', cache_page(60 * 20, key_prefix='sitemap_cache_'), sitemap_views.sitemap,
                          # 对这个接口进行缓存 缓存了sitemap这个接口 第一次访问之后 后面20分钟之内的访问都不需要再次生成sitemap了
                          {'sitemaps': {'posts': PostSitemap}}),

                  # re_path(r'^api/post/', PostList.as_view(), name='post-list'),
                  # re_path(r'^api/post/', post_list, name='post-list'),

                  re_path(r'^api/', include(router.urls)),

                  re_path(r'^api/docs', include_docs_urls(title='huaxh apis')),
                  url(r'^category-autocomplete/$', CategoryAutocomplete.as_view(), name='category-autocomplete'),
                  url(r'^tag-autocomplete/$', TagAutocomplete.as_view(), name='tag-autocomplete'),

                  # path('links/', links, name='links'),
                  # re_path(r'^category/(?P<category_id>\d+)$', CategoryView.as_view(), name='category-list'), class view
                  # re_path(r'^category/(?P<category_id>\d+)$', post_list, name='category-list'), function view
                  # path('category/<int:category_id>', post_list, name='category_list'), function view

                  path('admin/', custom_site.urls),  # 用户管理页面
                  path('super_admin/', admin.site.urls),  # 超级管理员

                  # 富文本图片路径 ckeditor_uploader.urls提供两个接口：接受上传图片和浏览已上传的图片
                  re_path(r'^ckeditor/', include('ckeditor_uploader.urls')),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
