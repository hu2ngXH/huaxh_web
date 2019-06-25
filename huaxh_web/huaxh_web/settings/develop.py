from .base import *  # NOQA

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases

# sqliteconfig
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
#     }
# }
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'huaxh_db',
        'USER': 'root',
        'PASSWORD': 'Hrz@123_',
        'HOST': '127.0.0.1',
        'PORT': 3306,
        # 'OPTIONS':{'charset':'utf8mb4'},
        # 'CONN_MAX_AGE':5*60 #数据库持久连接 数据库连接池的概念 django中的连接是每一个请求结束都会关闭当前的数据库连接 多线程不要配置
    }
}
# local-memory caching:内存缓存 线程安全 进程间是独立的 这个是默认配置
# CACHE = {
#     'default': {
#         'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
#         'LOCATION': 'unique-snowflake'
#     }
# }

# filesystem caching:把数据存到文件系统中
# CACHE = {
#     'default': {
#         'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache',
#         'LOCATION': '/var/local/django_cache'
#     }
# }

# database caching:数据库缓存 需要创建缓存用的表 意义不大
# CACHE = {
#     'default': {
#         'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
#         'LOCATION': 'unique-snowflake'
#     }
# }

# memcached: django推荐的缓存系统 也是分布式（分布式逻辑在客户端） 集成度较好
# CACHE = {
#     'default': {
#         'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
#         'LOCATION': [
#               '172.19.26.1:11211',
#               '172.19.26.2:11211'
#         ]
#     }
# }
