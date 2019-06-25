from .base import *  # NOQA

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

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
