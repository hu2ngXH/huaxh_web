from rest_framework import serializers, pagination
from .models import Post, Category

'''
用于序列化数据
'''


# class PostSerializers(serializers.HyperlinkedModelSerializer): todo 不知道为什么这个不行 之后研究一下
class PostSerializers(serializers.ModelSerializer):
    # SlugRelatedField如果是外键数据需要通过它来配置 定义外键是否可写 如果是多对多的话 就需要many选项 slug_field指定展示的字段是什么
    category = serializers.SlugRelatedField(
        read_only=True,
        slug_field='name'
    )
    tag = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field='name'
    )
    owner = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username'
    )
    created_time = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")

    class Meta:
        model = Post
        fields = ['id', 'title', 'category', 'tag', 'owner', 'created_time']


class PostDetailSerializers(PostSerializers):
    class Meta:
        model = Post
        fields = ['id', 'title', 'category', 'tag', 'owner', 'content_html', 'created_time']


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = (
            'id', 'name', 'created_time',
        )


class CategoryDetailSerializer(CategorySerializer):
    # SerializerMethodField:作用是帮我们把posts字段获取的内容映射到paginated_posts方法上
    posts = serializers.SerializerMethodField('paginated_posts')

    def paginated_posts(self, obj):
        posts = obj.post_set.filter(status=Post.STATUS_NORMAL)
        paginator = pagination.PageNumberPagination()
        page = paginator.paginate_queryset(posts, self.context['request'])
        serializer = PostSerializers(page, many=True, context={'request': self.context['request']})
        return {
            'count': posts.count(),
            'results': serializer.data,
            'previous': paginator.get_previous_link(),
            'next': paginator.get_next_link(),
        }

    class Meta:
        model = Category
        fields = (
            'id', 'name', 'created_time', 'posts',
        )
