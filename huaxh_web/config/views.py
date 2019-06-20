from django.views.generic import ListView
from .models import Link
from blog.views import CommonViewMixin
from django.shortcuts import HttpResponse


# Create your views here.

def links(request):
    return HttpResponse('links')


class LinkListView(CommonViewMixin, ListView):
    queryset = Link.objects.filter(status=Link.STATUS_NORMAL)
    template_name = "config/links.html"
    context_object_name = 'link_list'
