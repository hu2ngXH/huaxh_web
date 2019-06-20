from django.shortcuts import redirect
from django.views.generic import TemplateView

from .forms import CommentForm


class CommentView(TemplateView):
    http_method_names = ['post']
    template_name = 'comment/result.html'

    # 只提供POST方法 通过CommentForm来处理数据 然后验证并保存 最后渲染评论结果页
    def post(self, request, *args, **kwargs):
        comment_form = CommentForm(request.POST)
        target = request.POST.get('target')  # 请求的路径
        if comment_form.is_valid():  # 不是空数据
            instance = comment_form.save(commit=False)
            instance.target = target
            instance.save()
            succeed = True
            # return redirect(target)
        else:
            succeed = False

        context = {
            'succeed': succeed,
            'form': comment_form,
            'target': target,
        }
        return self.render_to_response(context)
