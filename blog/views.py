from django.conf import settings
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView
from django.http import Http404

from .models import Post


class PostListView(ListView):
    """ Представление списка постов. """
    queryset = Post.published.all()
    context_object_name = 'posts'
    paginate_by = settings.MAX_PAGES
    template_name = 'blog/list.html'

    def get_context_data(self, **kwargs):
        try:
            return super(PostListView, self).get_context_data(**kwargs)
        except Http404:
            self.kwargs['page'] = 1
            return super(PostListView, self).get_context_data(**kwargs)


def post_detail(request, year: int, month: int, day: int, post: str):
    """ Детальное представление поста. """
    post = get_object_or_404(
        Post,
        status=Post.Status.PUBLISHED,
        slug=post,
        publish__year=year,
        publish__month=month,
        publish__day=day
    )

    return render(request, 'blog/detail.html', {'post': post})
