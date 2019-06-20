# -*- utf-8 -*-
from django.contrib.admin import AdminSite


class CustomSite(AdminSite):
    site_header = 'huaxh'
    site_title = '后台管理'
    index_title = '首页'


custom_site = CustomSite(name='cus_admin')
