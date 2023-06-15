from django.conf import settings
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, get_object_or_404

from .models import Post


def post_list(request):
    """ Представление списка постов. """
    posts = Post.published.all()
    paginator = Paginator(posts, settings.MAX_PAGES)
    page_number = request.GET.get('page', 1)
    try:
        page_obj = paginator.page(page_number)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)
    context = {'page_obj': page_obj}
    return render(request, 'blog/list.html', context)


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
