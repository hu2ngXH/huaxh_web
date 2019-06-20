from django.contrib import admin

from .models import Comment

from huaxh_web.custom_site import custom_site
from huaxh_web.base_admin import BaseOwnerAdmin


# Register your models here.


@admin.register(Comment, site=custom_site)
class CommetAdmin(BaseOwnerAdmin):
    list_display = ('target', 'nickname', 'content', 'website', 'created_time')
