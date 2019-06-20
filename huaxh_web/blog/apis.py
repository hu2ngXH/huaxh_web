from rest_framework import generics
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Post, Category
from .serializers import PostSerializers, PostDetailSerializers, CategorySerializer, CategoryDetailSerializer

from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser

'''
# function view
# View转换为API View的装饰器可以提供可选参数api_view(['GET','POST'])来限定请求的类型
@api_view()
def post_list(request):
    posts = Post.objects.filter(status=Post.STATUS_NORMAL)
    post_serializers = PostSerializers(posts, many=True)
    return Response(post_serializers.data)


# class view
# ListCreateAPIView很像ListView 只需要指定queryset 和 用来序列化的类 而且可以有create功能 可以接受POST请求
# ListAPIView类只是单纯输出列表 仅支持GET功能
class PostList(generics.ListCreateAPIView):
    queryset = Post.objects.filter(status=Post.STATUS_NORMAL)
    serializer_class = PostSerializers
'''


# 每一个资源都需要CRUD操作 所以需要更上层的抽象 能在一个类里面完成所有的方法维护 完成了CRUD操作的定义
class PostViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = PostSerializers
    queryset = Post.objects.filter(status=Post.STATUS_NORMAL)

    # permission_classes = [IsAdminUser] 写入的权限校验 我们没有写入的需求
    # viewsets.ModelViewSet -》 viewsets.ReadOnlyModelViewSet 用来创建只读接口

    # 使用这个方法重设 serializer_class的值
    def retrieve(self, request, *args, **kwargs):
        self.serializer_class = PostDetailSerializers
        return super().retrieve(request, *args, **kwargs)

    # 获取某个分类下的文章
    def filter_queryset(self, queryset):
        category_id = self.request.query_params.get('category')
        if category_id:
            queryset = queryset.filter(category_id=category_id)
        return queryset


class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = CategorySerializer
    queryset = Category.objects.filter(status=Category.STATUS_NORMAL)

    def retrieve(self, request, *args, **kwargs):
        self.serializer_class = CategoryDetailSerializer
        return super().retrieve(request, *args, **kwargs)
