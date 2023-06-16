from django.conf import settings
from django.http import Http404
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView

from .forms import EmailPostForm
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


def post_share(request, post_id):
    """ Обработка формы отправки сообщений на почту. """
    post = get_object_or_404(Post, id=post_id, status=Post.status.PUBLISHED)
    if request.method == 'POST':
        form = EmailPostForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
    else:
        form = EmailPostForm()
    context = {
        'post': post,
        'form': form
    }
    return render(request, 'blog/share.html', context)
