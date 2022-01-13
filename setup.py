from setuptools import setup, find_packages

setup(
    name='huaxh',
    # version='0.1',
    version='${version}',  # 在自动打包的时候需要变化版本号
    description='Huaxh Blog',
    author='hua',
    author_email='huaxh@gmail.com',
    # url='https://www.the5fire.com',
    license='MIT',

    packages=find_packages('huaxh_web'),  # 指明要打入的包
    package_dir={'': 'huaxh_web'},  # 指明上面的包在哪个目录下 如果在setup统计目录可以不写

    # 指明除了.py文件外 还需要打包哪些文件到最终的安装包里面 对应的值需要是字典格式
    # key为要找的目录 value是list结构 表示要查找的具体文件 支持通配符的方式 如果key为空 则表示要查找所有的包
    # 下面是需要打包JavaScript文件
    # package_data={'': [  # 打包数据文件，方法一
    #     'themes/*/*/*/*',  # 需要按目录层级匹配
    # ]},

    include_package_data=True,  # 方法二：配合MANIFEST.in文件 一般使用这种方式 可以两种方式共存

    install_requires=[
        "Django==2.1.8",
        "django-autocomplete-light==3.3.5",
        "django-ckeditor==5.7.1",
        "django-js-asset==1.2.2",
        "django-rest-framework==0.1.0",
        "djangorestframework==3.9.4",
        "entrypoints==0.3",
        "idna==2.8",
        "image==1.5.27",
        "ipykernel==5.1.0",
        "Jinja2==2.10.1",
        "jsonschema==3.0.1",
        "Pillow==9.0.0",
        "PyMySQL==0.9.3",
        "webencodings==0.5.1",
        "widgetsnbextension==3.4.2",
        "sqlparse==0.3.0",
        "Send2Trash==1.5.0",
    ],  # 指明依赖版本 安装项目的时候首先安装依赖包
    # extras_require 额外的依赖
    scripts=[
        'huaxh_web/manage.py',
        'huaxh_web/huaxh_web/wsgi.py',
    ],  # 指明要放到bin目录下的可执行文件 这里我们把项目的manage.py放进去 安装完毕之后就可以通过manage.py runserver来启动项目了

    entry_points={
        'console_scripts': [
            'huaxh_manage = manage:main',
        ]
    },
    # 表示程序执行的点 比较常用的配置就是console_scripts 用来生成一个可执行文件bin目录下
    # 会生成一个huaxh_manage可执行文件到bin目录下 执行此命令就相当于执行了manage.py中的main方法（在manage.py中增加main方法）
    classifiers=[  # Optional
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 3 - Alpha',

        # Indicate who your project is intended for 指明项目受众
        'Intended Audience :: Developers',
        'Topic :: Blog :: Django Blog',

        # Pick your license as you wish 选择项目许可证
        'License :: OSI Approved :: MIT License',

        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        'Programming Language :: Python :: 3.7',
    ],  # 项目当前的状况
)
